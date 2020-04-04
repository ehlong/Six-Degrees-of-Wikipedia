# Elliott Long
# 6 Degrees of Star Wars (or anything on Wikipedia)

from bs4 import BeautifulSoup
import requests
import re
from collections import deque


# used to generate first random url
def get_random_page_url():
    rand = requests.get('https://en.wikipedia.org/wiki/Special:Random')
    return rand.url


def filter_links(href):
    if href:
        if re.compile('^/wiki/').search(href):
            if not re.compile('/\w+:').search(href):
                if not re.compile('#').search(href):
                    return True
    return False


def page_title(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    pageTitle = page.find('h1', id="firstHeading").string
    return pageTitle

def bfs(url, depth, visited, path, flag):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    pageTitle = page.find('h1', id="firstHeading").string
    mainBody = page.find(id="bodyContent")
    holder = {url: pageTitle}
    q = deque([])
    for link in mainBody.find_all('a', href=filter_links):
        links = link.get('href')
        links = "https://en.wikipedia.org" + links
        q.append(links)                 # creates usable deque of links
    p = q.copy()
    if depth >= 7:                      # if too deep, go back
        return path
    visited.update(holder)              # add current url to visited list
    path.append(url)                    # add current url to the path
    if 'https://en.wikipedia.org/wiki/Star_Wars' in path:
        return path                     # return the path if SW was found
    for i in range(len(q)):                     # for each element of q, run a search
        test = p.popleft()
        if test == 'https://en.wikipedia.org/wiki/Star_Wars':
            path = bfs(test, depth, visited, path, 1)
            return path
    if flag == 1:                       # flag to control if search or new depth
        path.pop()
        return path
    p = q.copy()
    for i in range(len(q)):
        if 'https://en.wikipedia.org/wiki/Star_Wars' in path:
            break                       # if SW in the path, search over
        if len(p) != 0:                 # protection from empty pop
            jump = p.popleft()
        for j in range(len(q) - 1):     # len - 1 because len gave me an error
            if jump in visited and len(p) != 0:
                jump = p.popleft()      # pop another if already visited
            else:
                break
        if jump in visited:
            break                       # if visited but can't pop, move on
        path = bfs(jump, depth, visited, path, 1)
    if 'https://en.wikipedia.org/wiki/Star_Wars' not in path:
        jump = q.popleft()
        for j in range(len(q)):
            if jump in visited:
                jump = q.popleft()
            else:
                break
        path = bfs(jump, depth + 1, visited, path, 0)   # same as above, but depth+1
    return path                                         # makes it a new depth to check


urlie = get_random_page_url()
visit = {}
pathie = deque([])
deep = 0
final = bfs(urlie, deep, visit, pathie, 0)
i = 0
hold = final.copy()
if 'https://en.wikipedia.org/wiki/Star_Wars' in final:
    for element in final:
        x = hold.popleft()
        y = page_title(x)
        print("   " * i + y + " (" + x + ")")
        i = i + 1
else:
    x = hold.popleft()
    y = page_title(x)
    print("Unable to find path from " + y + " to Star Wars")
