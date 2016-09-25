import os
import pickle
import json
import base64
import requests
from passenger import Passenger
from shopping import Shopping
from recommender import Recommender
from fake_useragent import UserAgent
from flask import Flask, render_template, request, send_file, redirect, url_for, session
from gevent.wsgi import WSGIServer
from settings import *

app = Flask(__name__)
app.secret_key = os.urandom(24).encode("hex")
app._static_folder = "static/"
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
        r = requests.post("https://zxing.org/w/decode", files=files, headers={"User-Agent": UserAgent().random})
        resp = r.text
        send = {
                "status": "Fail"
                }
        if "Decode Succeeded" in resp:
            data = resp.split("<pre>")[1].split("</pre>")[0]
            if len(data) > 15:
                send = {
                    "status": "Success",
                    "data": resp.split("<pre>")[1].split("</pre>")[0]
                        }
        print resp
        print send
        return json.dumps(send)
    if request.method == "GET":
        return send_file("file.png", mimetype="image/png")

#@app.route("/login/<id_type>/<data>")
@app.route("/login")
#def login(id_type, data):
def login():
    url = request.url
    if "demo" not in url:
        session["demo"] = False
        passenger = Passenger({
            "id_type": url.split("id_type=")[1].split("&")[0],
            "data": url.split("data=")[1],
            "demo": False
            })
    else:
        session["demo"] = True
        passenger = Passenger({
            "demo": True
            })
    session["passenger"] = passenger.uid
    with open("pickle/"+passenger.uid+".pickle", "wb") as f:
        pickle.dump(passenger, f)
    return redirect(url_for("welcome"))

@app.route("/welcome")
def welcome():
    if "passenger" in session:
        with open("pickle/"+session["passenger"]+".pickle", "rb") as f:
            passenger = pickle.load(f)
            data = {
                    "first_name": passenger.firstname,
                    "last_name": passenger.lastname,
                    "gate": passenger.gate,
                    "board_time": passenger.boardtime,
                    "airline": passenger.airlines,
                    "flightnum": passenger.flightnum,
                    "time_to_board": passenger.time_to_board(),
                    "destination": passenger.dest
                    }
        return render_template("welcome.html", data=data)
    else:
        return redirect(url_for("home"))

@app.route("/swipe/<demo>", methods=["GET", "POST"])
def swipe(demo):
    if "passenger" in session:
        if request.method == "GET":
            with open("pickle/"+session["passenger"]+".pickle", "rb") as f:
                passenger = pickle.load(f)
            if demo == "demo":
                r = Recommender(passenger=passenger,demo=True)
            elif demo == "normal":
                r = Recommender(passenger=passenger,demo=False)
            with open("pickle/"+passenger.uid+"_swipe.pickle", "wb") as f:
                pickle.dump(passenger, f)
            cards = []
            while True:
                card = r.checkpoint_info()
                if card is None:
                    break
                cards.append(card)
            data = {
                    "checkpoint_info": cards
                    }
            return render_template("swipe.html", data=data)
        elif request.method == "POST":
            print request.data
    else:
        return redirect(url_for("home"))

@app.route("/explore")
def explore():
    data = {}
    return render_template("explore.html", data=data)

http_server = WSGIServer(("", PORT), app)
http_server.serve_forever()
