import sys
import re
import requests
from bs4 import BeautifulSoup
from collections import deque
import pickle
from time import sleep


def get_url_text(url): 
    response = requests.get(url, allow_redirects=False)
    if response.ok:
        return response.text
    else:
        return ""


class Article:
    def contain(self, value):
        return self.content.find(value) != 0

    def __init__(self, domain, topic, soup):
        tag_a = soup.find("h4", {"class":"title"}).a
        href = tag_a.get("href")
        self.valid = False
        if href.find(topic) == 0:
            self.valid = True
            self.ref = domain + href
            self.title = tag_a.get_text()
            self.annotation = soup.find("p", {"class":"dek"}).a.get_text()
            self.__get_data_from_article(self.ref)

    def __get_data_from_article(self, url):
        text = get_url_text(url)
        soup = BeautifulSoup(text, "html.parser")
        refs = soup.find("div", {"class":"author-byline"}).find_all("a")
        self.autors = []
        for ref in refs:
            if ref.get("href").find("/person") == 0:
                self.autors.append(ref.get_text())

        self.content = soup.find("div", {"class":"article-body"}).get_text().lower()

    def __str__(self):
        return "title: {title}\nref: {ref}\nautors: {autors}\nannotation: {annotation}\n".format(**self.__dict__)

cache = dict()
cache_file = "cache_lab2.pickle"
def load_cache():
    print("start cache load")
    global cache
    try:
        with open(cache_file, "rb") as f:
            cache = pickle.load(f)
    except:
        pass
    print("end cache load")


def save_cache():
    print("start cache save")
    with open(cache_file, "wb") as f:
        pickle.dump(cache, f)
    print("end cache save")


if __name__ == "__main__":
    load_cache()

    try:
        while True:
            domain = "https://www.foxnews.com"
            topic = "/politics"
            text = get_url_text(domain + topic)
            soup = BeautifulSoup(text, "html.parser")
            articles = soup.find("div", {"class":"content article-list"}).find_all("article")
            for article_soup in articles:
                article = Article(domain, topic, article_soup)
                if article.valid:
                    contain = article.contain("democrat")
                    contain = contain or article.contain("republican")
                    contain = contain or article.contain("gop")
                    if contain:
                        cache[article.title] = article
                        some = article
            save_cache()
            sleep(10 * 60)
    except requests.exceptions.RequestException as req_err:
        print("Error url or connection:", req_err)
    except Exception as e:
        print(e)
    except:
        pass

    for article in cache.values():
        print(article)

    save_cache()

