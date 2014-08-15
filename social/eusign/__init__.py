from social.backends.base import BaseAuth
from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthCanceled, AuthUnknownError, \
                              AuthMissingParameter, AuthStateMissing, \
                              AuthStateForbidden

from requests import HTTPError

EUSIGN_HOST = "https://eusign.org"

# http://zakon4.rada.gov.ua/laws/show/z1399-12
DRFO_ID = '1.2.804.2.1.1.1.11.1.4.1.1'
DAEMON_VERSION = "0.4.2"


class Eusign(BaseOAuth2):
    name = 'eusign'

    AUTHORIZATION_URL = EUSIGN_HOST+'/oauth'
    ACCESS_TOKEN_URL = EUSIGN_HOST+'/oauth/token'
    API_BASE = EUSIGN_HOST

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        data = self._user_data(access_token)
        return data

    def _user_data(self, access_token, path=None):
        url = '{}/api/1/users/{}'.format(self.API_BASE, path or 'me')
        return self.get_json(url, params={'access_token': access_token})

    def get_user_details(self, response):
        fullname, first_name, last_name = self.get_user_names(
            response.get('name')
        )
        return {
            'fullname': fullname,
            'first_name': first_name,
            'last_name': last_name,
        }

    def get_user_id(self, details, response):
        return response['uniq']


class EusignDSTU(BaseAuth):
    name = 'eusign-dstu'

    AUTHORIZATION_URL = EUSIGN_HOST+'/auth/{app_id}/?itype=full&state={state}'
    ACCESS_TOKEN_URL = EUSIGN_HOST+'/auth/access_token'
    CERT_API_URL = EUSIGN_HOST+'/api/1/certificates/{cert_id}'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('taxid', 'taxid'),
       # ('expires', 'expires')
    ]

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        data = self._user_data(access_token)
        return data

    def auth_url(self):
        name = self.name + '_state'
        state = self.strategy.session_get(name)
        if state is None:
            state = self.state_token()
            self.strategy.session_set(name, state)
            print 'set state', name, state

        return self.AUTHORIZATION_URL.format(app_id=self.app_id, state=state)

    def auth_complete(self, *args, **kwargs):
        self.process_error(self.data)
        try:
            response = self.check_signature(
                self.dstud_url,
                data=self.auth_complete_params(self.validate_state()),
            )
        except HTTPError as err:
            if err.response.status_code in [403, 404]:
                raise AuthCanceled(self)
            else:
                raise
        except Exception as ex:
            print 'ex', ex
            raise
            raise AuthUnknownError(self)

        if response is None:
            raise AuthUnknownError(self)

        return self.do_auth(response)

    def validate_state(self):
        """Validate state value. Raises exception on error, returns state
        value if valid."""
        state = self.strategy.session_get(self.name + '_state')
        request_state = self.data.get('state')
        if request_state and isinstance(request_state, list):
            request_state = request_state[0]

        if not request_state:
            raise AuthMissingParameter(self, 'state')
        elif not state:
            raise AuthStateMissing(self, 'state')
        elif not request_state == state:
            raise AuthStateForbidden(self)
        else:
            return state


    def check_signature(self, url, data):
        cert = self.fetch_certificate(data['cert_id'])
        check_data = '{nonce}|{url}'.format(url=self.redirect_uri, **data)
        sign = data['sign']
        sign = sign.replace('-', '+').replace('_', '/')
        body = 'c={cert}&d={data}&s={sign}'.format(cert=cert, data=check_data,
                                                   sign=sign)
        return self.request(url, method='POST', data=body,
            headers={"Expect": "Version=%s", })

    def parse_user(self, dstu_data):
        ret = {}
        for line in dstu_data.text.split('\n'):
            if '=' not in line:
                continue
            key, value = line.strip().split('=', 1)
            ret[key] = value

        ret['tax_id'] = ret.get(DRFO_ID)
        return ret

    def fetch_certificate(self, cert_id):
        url = self.cert_url(cert_id)
        cert_data = self.request(url)
        if cert_data.status_code != 200:
            raise AuthUnknownError(self, "Failed to fetch certificate")

        return cert_data.text

    def cert_url(self, cert_id):
        return self.CERT_API_URL.format(cert_id=cert_id)

    def do_auth(self, response):
        user_data = self.parse_user(response)
        return self.strategy.authenticate(response=user_data, backend=self)

    def get_user_details(self, response):
        if response['tax_id']:
            uniq = response['tax_id']
        else:
            uniq = response['CN']

        if response.get('GN'):
            full_name = response['GN']
        else:
            full_name = response['CN']

        name = full_name.split()

        return {
            "username": uniq,
            "fullname": response['CN'],
            "first_name": name[0],
            "last_name": response.get('SN') or name[-1],
        }

    def auth_complete_params(self, state=None):
        return {
            "nonce": self.data.get('nonce'),
            "cert_id": self.data.get('cert_id'),
            "sign": self.data.get('sign'),
        }

    @property
    def app_id(self):
        return self.setting('APP_ID')

    @property
    def dstud_url(self):
        return self.setting('DSTUD_URL')

