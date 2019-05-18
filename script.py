from urllib.parse import quote
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import requests
from urllib.parse import quote

CLIENT_ID = "eaaaf83e6d3647548dcb9a8c3ffa1149"
CLIENT_SECRET = "5d8a3852d8ec457ca10d6bfab06a6701"
SCOPES = "user-read-currently-playing user-read-recently-played"
QUOTE_SCOPES=quote(SCOPES.encode("utf-8"))

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize?response_type=code&client_id={}&scope={}&redirect_uri={}'.format(CLIENT_ID, QUOTE_SCOPES, "http://127.0.0.1:8081/callback/q")

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def authorize():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": "http://127.0.0.1:8081/callback/q",
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)

    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)