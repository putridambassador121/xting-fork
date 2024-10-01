#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: lrcParser.py


import os, re

class lrcParser:

    def __init__(self, lrcfile, isFile = True, lrcFrom = None):
        self.isFile = isFile

        self.lrcfile = lrcfile
        if isFile:
            l = lrcfile
        elif (not isFile) and lrcFrom:
            l = lrcFrom
        else:
            l = "online"
        self.syncedLyrics = syncedLyrics(l)



    def parse(self):
        if not self.isFile:
            lineList = self.lrcfile.split("\n")
        else:
            with open(self.lrcfile, "r") as f:
                lineList = f.readlines()
        lineList = list(map(lambda x: x.strip().replace("<br />", ""), lineList))
        self.syncedLyrics.lrcWithTag = "\n".join(lineList)

        offset = 0
        for y in lineList:
            offsetTag = re.search(r'\[offset:(.*?)\]', y)
            if offsetTag:
                offset = int(offsetTag.group(1).strip())
                haveOffsetTag = True
                break
        self.syncedLyrics.offset = offset

        td = dict()
        for i in lineList:
            tags = re.findall(r"\[\d\d:\d\d.*?\]", i)
            if not tags:
                continue
            text = i.split("]")[-1]
            for j in tags:
                j = self.tagToms(j) - offset
                td[j] = text
        tl = list(td.keys())
        tl.sort()
        tlCopy = tl.copy()
        tl.append(0)
        m = [0] + tlCopy
        dl = list(map(lambda x: x[0] - x[1], zip(tl, m)))
        lyrics = []
        o = 1
        plain = ""
        for k in tlCopy:
            lyrics.append([k, td[k], dl[o]])
            plain += td[k] + "\n"
            o += 1
        readyLine = [[0, "", lyrics[0][0]]]
        self.syncedLyrics.scheduledLrc = readyLine + lyrics  # [[tag1, lyrics1, duration1], [tag2, lyrics2, duration2], .......]
        self.syncedLyrics.lrcWithoutTag = plain

        return self.syncedLyrics


    def tagToms(self, tag):
        tag = tag.replace("[", "").replace("]", "")
        m, s = tag.split(":", 1)
        s1 = int(float(s))
        s2 = round((float(s) - s1) * 1000)
        return int(m) * 60000 + s1 * 1000 + s2

class syncedLyrics:

    def __init__(self, lrcFrom = "local"):
        self.lrcWithTag = None
        self.lrcWithoutTag = None
        self.scheduledLrc = None
        self.lrcFrom = lrcFrom
        self.offset = 0

if __name__ == "__main__":
    p = lrcParser("b.lrc")
    l = p.parse()
    print(l)
    print(l[2][1])
