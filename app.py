#!/usr/bin/env python3    
import json
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import quote


PORT = 8081
app = Flask(__name__)
    
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=PORT)

    