import logging
import os
import random
import urllib.request
from urllib.parse import urlparse

import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet

logger = logging.getLogger(__name__)


def download_archive(url: str):
    logger.info(f"Downloading url: {url}")
    r = requests.get(url)

    soup = BeautifulSoup(r.content)
    links = soup.find_all("a")

    archive_links = list(
        filter(
            lambda x: x.has_attr("href")
            and ("mp3" in x.get("href") or "txt" in x.get("href")),
            links,
        )
    )
    i = 0

    for i in range(len(archive_links) // 2):
        if not archive_links[2 * i].get("href").endswith("mp3"):
            raise RuntimeError("Expected mp3 on odd positions")
        print(
            f"{archive_links[2 * i].get("href")}, {archive_links[2 * i + 1].get("href")}"
        )

        url = "http://www.arrl.org/" + archive_links[2 * i].get("href")
        parsed_url = urlparse(url)
        filename = os.path.join("data", os.path.basename(parsed_url.path))

        urllib.request.urlretrieve(url, f"{filename}")

        url = "http://www.arrl.org/" + archive_links[2 * i + 1].get("href")
        parsed_url = urlparse(url)
        filename = os.path.join("data", os.path.basename(parsed_url.path))
        urllib.request.urlretrieve(url, f"{filename}")


def main():
    logger.info("Downloading top level list")
    start_page = "http://www.arrl.org/code-practice-files"

    r = requests.get(start_page)

    soup = BeautifulSoup(r.content)
    links = soup.find_all("a")

    wpm_archive = map(
        lambda x: x["href"],
        filter(
            lambda x: "code-archive" in x.get("href"),
            filter(lambda x: x.has_attr("href"), links),
        ),
    )
    for l in wpm_archive:
        if "http" in l:
            download_archive(l)


def setup_logging():
    # create logger
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


if __name__ == "__main__":
    setup_logging()
    main()
