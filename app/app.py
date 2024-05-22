from flask import Flask, request
import logging.config
import yaml

from settings import Config
from extensions import oauth, jwt, minify
from home import home_bp
from dashboard import dashboard_bp
from auth import auth_bp
from errors import errors_bp
from utils.commons import check_url


# load logging config
with open('logging.yml') as config:
    LOGGING_CONFIG = yaml.safe_load(config.read())


def create_app():
    """
    Creates and configures the Flask application.

    Returns:
    app: configured Flask application.
    """
    # configure logging
    logging.getLogger("werkzeug").disabled = True   # disable werkzeug default logging
    logging.config.dictConfig(LOGGING_CONFIG)

    # create app
    app = Flask(__name__)
    app.config.from_object(Config)
    app.logger.debug("Config loaded")

    # validate external urls
    app.config['API_URL'] = app.config['API_URL'] + '/' if not app.config['API_URL'].endswith('/') else app.config['API_URL']   # add / if not present to end of API url

    app.logger.debug("Validating external urls...")
    for url in [app.config['DISCORD_URL'], app.config['SUPPORT_URL'], app.config['CLIENT_DOWNLOAD_URL'], app.config['DOCS_URL'], app.config['API_URL']]:
        if not check_url(url):
            app.logger.error(f"Invalid URL in config: {url}")
            raise ValueError(f"Invalid URL in config: {url}")

    # init extensions
    oauth.init_app(app)
    jwt.init_app(app)
    minify.init_app(app)
    # configure minify
    minify.html = True
    minify.cssless = True
    minify.js = True

    # configure oauth client
    oauth.register(
        name="mcauth",
        access_token_url="https://mc-auth.com/oAuth2/token",
        access_token_params={
            "grant_type": "authorization_code",
            "client_id": app.config.get("MCAUTH_CLIENT_ID"),
            "client_secret": app.config.get("MCAUTH_CLIENT_SECRET")
        },
        authorize_url="https://mc-auth.com/oAuth2/authorize",
        authorize_params={
            "response_type": "code"
        },
        api_base_url="https://mc-auth.com/api/v2/",
    )
    
    # register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(errors_bp)

    # requests logging
    @app.after_request
    def log_requests(response):
        app.logger.info(f"{request.remote_addr} - [{request.method}] {request.url} | {response.status_code}")
        return response

    app.logger.debug("App created")
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()