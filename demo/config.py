DEBUG = True
SECRET_KEY = 'change me please'

from os.path import dirname, abspath, join
SQLALCHEMY_DATABASE_URI = 'sqlite:////%s/data.sqlite' % dirname(abspath(__file__))

SOCIAL_AUTH_USER_MODEL = 'User'
SOCIAL_AUTH_LOGIN_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social.eusign.EusignDSTU',
    'social.eusign.Eusign',
)

SOCIAL_AUTH_USER_FIELDS = ['username', 'email', 'fullname', 'tax_id']

# auth url is set to http://127.0.0.1:5000/complete/eusign/
SOCIAL_AUTH_EUSIGN_DSTU_APP_ID = ''

SOCIAL_AUTH_EUSIGN_KEY = '415a2699b4a143fdb147dc40b16a5eea'
SOCIAL_AUTH_EUSIGN_SECRET = 'fhcOak3CS2LFmZqSLPLZfdeffE344rlOxm9cRd8A'
