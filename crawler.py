import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet


def download_archive(url: str):
    r = requests.get(url)


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

    print(wpm_archive)
    print(*wpm_archive, sep="\n")
