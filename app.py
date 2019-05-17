#!/usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__)

my_obj = Obj(1,2)

@app.route('/')
def home(items = my_obj.list_store()):
    return render_template('index.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)