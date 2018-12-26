#!/usr/bin/python3

import sys
import re
import requests
from bs4 import BeautifulSoup
from collections import deque
import pickle

def get_url_text(url):
    response = requests.get(url, allow_redirects=False)
    if response.ok:
        return response.text
    else:
        return ""


def make_wiki_url(name, prefix = "https://en.wikipedia.org/wiki/"):
    return prefix + name

    
class WikiPage:
    def __init__(self, name):
        self.index = None

        text = get_url_text(make_wiki_url(name))
        soup = BeautifulSoup(text, "html.parser")

        self.canonical_link = soup.find("link", rel="canonical").get("href")

        body_content = soup.find(id="bodyContent")
        self.ref = []
        for link in body_content.find_all("a"):
            href = link.get("href")
            if href and href.find("/wiki/") is 0 and not re.search("/wiki/.*:.*", href):
                self.ref.append(href[6:])    


cache = dict()
cache_file = "cache.pickle"
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

        
page_for_save = 20
page_before_save = page_for_save
def get_wikipage(name):
    global page_before_save
    from_cache = cache.get(name)
    if from_cache: 
        return from_cache
    else:
        page = WikiPage(name)
        cache[name] = page
        if not page_before_save:
            save_cache()
            page_before_save = page_for_save
        else:
            page_before_save -= 1
        return page



def bfs(start, end, max_step=10):
    start_page = get_wikipage(start)
    end_page = get_wikipage(end)
    stop = end_page.canonical_link 

    if start_page.canonical_link == stop:
        return [stop]

    found = False
    used = {start_page.canonical_link: None}
    q = deque()
    start_page.index = 0
    q.append(start_page)

    while q and not found:
        u = q.popleft()
        for name in u.ref:
            v = get_wikipage(name)
            if not v.canonical_link in used:
                v.index = u.index + 1
                used[v.canonical_link] = u.canonical_link

                if v.canonical_link == stop:
                    found = True
                    break

                if v.index < max_step:
                    q.append(v)

    if not found:
        return []

    current = stop
    result = [stop]

    while current:
        current = used[current]
        if current:
            result.append(current)

    result.reverse()
    return result

        
if __name__ == "__main__":
    try:
        start, end = sys.argv[1:3]
    except:
        print("Not valid argument")
        exit(1)

    load_cache()

    try:
        print("start find first path") 
        first = bfs(start, end) 
        print("first:", first)
        print("start find second path") 
        second = bfs(end, start)
        print("second:", second)
    except requests.exceptions.RequestException as req_err:
        print("Error url or connection:", req_err)
    except:
        pass

    save_cache()

