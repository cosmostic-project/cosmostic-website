from flask import Blueprint, redirect, make_response, url_for, jsonify, flash, current_app,request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, set_access_cookies, unset_access_cookies

from extensions import oauth
from utils.decorators import redirect_mobile_devices


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET'])
@redirect_mobile_devices
@jwt_required(optional=True)
def login():
    if get_jwt_identity():   # if already logged in
        return redirect(url_for('dashboard.dashboard'))
    
    redirect_uri = url_for('auth.authorize', _external=True)
    return oauth.mcauth.authorize_redirect(redirect_uri, scope='profile')   # redirect to auth page

@auth_bp.route('/authorize', methods=['GET'])
@redirect_mobile_devices
def authorize():
    if not request.args:   # if no query string
        return redirect(url_for('home.home'))
    
    if request.args.get('error') == 'access_denied':   # if user denies login
        flash("Login cancelled", 'info')
        return redirect(url_for('home.home'))

    try:
        oauth.mcauth.authorize_access_token()   # complete login

        # get user uuid
        profile = oauth.mcauth.get('profile').json()
        uuid = profile.get('id')

        access_token = create_access_token(identity=uuid)   # create jwt
    except Exception as e:
        current_app.logger.exception(f"{request.remote_addr} - Failed to complete login : {e}")
        flash("Failed to complete login", 'error')
        return redirect(url_for('home.home'))
    
    # create response
    response = make_response(redirect(url_for('dashboard.dashboard')))
    set_access_cookies(response, access_token)

    current_app.logger.info(f"{request.remote_addr} - ({uuid}) User logged in")
    flash(f"Successfully logged in", 'success')
    return response

@auth_bp.route('/logout', methods=['GET'])
@redirect_mobile_devices
@jwt_required()
def logout():
    response = make_response(redirect(url_for('home.home')))
    unset_access_cookies(response)   # logout

    current_app.logger.info(f"{request.remote_addr} - ({get_jwt_identity()}) User logged out")
    flash("Successfully logged out", 'success')
    return response


@auth_bp.route('/identity', methods=['GET'])
@redirect_mobile_devices
@jwt_required()
def get_identity():
    return jsonify(get_jwt_identity()), 200