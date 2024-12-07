from base64 import b64encode, encode
from time import time
from requests import post, models
from urllib.parse import urlencode

class SpotifyOAuth(object):
    """
    Spotify Authorization 

    """
    token_url: str = "https://accounts.spotify.com/api/token"
    auth_url: str = "https://accounts.spotify.com/authorize"

    def __init__(self, client_id: str | None=None, client_secret: str | None=None, scope: str | None=None, redirect_uri: str | None=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.redirect_uri = redirect_uri

    def get_client_credentials(self) -> str:
        """
        Returns base64 string.
        """
        if self.client_id == None or self.client_secret == None:
            raise Exception("client_id or _client secret not set")
        client_creds: str = f"{self.client_id}:{self.client_secret}"
        client_creds_64: bytes = b64encode(client_creds.encode()) 
        return client_creds_64.decode()

    def get_token_headers(self) -> dict[str, str]:
        client_creds_64: str = self.get_client_credentials()
        return  {
            "Authorization": f"Basic {client_creds_64}"
        }

    def get_token_data(self) -> dict[str, str]:
        return {
            "grant_type": "client_credentials"
        }

    def get_authorize_url(self) -> str:
        """
        Request authorization from the user to access data.
        """
        data: dict[str, any] = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": self.scope
        }
        urlparams: str = urlencode(data)
        return "%s?%s" % (self.auth_url, urlparams)

    def get_access_token(self, code: str | None =None) -> dict:
        """
        Request access and refresh token.
        """
        token_url: str = self.token_url
        # data for Implicit Grant Flow
        token_data: dict[str, any] = self.get_token_data() #prob obrisati
        token_headers: dict[str, str] = self.get_token_headers()
        # data for Authorization Code Flow
        if code != None:
            token_data = {
                "redirect_uri": self.redirect_uri,
                "code": code,
                "grant_type": "authorization_code",
            }
        r: models.Response = post(token_url, data=token_data, headers=token_headers,)

        # check if request is valid (200-299)
        if r.status_code  not in range(200, 299):
            raise Exception("Couldn't authenticate client")

        token_info: dict = r.json()
        token_info = self.add_custom_values_to_token_info(token_info)
        return token_info

    def add_custom_values_to_token_info(self, token_info: dict) -> dict:
        """
        Add expires at property to token_info.
        """
        token_info["expires_at"] = int(time()) + token_info["expires_in"]
        return token_info
