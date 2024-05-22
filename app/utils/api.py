from flask import current_app
import requests


def _create_api_exception(response:requests.Response):
    """
    Creates an exception message based on the response from an API request.

    Args:
        response (requests.Response): The response object from the API request.

    Returns:
        str: The exception message.
    """
    try:
        error = response.json()
        return f"{error['message']} ({error['code']})"
    except:   # if response is None/False or does not have error message
        return "Failed to fetch data from API"

def _make_api_request(endpoint:str, method:str, params:dict=None, authorization:str=None):
    """
    Makes an API request to the specified endpoint with the given method and parameters.

    Args:
        endpoint (str): The endpoint to make the API request to.
        method (str): The HTTP method to use. Must be one of 'put', 'get', 'post', or 'delete'.
        params (dict, optional): The parameters to include in the request. Defaults to None.
        authorization (str, optional): The authorization token to include in the request headers. Defaults to None.

    Returns:
        requests.Response: The response object from the API request.
        bool: False if the request fails or encounters an exception.
    """
    api_base_url = current_app.config.get("API_URL")
    url = f"{api_base_url}{endpoint}"
    headers = {'Authorization': f"Bearer {authorization}"} if authorization else {}

    try:
        match method:
            case 'put':
                r = requests.put(url, params=params, headers=headers)
            case 'get':
                r = requests.get(url, params=params, headers=headers)
            case 'post':
                r = requests.post(url, params=params, headers=headers)
            case 'delete':
                r = requests.delete(url, params=params, headers=headers)
    except:
        return False
    return r

def _fetch_user_data(endpoint:str, user_uuid:str):
    """
    Fetches user data from the specified endpoint for the given user UUID.

    Args:
        endpoint (str): The endpoint to fetch data from.
        user_uuid (str): The UUID of the user.

    Returns:
        [dict, str, list]: The fetched user data.
        bool: False if the request fails or encounters an exception.
    """
    r = _make_api_request(f"user/{user_uuid}/{endpoint}", method='get')
    
    if r is False or r.status_code not in (200, 422):
        return False
    
    if r.status_code == 422:   # if no active item
        return "" if endpoint == "cape" else []
    
    return r.json()


def fetch_user_active_cape(user_uuid:str):
    """
    Fetches the active cape for the specified user UUID.

    Args:
        user_uuid (str): The UUID of the user.

    Returns:
        str: The user's active cape.
        bool: False if the request fails or encounters an exception.
    """
    return _fetch_user_data("cape", user_uuid)

def fetch_user_active_accessories(user_uuid:str):
    """
    Fetches the active accessories for the specified user UUID.

    Args:
        user_uuid (str): The UUID of the user.

    Returns:
        list: The user's active accessories.
        bool: False if the request fails or encounters an exception.
    """
    return _fetch_user_data("accessories", user_uuid)

def update_user_active_cape(cape_uuid:str, user_uuid:str, access_token:dict):
    """
    Updates the active cape for a user.

    Args:
        cape_uuid (str): The UUID of the cape to update. If None, the active cape will be deleted.
        user_uuid (str): The UUID of the user.
        access_token (dict): The access token for authentication.

    Returns:
        bool: True if the update was successful.

    Raises:
        Exception: If the API request fails or encounters an exception.
    """
    if not cape_uuid:
        r = _make_api_request(f"user/{user_uuid}/cape", method='delete', authorization=access_token)   # delete cape
    else:
        r = _make_api_request(f"user/{user_uuid}/cape", method='put', params={'cape_uuid': cape_uuid}, authorization=access_token)   # update cape
    
    if r is False or r.status_code not in (200, 201, 422):
        raise Exception(_create_api_exception(r))
    return True

def update_user_active_accessories(accessories_uuids:list, user_uuid:str, access_token:dict):
    """
    Updates the active accessories for a user.

    Args:
        accessories_uuids (list): The list of UUIDs of the accessories to update.
        user_uuid (str): The UUID of the user.
        access_token (dict): The access token for authentication.

    Returns:
        bool: True if the update was successful.

    Raises:
        Exception: If the API request fails or encounters an exception.
    """
    # fetch user active accessories
    active_accessories = fetch_user_active_accessories(user_uuid)
    if active_accessories is False:
        raise Exception(_create_api_exception(False))

    # delete accessories not in new accessories
    for accessory in active_accessories:
        if accessory not in accessories_uuids:
            r = _make_api_request(f"user/{user_uuid}/accessories", method='delete', params={'accessory_uuid': accessory}, authorization=access_token)   # delete it

            if r is False or r.status_code not in (200, 201):
                raise Exception(_create_api_exception(r))
        else:
            accessories_uuids.remove(accessory)   # avoid duplicate accessories

    # add new accessories
    for accessory in accessories_uuids:
        r = _make_api_request(f"user/{user_uuid}/accessories", method='post', params={'accessory_uuid': accessory}, authorization=access_token)

        if r is False or r.status_code not in (200, 201, 409):
            raise Exception(_create_api_exception(r))
    return True