from flask import Flask, g, render_template, redirect
from social.apps.flask_app.routes import social_auth
from social.apps.flask_app.models import init_social
from social.apps.flask_app.template_filters import backends

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user, logout_user, UserMixin

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(social_auth)

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
init_social(app, db)

@app.before_request
def set_g_user():
    g.user = current_user._get_current_object()


@login_manager.user_loader
def load_user(userid):
    from models import User
    try:
        return User.query.get(int(userid))
    except (TypeError, ValueError):
        pass


@app.route('/')
def index():
    return render_template('index.html', user=g.user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

