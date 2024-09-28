#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: bing_5nd.py


import requests, re
from urllib.parse import quote


class bing_5nd:

    def __init__(self):
        self.baseurl = "https://cn.bing.com/search?q="


    def getLrc(self, title, artist):
        extendurl = f"{quote(title)}+{quote(artist)}+lrc%E6%AD%8C%E8%AF%8D"
        url = self.baseurl + extendurl
        res = requests.get(url)
        html = res.text
        res.close()
        l = list(set(re.findall(r"http://www.5nd.com/gecilrc/.*?htm", html)))
        if not l:
            return None
        res = requests.get(l[0])
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
    print(a.getLrc("月光爱人", "李玟"))
