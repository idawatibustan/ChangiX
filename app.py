import json
import base64
import requests
from flask import Flask, render_template, request, send_file, redirect, url_for
from gevent.wsgi import WSGIServer
from settings import *

app = Flask(__name__)
app.debug = True

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/scan", methods=["GET", "POST"])
def scan():
    if request.method == "POST":
        img = base64.b64decode(request.data)
        open("file.png", "w").write(img)
        files = {"media": open("file.png", "rb")}
        r = requests.post("https://zxing.org/w/decode", files=files)
        print r.text
        return json.dumps("")
    if request.method == "GET":
        return send_file("file.png", mimetype="image/png")

@app.route("/file/<file>")
def reroute(file):
    return send_file("file.png", mimetype="image/png")

http_server = WSGIServer(("", PORT), app)
http_server.serve_forever()
