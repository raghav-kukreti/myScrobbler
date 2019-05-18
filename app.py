#!/usr/bin/env python3    
import json
from script import SPOTIFY_AUTH_URL, CLIENT_ID, CLIENT_SECRET
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import quote

PORT = 8081
app = Flask(__name__)

auth_check = False
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
@app.route('/')
def home(auth_check=auth_check):
    return render_template('index.html', isAuthorized=auth_check)

@app.route('/auth/')
def authenticate():
    return redirect(SPOTIFY_AUTH_URL)

@app.route('/callback/q')
def callback():
    
    return render_template('dashboard.html', data=profile_data)
    
if __name__ == '__main__':
    app.run(debug=True, port=PORT)

    