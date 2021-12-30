import requests
import xml.etree.ElementTree
from enum import Enum


class RssStatus(Enum):
    GOOD = ""
    UNFETCHABLE = "The requested resource could not be fetched"
    INVALID_TAG = "The requested tags are not present on the resource"


class RssFeed:
    def __init__(self, url: str) -> None:

        self.__items = []

        response = self.__make_request(url)
        if response != None:
            self.__status = RssStatus.GOOD
            self.__items = [{
                tag: item.find(tag).text
                for tag in [child.tag for child in item]
            } for item in xml.etree.ElementTree.fromstring(response.text).iter(
                "item")]
        else:
            self.__status = RssStatus.UNFETCHABLE

    def __make_request(self, url: str) -> requests.Response:
        response = requests.get(url)
        if response.status_code == 200:
            if "Content-Type" in response.headers:
                if "text/xml" in response.headers["Content-Type"]:
                    return response
        return None

    def get_items(self, tags: list[str] = [], max_items: int = -1) -> tuple:
        if max_items != -1 and len(self.__items) > max_items:
            items = self.__items[:max_items]
        else:
            items = self.__items[:]

        if tags == []:
            return items

        for item in items:
            for tag in tags:
                if tag not in item.keys():
                    return RssStatus.INVALID_TAG

        return [{tag: item[tag] for tag in tags} for item in items]

    def get_status(self):
        return self.__status


if __name__ == "__main__":
    r = RssFeed("https://feeds.skynews.com/feeds/rss/home.xml")
    print(r.get_items(["title", "description", "pubDate"], 5))
