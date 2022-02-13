from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import mysql.connector

# local imports
import novelCrawler
import webScraper
import sqlConnect

# constants
app = Flask(__name__)
scheduler = BackgroundScheduler()


@app.route("/")
def root():
    return "Python Flask API for WuxiaApp"


@app.route("/search")
def searchNovel():
    response = jsonify(webScraper.searchNovel(request.args.get("query")))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/chapters")
def getChapter():
    response = jsonify(webScraper.getChapter(request.args.get("url")))
    return response


def test():
    novelCrawler.novelCrawler()


# server start
if __name__ == "__main__":
    app.run()
