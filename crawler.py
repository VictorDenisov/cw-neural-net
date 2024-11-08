import urllib.request

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet


def download_archive(url: str):
    url = "http://www.arrl.org/5-wpm-code-archive"
    r = requests.get(url)

    soup = BeautifulSoup(r.content)
    print(soup.prettify())
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
        print(f"{archive_links[2 * i]}, {archive_links[2 * i + 1]}")
        urllib.request.urlretrieve(
            "http://www.arrl.org/" + archive_links[2 * i].get("href"), f"{i}.mp3"
        )
        urllib.request.urlretrieve(
            "http://www.arrl.org/" + archive_links[2 * i + 1].get("href"), f"{i}.txt"
        )

    print(*archive_links, sep="\n")


def main():
    start_page = "http://www.arrl.org/code-practice-files"

    r = requests.get(start_page)

    print(r.content)

    soup = BeautifulSoup(r.content)
    print(soup)
    links = soup.find_all("a")
    print(*links, sep="\n")
    print(type(links))
    link = links[15]
    print(type(link))
    print(link.get("href"))
    print("code-archive" in link.get("href"))

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

    print(wpm_archive)
    print(*wpm_archive, sep="\n")
