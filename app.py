#!/usr/bin/env python3    
import json
from script import SPOTIFY_AUTH_URL, CLIENT_ID, CLIENT_SECRET
from script import authorize_app, authorize_user, get_user_data, get_users_recently_played,get_current_playing
from flask import Flask, request, redirect, g, render_template, session
import requests
from urllib.parse import quote

PORT = 8081
app = Flask(__name__)
app.secret_key = "youcantguessthislmaoslowthai"

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
        session['auth_header'] = auth
        return render_template('auth_done.html', title="Authorization done!")



@app.route('/dashboard/')
def dashboard():
    # print(session.get('auth_header', None))
    auth_header = session.get('auth_header', None)
    return render_template('dashboard.html', user_data=get_user_data(auth_header), current_data=get_current_playing(auth_header))


if __name__ == '__main__':
    app.run(debug=True, port=PORT)

    