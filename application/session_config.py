import secrets
from application import manucrypt_app
from flask_session import Session


def session_config():

    # Flask session config
    SECRET_KEY = secrets.token_urlsafe(32)
    manucrypt_app.secret_key = SECRET_KEY
    manucrypt_app.config['SESSION_TYPE'] = 'filesystem'
    sess = Session()
    sess.init_app(manucrypt_app)
    return
