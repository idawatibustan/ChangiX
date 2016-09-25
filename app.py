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

from datetime import datetime, timedelta
from random import randint
def helper(passenger):
    arrival = passenger.get_arrival_gate()
    dest = passenger.get_dest_gate()
    r = Recommender(demo=True)
    checkpoints = r.recommendations()

    curr_time = arrival['time']
    stack = []
    stack.append({
        'time': curr_time.strftime("%H:%M"),
        'title': 'Arrival Gate {}'.format(arrival['gate']),
        'subtitle': '{} from {}'.format(arrival['flight'], arrival['from'])
    })

    for chk in checkpoints:
        d = {}
        curr_time = curr_time - timedelta(minutes=randint(15,60))
        d['time'] = curr_time.strftime("%H:%M")
        d['title'] = chk['name']
        max_char = 65 # KYLE: change to vary maximum characters allowed
        d['subtitle'] = chk['description'][:max_char] + '...'
        stack.append(d)

    stack.append({
        'time': (curr_time - timedelta(minutes=randint(30,80))).strftime("%H:%M"),
        'title': 'Departure Gate {}'.format(dest['gate']),
        'subtitle': '{} to {}'.format(dest['flight'], dest['to'])
    })
    return [i for i in reversed(stack)]

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
        return json.dumps({
            "status": "Success",
            #"data": "M1LEE/JUHO%20%20%20%20%20%20%20%20%20%20%20%20E8EKVV7%20SINHKGCX%200710%20209Y056K0224%2034A&gt;1180%20%20%20%20%20%20B%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%2029%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%208"
            "data": "M1LEE/JUHO            E8EKVV7 HKGSFOCX 0870 209Y049E0167 34A&gt;1180      B                29                                         8"
            })
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
    with open("pickle/"+session["passenger"]+".pickle", "rb") as f:
        passenger = pickle.load(f)
        arr_gate, dest_gate = passenger.get_arrival_gate(), passenger.get_dest_gate()
        arr_time, dest_time = arr_gate["time"], dest_gate["time"]
        arr_gate["time"] = arr_time.strftime("%H:%M")
        dest_gate["time"] = dest_time.strftime("%H:%M")
        r = Recommender(demo=True)
        recs = r.recommendations()
        print recs
        s = Shopping(recs)
        top_list = s.get_list(5)
        print top_list
        data = {
                "arrival": arr_gate,
                "destination": dest_gate,
                "objects": helper(passenger),
                "shopping": top_list
                }
    print json.dumps(data, indent=4)
    return render_template("explore.html", data=data)

@app.route("/logout")
def logout():
    session.pop("passenger", None)
    return redirect(url_for("home"))

@app.route("/item")
def item():
    return render_template("item.html")

@app.route("/win")
def win():
    return render_template("win.html")

http_server = WSGIServer(("", PORT), app)
http_server.serve_forever()
