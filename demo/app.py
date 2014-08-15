from flask import Flask, g, render_template, redirect
from social.apps.flask_app.routes import social_auth, init_social

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user, logout_user, UserMixin

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(social_auth)

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
init_social(app, db)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(200))
    tax_id = db.Column(db.String(16))


@app.before_request
def set_g_user():
    g.user = current_user._get_current_object()


@login_manager.user_loader
def load_user(userid):
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


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8000)
