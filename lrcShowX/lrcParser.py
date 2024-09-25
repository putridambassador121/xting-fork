#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: lrcParser.py


import os, re

class lrcParser:

    def __init__(self, lrcfile):
        self.lrcfile = lrcfile


    def parse(self):
        with open(self.lrcfile, "r") as f:
            lineList = f.readlines()

        td = dict()
        for i in lineList:
            tags = re.findall(r"\[\d\d:\d\d.*?\]", i)
            if not tags:
                continue
            text = i.split("]")[-1].strip()
            for j in tags:
                j = self.tagToms(j)
                td[j] = text
        tl = list(td.keys())
        tl.sort()
        tlCopy = tl.copy()
        tl.append(0)
        m = [0] + tlCopy
        dl = list(map(lambda x: x[0] - x[1], zip(tl, m)))
        lyrics = []
        o = 1
        for k in tlCopy:
            lyrics.append([k, td[k], dl[o]])
            o += 1
        return lyrics   # [[tag1, lyrics1, duaration1], [tag2, lyrics2, duaration2], .......]


    def tagToms(self, tag):
        tag = tag.replace("[", "").replace("]", "")
        m, s = tag.split(":", 1)
        s1 = int(float(s))
        s2 = round((float(s) - s1) * 1000)
        return int(m) * 60000 + s1 * 1000 + s2

if __name__ == "__main__":
    p = lrcParser("b.lrc")
    l = p.parse()
    print(l)
    print(l[2][1])
