from flask import Flask, request, jsonify

# local imports
import webScraper

# constants
app = Flask(__name__)


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


# server start
if __name__ == "__main__":
    app.run()
