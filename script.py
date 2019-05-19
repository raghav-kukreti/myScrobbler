from urllib.parse import quote
import json
import requests
from flask import request

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

CLIENT_ID = "eaaaf83e6d3647548dcb9a8c3ffa1149"
CLIENT_SECRET = "5d8a3852d8ec457ca10d6bfab06a6701"
SCOPES = "user-read-currently-playing user-read-recently-played"

HOST = "http://127.0.0.1"
PORT = "80"

REDIRECT_URI = quote("{}:{}/callback/q".format(HOST, PORT))


print(REDIRECT_URI)
def authorize():
    pass