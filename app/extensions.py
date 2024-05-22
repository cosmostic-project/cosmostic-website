from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import JWTManager
from flask_minify import Minify


oauth = OAuth()
jwt = JWTManager()
minify = Minify()