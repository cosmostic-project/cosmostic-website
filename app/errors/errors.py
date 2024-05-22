from flask import Blueprint, flash, redirect, make_response, url_for, render_template, jsonify, current_app, request
from flask_jwt_extended import unset_access_cookies

from extensions import jwt


errors_bp = Blueprint('errors', __name__, template_folder='templates', static_folder='static', static_url_path='/errors/static')


@errors_bp.app_errorhandler(404)
def page_not_found(_):
    """
    Handles 404 errors.

    Returns:
        Flask response with error template and a 404 status code.
    """
    error = {
        'code': 404,
        'title': "Page not found",
        'message': "The page you are looking for doesn't exist or has been removed."
    }
    response = render_template('errors.html', error=error)
    return make_response(response, 404)

@errors_bp.app_errorhandler(Exception)
def internal_server_error_callback(e):
    """
    Handles internal server errors.

    Returns:
        Flask response with error template and a 500 status code.
    """
    error = {
        'code': 500,
        'title': "Internal server error",
        'message': "Internal server error : please contact support"
    }

    current_app.logger.exception(f"{request.remote_addr} - Internal server error : {e}")
    response = render_template('errors.html', error=error)
    return make_response(response, 500)


@jwt.unauthorized_loader
def unauthorized_callback(_):
    """
    Handles unauthorized access. 

    Returns:
        Flask response with empty string and 401 status code if API path.
        Flask response with redirect to home page and flashed message.
    """
    if request.path == url_for("auth.get_identity"):   # if API path
        return make_response(jsonify(None), 401)
    
    current_app.logger.info(f"{request.remote_addr} - Unauthorized access to {request.path}")
    flash("Unauthorized : please login", 'warning')
    return redirect(url_for("home.home"))

@jwt.invalid_token_loader
def invalid_token_callback(reason):
    """
    Handles invalid token.

    Returns:
        Flask response with redirect to home page and flashed message.
    """
    response = make_response(redirect(url_for('home.home')))
    unset_access_cookies(response)   # remove token

    current_app.logger.info(f"{request.remote_addr} - Invalid token : {reason}")
    flash("Invalid token : please login", 'error')
    return response

@jwt.expired_token_loader
def expired_token_callback(_, payload):
    """
    Handles expired token.

    Returns:
        Flask response with redirect to home page and flashed message.
    """
    response = make_response(redirect(url_for('home.home')))
    unset_access_cookies(response)   # remove token

    current_app.logger.info(f"{request.remote_addr} - ({payload.get('sub')}) Expired token")
    flash("Session expired : please login", 'info')
    return response