import os

from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_restplus.apidoc import apidoc

flask_bcrypt = Bcrypt()


def create_app(config_name):
    url_prefix = os.getenv('urlPrefix')

    # Make a global change setting the URL prefix for the swaggerui at the module level
    apidoc.url_prefix = url_prefix

    app = Flask(__name__)

    CORS(app)

    flask_bcrypt.init_app(app)

    return app
