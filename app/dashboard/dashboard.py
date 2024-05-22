from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils.commons import check_uuid, get_raw_jwt
from utils.api import update_user_active_cape, update_user_active_accessories
from utils.decorators import redirect_mobile_devices


dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates', static_folder='static', static_url_path='/dashboard/static')


@dashboard_bp.route('/', methods=['GET'])
@redirect_mobile_devices
@jwt_required()
def dashboard():
    return render_template('dashboard.html', uuid=get_jwt_identity())

@dashboard_bp.route('/cape', methods=['GET'])
@redirect_mobile_devices
@jwt_required()
def cape():
    return render_template('cape.html')

@dashboard_bp.route('/accessories', methods=['GET'])
@redirect_mobile_devices
@jwt_required()
def accessories():
    return render_template('accessories.html')


@dashboard_bp.route('/cape/update', methods=['GET'])
@redirect_mobile_devices
@jwt_required()
def update_cape():
    access_token = get_raw_jwt(request)

    # get cape uuid from query string
    uuid =  request.args.get('cape_uuid')
    if uuid is None:   # if no args
        return redirect(url_for('dashboard.cape'))

    if uuid == "":   # if no uuid
        try:
            update_user_active_cape(None, get_jwt_identity(), access_token)   # remove active cape
        except Exception as e:
            current_app.logger.exception(f"{request.remote_addr} - ({get_jwt_identity()}) Failed to remove custom cape : {e}")
            flash("Failed to remove custom cape: "+str(e), 'error')
        else:
            current_app.logger.info(f"{request.remote_addr} - ({get_jwt_identity()}) Removed active cape")
            flash("Custom cape removed", 'success')
        return redirect(url_for('dashboard.dashboard'))
    
    # validate uuid
    if not check_uuid(uuid):
        flash("Invalid cape uuid", 'warning')
        return redirect(url_for('dashboard.dashboard'))
    
    # update active cape
    try:
        update_user_active_cape(uuid, get_jwt_identity(), access_token)
    except Exception as e:
        current_app.logger.exception(f"{request.remote_addr} - ({get_jwt_identity()}) Failed to update active cape : {e}")
        flash("Failed to update active cape: "+str(e), 'error')
    else:
        current_app.logger.info(f"{request.remote_addr} - ({get_jwt_identity()}) Updated active cape")
        flash("Active cape updated", 'success')
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/accessories/update', methods=['GET'])
@redirect_mobile_devices
@jwt_required()
def update_accessories():
    access_token = get_raw_jwt(request)

    # get uuids from query string
    uuids_str =  request.args.get('accessories_uuids')
    if uuids_str is None:   # if no args
        return redirect(url_for('dashboard.accessories'))

    if uuids_str == "":   # if no uuids
        try:
            update_user_active_accessories([], get_jwt_identity(), access_token)   # remove all active accessories
        except Exception as e:
            current_app.logger.exception(f"{request.remote_addr} - ({get_jwt_identity()}) Failed to remove active accessories : {e}")
            flash("Failed to remove active accessories: "+str(e), 'error')
        else:
            current_app.logger.info(f"{request.remote_addr} - ({get_jwt_identity()}) Removed all active accessories")
            flash("Active accessories removed", 'success')
        return redirect(url_for('dashboard.dashboard'))

    # extract uuids
    try:
        uuids = uuids_str.split(',')
        uuids = [uuid.strip() for uuid in uuids]
    except:
        flash("Invalid query", 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    # validate uuids
    for uuid in uuids:
        if not check_uuid(uuid):
            flash("An uuid is invalid", 'warning')
            return redirect(url_for('dashboard.dashboard'))
    
    if len(uuids) > 5:   # if too many accessories
        flash("Too many accessories (max 5)", 'warning')
        return redirect(url_for('dashboard.dashboard'))

    # update active accessories
    try:
        update_user_active_accessories(uuids, get_jwt_identity(), access_token)
    except Exception as e:
        current_app.logger.exception(f"{request.remote_addr} - ({get_jwt_identity()}) Failed to update active accessories : {e}")
        flash("Failed to update active accessories: "+str(e), 'error')
    else:
        current_app.logger.info(f"{request.remote_addr} - ({get_jwt_identity()}) Updated active accessories")
        flash("Active accessories updated", 'success')
    return redirect(url_for('dashboard.dashboard'))