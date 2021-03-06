from flask import Flask, request
from utils import *

app = Flask(__name__)


@app.route("/")
def index():
    current_routes = "Current routes: <br><br> summonerDetails<br><br>summonerChamps<br><br>summonerLastMatch"
    return current_routes


@app.route("/summonerDetails", methods=["GET"])
def summonerDetails():
    args = request.args
    name = args.get("name")

    return {"API": "Response Positive",
            "Details": getSummonerDetailsByName(name)}


@app.route("/summonerChamps", methods=["GET"])
def summonerChamps():
    args = request.args
    name = args.get("name")
    return {"API": "Response Positive",
            "Champs": getSummonerTopChampionsByName(name)}


@app.route("/summonerLastMatch", methods=["GET"])
def summonerGame():
    args = request.args
    name = args.get("name")
    return {"API": "Response Positive",
            "Details": getMatchHistoryByNameLOL(name)}


if __name__ == "__main__":
    app.run()
