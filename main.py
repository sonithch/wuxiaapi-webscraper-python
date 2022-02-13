import os
import _thread
import threading

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


@app.route("/syncJob")
def test():
    if request.args.get("key") == str(os.environ.get("SyncJobKey")):
        t = threading.Thread(target=novelCrawler.novelCrawler)
        t.start()
        return "syncJob triggered"
    else:
        return "Invalid Auth!!"

def syncJob():
    print("")


# server start
if __name__ == "__main__":
    app.run()
