from urllib.parse import quote
import json
import requests
from flask import request
import base64

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
USER_PLAYLISTS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, 'playlists')
USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, 'top')  # /<type>
USER_RECENTLY_PLAYED_ENDPOINT = "{}/{}/{}".format(USER_PROFILE_ENDPOINT,'player', 'recently-played')
BROWSE_FEATURED_PLAYLISTS = "{}/{}/{}".format(SPOTIFY_API_URL, 'browse', 'featured-playlists')

CLIENT_ID = "eaaaf83e6d3647548dcb9a8c3ffa1149"
CLIENT_SECRET = "5d8a3852d8ec457ca10d6bfab06a6701"
SCOPES = "user-read-currently-playing user-read-recently-played"

HOST = "http://127.0.0.1"
PORT = "8081"

current_access_token = ""
current_refresh_token = ""
CURRENT_AUTH_HEADER = ""
REDIRECT_URI = "{}:{}/callback/q".format(HOST, PORT)

def authorize_app():
    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "client_id": CLIENT_ID
    }
    url_args = "&".join(["{}={}".format(key, quote(val)) for key,val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return auth_url

def authorize_user():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    if 'error' in response_data:
        return False
    

    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    current_refresh_token = refresh_token
    current_access_token = access_token
    # Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    # CURRENT_AUTH_HEADER = authorization_header
    # print("HEADER: " + authorization_header)
    return authorization_header


def request_new_token():
    payload = {
        "grant_type" : "refresh_token",
        "refresh_token" : current_refresh_token
    }

    base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=payload, headers=headers)

    response_data = json.loads(post_request)
    new_token = response_data['access_token']
    new_refresh = response_data['refresh_token']

    current_access_token = new_token
    current_refresh_token = new_refresh

    return current_access_token

def get_user_data(auth_header):
    url = USER_PROFILE_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()