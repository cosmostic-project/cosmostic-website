from flask import Request, current_app
from uuid import UUID
import requests


def check_uuid(uuid):
    """
    Checks if the input UUID is valid.
    
    Parameters:
    uuid (str): The UUID string to be checked.
    
    Returns:
    bool: True if the input UUID is valid, else False.
    """
    try:
        uuid = UUID(uuid)
    except ValueError:
        return False
    return True

def get_raw_jwt(request:Request):
    """
    Retrieves the raw JWT token from the provided Flask request object.

    Parameters:
        request (Request): The Flask request object containing the cookies.

    Returns:
        str: The raw JWT token value, or None if the token is not found.
    """
    return request.cookies.get(current_app.config['JWT_ACCESS_COOKIE_NAME'])

def check_url(url:str):
    """
    Checks if the given URL is valid (returns 200 status code).

    Parameters:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is valid, else False.
    """
    try:
        r = requests.get(url)

        if r.status_code != 200:
            return False
    except:
        return False
    return True

def check_device_type(user_agent:str):
    """
    Checks if the given user agent is from an Android or iPhone device.

    Parameters:
        user_agent (str): The user agent string to check.

    Returns:
        bool: True if the user agent is an Android or iPhone device, else False.
    """
    return 'Android' in user_agent or 'iPhone' in user_agent