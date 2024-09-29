#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: lrc99.py

import re
from urllib.parse import quote
import requests


class lrc99:
    def __init__(self):
        self.baseurl = 'http://www.lrc99.com/'

    def search(self, title, artist):
        url = self.baseurl + f"gs_{quote(artist)}.html"
        u = self.getLrcPage(url, title, True)
        if u:
            return self.getLrc(u)

        else:
            for i in range(0, self.totalPage):
                j = i + 2
                pu = url + f"?name={quote(artist)}&page={j}"
                u = self.getLrcPage(pu, title)
                if u:
                    return self.getLrc(u)
            return False

    def getLrcPage(self, url, title, page = False):
        res = requests.get(url)
        t = res.text
        res.close()
        b = re.search(f"geci_.*?html\">{title}", t)
        if page:
            p = re.findall("page=", t)
            self.totalPage = len(p)
        if b:
            u = self.baseurl + b.group(0).split('"')[0]
            return u
        else:
            return False

    def getLrc(self, url):
        res = requests.get(url)
        t = res.text
        res.close()
        b = re.search(r'<article id="lrc">.*?</article>', t, re.S).group(0)
        lrc = b.split("</h3>")[-1].strip().replace("</article>", "")
        return lrc


if __name__ == "__main__":
    p = lrc99()
    l = p.search("过完冬季", "李玟")
    print(l)



