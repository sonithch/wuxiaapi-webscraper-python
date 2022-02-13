import requests
from bs4 import BeautifulSoup as bsoup

## local imports
import constants


def getPage(url: str):
    return bsoup(requests.get(url).content, "html.parser")


def searchNovel(query: str):
    novels = list()
    apiUrl = constants.SEARCHURL.replace("@@query", query)
    page = bsoup(requests.get(apiUrl).content, "html.parser")

    for novel in page.findAll("div", class_="update_item list_category"):
        title = novel.get("title")
        metadata = novel.find("a", attrs={"title": title})

        url = metadata.get("href")
        imgUrl = metadata.find("img").get("src")
        lastChapter = novel.find("a", class_="chapter")

        novels.append(
            {
                "title": title,
                "url": url,
                "imgUrl": imgUrl,
                "lastChapter": {
                    "title": lastChapter.text,
                    "url": lastChapter.get("href")
                }
            }
        )

    return novels


def getChapter(chapterUrl: str):
    page = bsoup(requests.get(chapterUrl).content, "html.parser")
    title = page.find(class_="name_chapter").text
    content = list()
    for paragraph in page.find("div", class_="vung_doc").find_all("p"):
        if paragraph.text not in ["", "\n"]:
            content.append(paragraph.text)

    return {"title": title, "content": content}


def getChapterCount(chapterUrl: str):
    page = bsoup(requests.get(chapterUrl).content, "html.parser")
    return len(page.find("div", class_="chapter-list").find_all("div", class_="row"))
