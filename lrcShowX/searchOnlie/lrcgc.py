#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: lrcge.py


import re
from urllib.parse import quote
import requests

class lrcgc:
    def __init__(self):
        self.baseurl = "https://so.lrcgc.com/?q="

    def search(self, title, artist):
        url = self.baseurl + quote(title) + "+" + quote(artist)
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
    a = lrcgc()
    r = a.search("陈奕迅", "十年")
    print(r)
    l = a.getLrcUrl(r[0][0])
    print(l)
