#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: lrcge.py


import re
from urllib.parse import quote
import requests

class lrcgc:
    def __init__(self, title, artist):
        self.baseUrl = "https://so.lrcgc.com/?q="

        self.url = self.baseUrl + quote(title) + "+" + quote(artist)
        print(self.url)

    def search(self):
        try:
            res = requests.get(self.url)
            html = res.text
            res.close()
        except:
            return False

        a = re.findall(r"http://www.lrcgc.com/lyric-.*?</a>", html)
        resultList = []
        for i in a:
            url, ra1, ra2, keywords = i.split("\"")
            keywords = keywords.replace("<em>", "").replace("</em>", "").replace("</a>", "").replace(">", "")
            resultList.append([url, keywords])
        return resultList

    def getLrcUrl(self, url):
        try:
            res = requests.get(url)
            html = res.text
            res.close()
        except:
            return False

        l = re.findall(r"data-swiftype-type=\"text\".*?</p>", html)
        if len(l) == 0:
            return False
        else:
            lyrics = l[0].replace('data-swiftype-type="text">', "").replace("</p>", "").strip()
            return lyrics


if __name__ == "__main__":
    a = lrcgc("陈奕迅", "十年")
    r = a.search()
    print(r)
    l = a.getLrcUrl(r[0][0])
    print(l)
