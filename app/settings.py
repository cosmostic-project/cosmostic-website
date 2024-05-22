import os
import secrets
import string
from datetime import timedelta


def generate_random_secret_key(lenth:int=16):
    """
    Generates a random secret key of the specified length.

    Parameters:
        lenth (int, optional): The length of the secret key. Defaults to 16.

    Returns:
        str: The randomly generated secret key.
    """
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(lenth))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', generate_random_secret_key(16))

    API_URL = os.environ.get('API_URL', "http://localhost:81/")

    # external links
    DISCORD_URL = "https://discord.com/invite/m4Q8p3Bk"
    SUPPORT_URL = DISCORD_URL
    DOCS_URL = "https://cosmostic-project.github.io/cosmostic-docs/"
    CLIENT_DOWNLOAD_URL = "https://cosmostic-project.github.io/cosmostic-docs/requirements/"

    # Session
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # OAuth
    MCAUTH_CLIENT_ID = os.environ.get('MCAUTH_CLIENT_ID')
    MCAUTH_CLIENT_SECRET = os.environ.get('MCAUTH_CLIENT_SECRET')

    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'Lax'