#!/usr/bin/python
#matt garrett
#cse 417

#This file contains code to compare signatures stored in a .csv file
#Signatures need to be in a very special format, which I won't describe
#here because this code will never be used again.  Sadface.jpg
import sys
import urllib2
from bs4 import BeautifulSoup
import re

#returns the base angle difference between a and b
# returns 0 if they point the same way
# returns 1 if they differ by pi/4
# returns 2 if they differ by pi/2
# returns 4 if they differ by more than pi/2

def explore(url, depth, stop, documents):
    if (depth <= stop):
        fullUrl = "http://en.wikipedia.org" + url
        request = urllib2.Request(fullUrl, headers={"User-Agent" : "Superman"})
        socket  = urllib2.urlopen(request)
        page    = socket.read()
        socket.close()
        page    = re.sub('id="References.*', '', page)
        soup    = BeautifulSoup(page)
        article = soup.find("div", {"id" : "mw-content-text"})
        for link in article.find_all("a", {"href" : re.compile("/wiki/.*")}):
            documents.add(link.get("href"))
            explore(link.get("href"), depth + 1, stop, documents)
    else:
        documents.add(url)

#yeah I'm used to java, learning python is hard
def main():
    if (len(sys.argv) < 3):
        showUsage()
    else:
        url = sys.argv[1]
        stop = int(sys.argv[2])
        documents = set()
        explore(url, 0, stop, documents)
    for doc in documents:
        print doc
main()
