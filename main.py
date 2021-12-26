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
    return response


@app.route("/chapters")
def getChapter():
    response = jsonify(webScraper.getChapter(request.args.get("url")))
    return response


def test():
    novelCrawler.novelCrawler()


def test1():
    print("webjob1")


# server start
if __name__ == "__main__":
    scheduler.add_job(test, "interval", seconds=60*60)
    scheduler.add_job(test1, "interval", seconds=1)

    scheduler.start()
    app.run()
