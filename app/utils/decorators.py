from flask import redirect, url_for, flash, request
from functools import wraps

from utils.commons import check_device_type


def redirect_mobile_devices(f):
    """
    Decorator function that redirects mobile devices to the home page.

    Parameters:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_agent = request.headers.get('User-Agent')   # get user agent
        if user_agent and check_device_type(user_agent):   # if Android or iPhone device
            flash("You can't access this page on mobile devices", 'info')
            return redirect(url_for('home.home'))
        
        return f(*args, **kwargs)
    return decorated_function