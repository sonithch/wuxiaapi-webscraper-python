import requests
from bs4 import BeautifulSoup as bsoup
import time

# local imports
import webScraper, sqlConnect, constants


def novelCrawler():
    novels = list()
    connection = sqlConnect.create_db_connection()

    start = time.perf_counter()

    for page in range(1, 200):
        apiUrl = constants.ASSETURL.replace("@@page", str(page))
        page = bsoup(requests.get(apiUrl).content, "html.parser")

        for novel in page.findAll("div", class_="update_item list_category"):
            title = novel.get("title")
            metadata = novel.find("a", attrs={"title": title})

            url = metadata.get("href")
            imgUrl = metadata.find("img").get("src")
            values = tuple([title, url, imgUrl, 0])

            sqlConnect.insertOrUpdateToTable(connection, "Novels", values, constants.NOVELS_COLUMNS)

    end = time.perf_counter()
    print(f"Downloaded the tutorial in {end - start:0.4f} seconds")
