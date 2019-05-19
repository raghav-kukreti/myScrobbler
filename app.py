#!/usr/bin/env python3    
import json
from script import SPOTIFY_AUTH_URL, CLIENT_ID, CLIENT_SECRET, CURRENT_ACCESS_TOKEN, CURRENT_REFRESH_TOKEN
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
    auth = authorize_user()
    if auth == False:
        return render_template('auth_done.html', title="Access token expired!")
    else:
        return render_template('auth_done.html', title="Authorization done!")
    

@app.route('/dashboard/')
def dashboard():

    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True, port=PORT)

    