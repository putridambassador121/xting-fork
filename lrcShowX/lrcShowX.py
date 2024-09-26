#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: lrcShow-X.py

import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from lrcShowX.lrcParser import lrcParser


class lrcShowX(QTextBrowser):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.timer = QTimer()

        self.readParameters()

        self.margin = QFontMetrics(self.font()).height() + self.lineMargin
        self.nullNum = int(self.viewport().height() / self.margin)

        self.showInfo("No music is playing")

        self.parent.parent.musicEngine.musicEquipment.playbackStateChanged.connect(self.playbackStateChanged_)
        self.timer.timeout.connect(self.scroll)

    def playbackStateChanged_(self, state):
        sv = state.value
        if sv == 0: # stoped state
            if self.timer.isActive():
                self.timer.stop()
            self.showInfo("No music is playing")
        elif sv == 1: # playing state
            # search local
            # seach engines

            p = lrcParser("lrcShowX/b.lrc")
            self.lrcScheduleList = p.parse()
            self.showLrc()

            self.locateCurrentTag()
            self.scrolLToCurrent()
        else:  # paused state
            self.locateCurrentTag()
            self.scrolLToCurrent()

    def locateCurrentTag(self):
        self.trackPos = self.parent.parent.musicEngine.getPositionInms()
        print(f"current position is: {self.trackPos}")
        n = 0
        for i in self.lrcScheduleList:
            if self.trackPos < i[0]:
                break
            elif self.trackPos == i[0]:
                n += 1
                break
            else:
                n += 1
        self.currentTag = n
        print(n)


    def scrolLToCurrent(self):
        duaration = self.lrcScheduleList[self.currentTag][2]
        self.verticalScrollBar().setValue(self.currentTag * self.margin)
        self.timer.start(duaration)

    def scroll(self):
        duaration = self.lrcScheduleList[self.currentTag][2]
        if duaration < 0:
            pass
        else:
            self.verticalScrollBar().setValue(self.currentTag * self.margin)
            self.timer.start(duaration)
            self.currentTag += 1


    def readParameters(self):
        self.lineMargin = self.parent.parent.parameter.lineMargin
        self.topMarginLines = self.parent.parent.parameter.topMarginLines

    def getMargin(self):
        self.margin = self.fontMetrics().height() + self.lineMargin

    def showInfo(self, t):
        l = self.formartInfo(t)
        self.setHtml(l)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def formartInfo(self, text):
        j =  f'<p align="center" style=" margin-top:{self.lineMargin}px; margin-bottom:{self.lineMargin}px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">&nbsp;</p>'
        nullLines = self.topMarginLines * j
        t = f'<p align="center" style=" margin-top:{self.lineMargin}px; margin-bottom:{self.lineMargin}px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">{text}</p>'
        return nullLines + t

    def showLrc(self):
        l = self.formartLrc()
        self.setHtml(l)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def formartLrc(self):
        if not self.lrcScheduleList:
            self.showInfo("Can not parse the LRC file")
        else:
            j =  f'<p align="center" style=" margin-top:{self.lineMargin}px; margin-bottom:{self.lineMargin}px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">&nbsp;</p>'
            nullLines = self.topMarginLines * j
            context = ""
            for i in self.lrcScheduleList:
                if i[1] == "":
                    t = f'<p align="center" style=" margin-top:{self.lineMargin}px; margin-bottom:{self.lineMargin}px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">&nbsp;</p>'
                else:
                    t = f'<p align="center" style=" margin-top:{self.lineMargin}px; margin-bottom:{self.lineMargin}px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">{i[1]}</p>'

                context += t
            co = nullLines + context + 50 * j + '<p align="center">&nbsp;</p>'
            return co

    # def resizeEvent(self, e):
    #     self.nullNum = self.height() / self.margin

