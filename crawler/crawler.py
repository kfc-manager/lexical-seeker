import requests
from typing import Iterator, Tuple
from bs4 import BeautifulSoup
from adapter.database import Database
from adapter.queue import Queue
from adapter.logger import Logger


class WikiCrawler:
    def __init__(self, database: Database, queue: Queue):
        self._base_url = "https://en.wikipedia.org"
        self._path = "/wiki/"
        self._database = database
        self._queue = queue
        self._logger = Logger("crawler")

    def visit(self, topic: str):
        link = self._base_url + self._path + topic
        try:
            if self._database.is_visited(link):
                return
            self._queue.send(link)
            self._database.insert_visit(link)
        except Exception as e:
            self._logger.log(f"exception in visit: {e}")

    def crawl(self) -> Iterator[Tuple[str, str]]:
        try:
            for message in self._queue.consume():
                response = requests.get(
                    message,
                    headers={
                        "User-Agent": "example.com info@example.com",
                        "Accept": "*/*",
                        "Connection": "keep-alive",
                    },
                )
                if not response.ok:
                    self._logger.log(f"unsuccessful api call: {response.text}")
                    continue
                soup = BeautifulSoup(response.text, "html.parser")
                links = [a["href"] for a in soup.find_all("a", href=True)]
                for link in links:
                    if not link.startswith(self._path):
                        continue
                    self.visit(link.removeprefix(self._path))
                yield (message, response.text)
        except Exception as e:
            self._logger.log(f"exception consuming queue: {e}")
