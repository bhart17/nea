from typing import List
import requests
import xml.etree.ElementTree
from enum import Enum

from requests.models import Response


class RssStatus(Enum):
    GOOD = ""
    UNFETCHABLE = "The requested resource could not be fetched"
    INVALID_TAG = "The requested tags are not present on the resource"
    NULL = None


class RssFeed:
    def __init__(self, url: str) -> None:
        self.url = url
        self.__status = RssStatus.NULL
        self.refresh()

    def __make_request(self, url: str) -> requests.Response:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                if "Content-Type" in response.headers:
                    if "xml" in response.headers["Content-Type"]:
                        return response
            return None
        except (requests.ConnectionError, requests.Timeout,
                requests.TooManyRedirects, requests.RequestException):
            return None

    def __parse_response(self, response: Response):
        if response != None:
            return RssStatus.GOOD, [{
                tag: item.find(tag).text
                for tag in [child.tag for child in item]
            } for item in xml.etree.ElementTree.fromstring(response.text).iter(
                "item")]
        return RssStatus.UNFETCHABLE, []

    def get_items(self, tags: list[str] = [], max_items: int = -1) -> list:
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

    def refresh(self):
        response = self.__make_request(self.url)

        self.__status, self.__items = self.__parse_response(response)

    def get_status(self):
        return self.__status


if __name__ == "__main__":
    # basic test
    r = RssFeed("https://lorem-rss.herokuapp.com/feed")
    print(r.get_items())
