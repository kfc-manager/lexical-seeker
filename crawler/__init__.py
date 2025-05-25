import os
import time
from typing import List
from adapter.storage import Storage
from adapter.database import Database
from adapter.queue import Queue
from adapter.logger import Logger
from crawler.crawler import WikiCrawler
from crawler.parser import Parser


def crawl(start: str, tokens: List[str]):
    storage = Storage("./data")
    database = Database(
        db_host=os.getenv("DB_HOST"),
        db_port=os.getenv("DB_PORT"),
        db_name=os.getenv("DB_NAME"),
        db_user=os.getenv("DB_USER"),
        db_pass=os.getenv("DB_PASS"),
    )
    queue = Queue(
        queue_host=os.getenv("QUEUE_HOST"),
        queue_name=os.getenv("QUEUE_NAME"),
    )
    logger = Logger("storage")
    crawler = WikiCrawler(database=database, queue=queue)
    parser = Parser(strip=tokens)
    crawler.visit(start)
    time.sleep(10)
    for link, article in crawler.crawl():
        time.sleep(0.1)
        try:
            text = parser.parse(article)
            hash = parser.hash(text)
            file_name = f"{hash}.txt"
            size = len(text.encode("utf-8"))
            storage.put(file_name, text)
            database.insert_metadata(link, size, file_name)
        except Exception as e:
            logger.log(f"exception storing file {e}")
