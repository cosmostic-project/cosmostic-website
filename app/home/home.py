from flask import Blueprint, render_template, redirect, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils.commons import check_device_type


home_bp = Blueprint('home', __name__, template_folder='templates', static_folder='static', static_url_path='/home/static')


@home_bp.route('/', methods=['GET'])
@jwt_required(optional=True)
def home():
    user_agent = request.headers.get('User-Agent')
    if user_agent and check_device_type(user_agent):   # if Android or iPhone device
        return render_template('mobile.html')
    
    return render_template('home.html', authenticated=True if get_jwt_identity() else False)

@home_bp.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@home_bp.route('/docs', methods=['GET'])
def docs():
    return redirect(current_app.config['DOCS_URL'])

@home_bp.route('/discord', methods=['GET'])
def discord():
    return redirect(current_app.config['DISCORD_URL'])

@home_bp.route('/support', methods=['GET'])
def support():
    return redirect(current_app.config['SUPPORT_URL'])

@home_bp.route('/download', methods=['GET'])
def download():
    return redirect(current_app.config['CLIENT_DOWNLOAD_URL'])