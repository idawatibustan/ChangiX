import json
from flask import Flask, render_template
from gevent.wsgi import WSGIServer
from settings import *

app = Flask(__name__)
app.debug = True

@app.route("/")
def home():
    return render_template("home.html")

http_server = WSGIServer(("", PORT), app)
http_server.serve_forever()
