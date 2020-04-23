"""deal with user authentication"""
import webbrowser
import requests
import uuid

AUTH_SERVER_URL = 'http://localhost:5000'

class Cronify:
    """deals with authenication for Cronify API

    Attributes:
        auth_server_url (str):  The base URL of the auth server (see auth_server.py)
    """
    def __init__(auth_server_url=AUTH_SERVER_URL):
        self.auth_server_url = auth_server_url

    def user(self, identifier=uuid.uuid4().hex):
        """Authenticate a user with cronify
        
        Args:
            identifier (str): the id for the user, if none is given a new 
                one will be generated. make sure to store this as it will be 
                needed in order to refresh the access_token

        Returns:
            a tuple containing: the access token, the refresh token, the number of 
                seconds until expiry, the identifier (given as a parameter or generated)
        """
        response = requests.get(f'{self.auth_server_url}/auth/authurl/{identifier}')
        webbrowser.open(response.text)
        response = requests.get(f'{self.auth_server_url}/auth/gettoken/{identifier}')
        json = response.json()
        return (json['access_token'], json['refresh_token'], json['expires_in'],  identifier)

    def refresh(self, identifier, refresh_token):
        """Refresh the cronify token for a user

        Args:
            identifier (str): the identifier for the user (returned from `auth.user_cronify`)
            refresh_token (str): the refresh token for the user

        Returns:
            a tuple containing: the new access token, the new refresh token, the number of seconds
                until the access token expires 
        """
        response = requests.get(f'{self.auth_server_url}/auth/gettoken/{identifier}/{refresh_token}')
        json = response.json()
        print(json)
        return (json['access_token'], json['refresh_token'], json['expires_in'])

