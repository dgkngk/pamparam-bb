from flask import Flask, render_template, request
from get_data import get_klines, get_one_kline
import json


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        list = {"15min":"15MIN","1hr":"1HOUR","4hr":"4HOUR","1d":"1DAY","1min":"1MIN"}
        return render_template('index.html', ticker_list=list, flask_token="hello")
    else:
        coin_data = get_klines(request.form['selection'])
        return render_template('main.html', coin_data=coin_data)

"""
@app.route("/")
def index():
    toke = get_one_kline()
    return render_template("index.html", flask_token=toke)
"""
@app.route("/1min")
def onemin():
    return get_klines("1MIN")

@app.route("/15min")
def fifteenmin():
    return get_klines("15MIN")

@app.route("/1hr")
def onehour():
    return get_klines("1HOUR")

@app.route("/4hr")
def fourhour():
    return get_klines("4HOUR")

@app.route("/1d")
def oneday():
    return get_klines("1DAY")

@app.route("/trial")
def trial():
    return get_one_kline()

