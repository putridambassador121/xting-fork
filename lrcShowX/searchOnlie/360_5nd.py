#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: bing_5nd.py


import requests, re
from urllib.parse import quote


class bing_5nd:

    def __init__(self):
        self.baseurl = "https://www.so.com/s?q="


    def getLrc(self, title, artist):
        extendurl = f"{quote(title)}+{quote(artist)}+lrc%E6%AD%8C%E8%AF%8D"
        url = self.baseurl + extendurl
        userAgent = "Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0"
        headers = {"User-Agent": userAgent}
        print(url)
        res = requests.get(url, headers)
        html = res.text
        #print(html)
        res.close()
        l = list(set(re.findall(r"http://www.5nd.com/gecilrc/.*?htm", html)))
        print(l)
        if not l:
            return None
        res = requests.get(l[0], headers)
        res.encoding = "gb2312"
        t = res.text
        res.close()
        lrcList = re.findall(r"</label></li><li>.*?</li>", t)
        if lrcList:
            lrc = lrcList[0].replace("</label></li><li>", "").replace("</li>", "")
            return lrc
        else:
            return None






if __name__ == "__main__":
    a = bing_5nd()
    print(a.getLrc("陈奕迅", "十年"))
