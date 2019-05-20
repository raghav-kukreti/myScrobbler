from urllib.parse import quote
import simplejson as json
import requests
from flask import request
import base64
SPOTIFY_CURRENTLY_PLAYING="https://api.spotify.com/v1/me/player/currently-playing"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
USER_PLAYLISTS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, 'playlists')
USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, 'top')
USER_RECENTLY_PLAYED_ENDPOINT = "{}/{}/{}".format(USER_PROFILE_ENDPOINT,'player', 'recently-played')
BROWSE_FEATURED_PLAYLISTS = "{}/{}/{}".format(SPOTIFY_API_URL, 'browse', 'featured-playlists')

CLIENT_ID = "eaaaf83e6d3647548dcb9a8c3ffa1149"
CLIENT_SECRET = "5d8a3852d8ec457ca10d6bfab06a6701"
SCOPES = "user-read-currently-playing user-read-recently-played"

HOST = "http://127.0.0.1"
PORT = "8081"

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

    return [new_token, new_refresh]

def get_user_data(auth_header):
    url = USER_PROFILE_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()

def get_users_playlists(auth_header):
    url = USER_PLAYLISTS_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_current_playing(auth_header):
    url = SPOTIFY_CURRENTLY_PLAYING
    resp = requests.get(url, headers=auth_header)
    return json.loads(str(resp.json()).replace("'", '"'))


# https://developer.spotify.com/web-api/get-users-top-artists-and-tracks/
def get_users_top(auth_header, t):
    if t not in ['artists', 'tracks']:
        print('invalid type')
        return None
    url = "{}/{type}".format(USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT, type=t)
    resp = requests.get(url, headers=auth_header)
    print(resp)

# https://developer.spotify.com/web-api/web-api-personalization-endpoints/get-recently-played/
def get_users_recently_played(auth_header):
    url = USER_RECENTLY_PLAYED_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()

# https://developer.spotify.com/web-api/get-list-featured-playlists/
def get_featured_playlists(auth_header):
    url = BROWSE_FEATURED_PLAYLISTS
    resp = requests.get(url, headers=auth_header)
    return resp.json()
