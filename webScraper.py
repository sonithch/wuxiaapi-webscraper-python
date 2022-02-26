import requests
import concurrent.futures
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
        chapters = 0

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(getChapterCount, url)
            chapters = future.result()

        imgUrl = metadata.find("img").get("src")
        novels.append(
            {
                "title": title,
                "url": url,
                "imgUrl": imgUrl,
                "chapters": chapters
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


def getTitles(url: str):
    response = list()
    try:
        page = bsoup(requests.get(url).content, "html.parser")
        titleRows = page.find("div", class_="chapter-list").find_all("div", class_="row")
        for row in titleRows:
            metadata = row.find("a")
            response.insert(0, {
                "title": metadata.text.strip(),
                "url": metadata.get("href")
            })

    except Exception as e:
        print(e)

    return response


def getChapterCount(chapterUrl: str):
    try:
        page = bsoup(requests.get(chapterUrl).content, "html.parser")
        return len(page.find("div", class_="chapter-list").find_all("div", class_="row"))
    except Exception as e:
        print(e)
        return 0
