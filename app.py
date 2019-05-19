#!/usr/bin/env python3    
import json
from script import SPOTIFY_AUTH_URL, CLIENT_ID, CLIENT_SECRET
from script import authorize_app, authorize_user
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import quote

PORT = 8081
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/auth/')
def authenticate():
    auth_url = authorize_app()
    return redirect(auth_url)

@app.route('/callback/q')
def callback():
    authorization_header = authorize_user()

    return render_template('dashboard.html', header=authorization_header)
    
if __name__ == '__main__':
    app.run(debug=True, port=PORT)

    