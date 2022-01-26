# Guidance from https://newbedev.com/flask-importerror-no-module-named-app

from flask import Flask

manucrypt_app = Flask(__name__)

from application import manucrypt
