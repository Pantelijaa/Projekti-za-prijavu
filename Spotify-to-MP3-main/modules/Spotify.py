from requests import get, models, exceptions
from urllib.parse import urlencode

class Spotify(object):
    """
    Use after initial OAuth
    """
    def __init__(self, auth: str | None =None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.auth = auth

    def get_resource_header(self) -> dict:
        headers: dict = {
            "Authorization": f"Bearer {self.auth}"
        }
        return headers

    def get_resource(self, lookup_id: str, resource_type: str ='albums') -> dict:
        endpoint: str = f"https://api.spotify.com/v1/{resource_type}/{lookup_id}"
        headers: dict = self.get_resource_header()
        r: models.Response = get(endpoint, headers=headers)
        if r.status_code not in range(200,299):
            raise exceptions.RequestException(r.json())
        return r.json()

    def get_album_by_id(self, _id: str) -> dict:
        """
        Get album by specific id.
        """
        return self.get_resource(_id, resource_type='albums')
    
    def get_track_by_id(self, _id: str) -> dict:
        """
        Get track by specific id.
        """
        return self.get_resource(_id, resource_type="tracks")

    def get_artist_by_id(self, _id: str) -> dict:
        """
        Get artist by specific id.
        """
        return self.get_resource(_id, resource_type='artists')

    def get_playlists_by_user_id(self, _id: str) -> list:
        """
        Get user's playlists by user id.
        """
        modified_id: str = f"{_id}/playlists"
        data: dict = self.get_resource(modified_id, resource_type='users')
        return data["items"]
    
    def get_playlist_tracks_by_id(self, _id: str) -> list:
        """
        Get playlist tracks by playlist id.
        """
        modified_id: str = f"{_id}/tracks"
        data: dict = self.get_resource(modified_id, resource_type='playlists')
        # ako je playlista duza od 100 pesama
        max_limit: int = 100
        while data['total'] > max_limit:
            extended_data: dict = self.get_resource(modified_id + f"?offset={max_limit}", resource_type='playlists')
            for item in extended_data['items']:
                data["items"].append(item)
            max_limit += 100

        return data["items"]

    def get_user_info(self) -> dict:
        """
        Get personal informations about logged user.
        """
        headers: dict = self.get_resource_header()
        endpoint: str = "https://api.spotify.com/v1/me/"
        r: models.Response = get(endpoint, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    
    def get_saved_tracks(self) -> dict:
        """
        Get all user's saved tracks.
        """
        id = "tracks"
        resource_type="me"
        data: dict = self.get_resource(lookup_id=id, resource_type=resource_type)
        max_limit: int = 20
        while data['total'] > max_limit:
            extended_data: dict = self.get_resource(id + f"?offset={max_limit}", resource_type=resource_type)
            for item in extended_data['items']:
                data['items'].append(item)
            max_limit += 20
        return data['items']
    
    def base_search(self, query_params: str) -> dict:
        headers: dict = self.get_resource_header()
        endpoint: str = "https://api.spotify.com/v1/search"
        lookup_url: str = f"{endpoint}?{query_params}"
        r: models.Response = get(lookup_url, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()

    def search(self, query: str =None,operator: str | None =None, operator_query: str | None =None, search_type: str =None) -> dict:
        if query == None:
            raise Exception("A query is required")
        if search_type == None:
            raise Exception("Search type is required")
        if isinstance(query, dict):
            # dictionary into list
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params: str = urlencode({"q": query, "type": search_type.lower()}, safe=',')
        return self.base_search(query_params)

