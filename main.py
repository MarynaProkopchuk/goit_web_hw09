import requests
from bs4 import BeautifulSoup
import json
import lxml

BASE_URL = "http://quotes.toscrape.com"
urls = [BASE_URL]
quotes = []
authors = []
authors_urls = []


def get_urls():
    url = "/page/1/"
    while url:
        response = requests.get(BASE_URL + url)
        soup = BeautifulSoup(response.text, "lxml")

        next_page = soup.select_one("li.next > a")
        if next_page:
            url = next_page["href"]
            urls.append(BASE_URL + url)
        else:
            url = None
    return urls


def get_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    for q in soup.select(".quote"):
        tags = [tag.get_text() for tag in q.select(".tag")]
        author = q.select_one(".author").get_text()
        quote = q.select_one(".text").get_text()
        author_url = BASE_URL + q.select_one("span a")["href"]

        quotes.append({"tags": tags, "author": author, "quotes": quote})
        authors_urls.append(author_url)


def get_authors(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    fullname = soup.select_one(".author-title").get_text()
    born_date = soup.select_one(".author-born-date").get_text()
    born_location = soup.select_one(".author-born-location").get_text()
    description = soup.select_one(".author-description").get_text().strip()
    authors.append(
        {
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description,
        }
    )


def main(urls):
    for url in urls:
        get_quotes(url)
    for url in authors_urls:
        get_authors(url)
    return quotes, authors


if __name__ == "__main__":
    main(get_urls())
    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)
