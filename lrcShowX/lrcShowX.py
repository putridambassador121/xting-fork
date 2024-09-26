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
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWordWrapMode(QTextOption.WrapMode.NoWrap)

        self.timer = QTimer()
        self.animateTimer = QTimer()

        self.readParameters()

        self.initColor()

        self.margin = QFontMetrics(self.font()).height() + self.lineMargin
        self.nullNum = int(self.viewport().height() / self.margin)

        self.showInfo("No music is playing")

        self.parent.parent.musicEngine.musicEquipment.playbackStateChanged.connect(self.playbackStateChanged_)
        self.timer.timeout.connect(self.scroll)
        self.animateTimer.timeout.connect(self.animate)

    def playbackStateChanged_(self, state):
        sv = state.value
        if sv == 0: # stoped state
            if self.timer.isActive():
                self.timer.stop()
            if self.animateTimer.isActive():
                self.animateTimer.stop()
            self.showInfo("No music is playing")
        elif sv == 1: # playing state
            # search local
            # seach engines

            p = lrcParser("lrcShowX/b.lrc")
            self.lrcScheduleList, self.offset = p.parse()
            self.showLrc()

            self.locateCurrentTag()
            self.scrolLToCurrent()
        else:  # paused state
            self.locateCurrentTag()
            self.scrolLToCurrent()

    def locateCurrentTag(self):
        self.trackPos = self.parent.parent.musicEngine.getPositionInms()
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


    def scrolLToCurrent(self):
        duaration = self.lrcScheduleList[self.currentTag][2]
        self.verticalScrollBar().setValue(self.currentTag * self.margin)
        for count in range(0, self.topMarginLines + self.currentTag - 1):
            self.moveCursor(QTextCursor.MoveOperation.Down)
        self.highLightCurrentLine()
        if duaration > self.offset:
            self.timer.start(duaration - self.offset)
        else:
            print("invalid offset, ignore!")
            self.timer.start(duaration)

    def scroll(self):
        duaration = self.lrcScheduleList[self.currentTag][2]
        if duaration < 0:
            pass
        else:
            if duaration < 700:
                self.verticalScrollBar().setValue(self.currentTag * self.margin)
            else:
                self.animateStartTag = self.currentTag
                self.animate()
            self.timer.start(duaration)
            self.currentTag += 1
            self.highLightCurrentLine()

    def animate(self):
        dis = int(self.margin / 5)
        pos = self.verticalScrollBar().value()
        if pos + dis < self.animateStartTag * self.margin:
            self.verticalScrollBar().setValue(pos + dis)
            self.animateTimer.start(100)
        else:
            self.verticalScrollBar().setValue(self.animateStartTag * self.margin)





    def highLightCurrentLine(self):
        self.moveCursor(QTextCursor.MoveOperation.StartOfLine)
        self.moveCursor(QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.KeepAnchor)


    def readParameters(self):
        self.lineMargin = self.parent.parent.parameter.lineMargin
        self.topMarginLines = self.parent.parent.parameter.topMarginLines
        self.backGroundColor = QColor(self.parent.parent.parameter.backGroundColor)
        self.foreGroundColor = QColor(self.parent.parent.parameter.foreGroundColor)
        self.highLightColor = QColor(self.parent.parent.parameter.highLightColor)
        self.lrcLocalSearchPath = self.parent.parent.parameter.lrcLocalSearchPath
        self.lrcLocalSavePath = self.parent.parent.parameter.lrcLocalSavePath

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

    def initColor(self):
        pl = QPalette()
        pl.setColor(QPalette.ColorRole.Window, self.backGroundColor)
        pl.setColor(QPalette.ColorRole.Base, self.backGroundColor)
        pl.setColor(QPalette.ColorRole.Text, self.foreGroundColor)
        pl.setColor(QPalette.ColorRole.Highlight, self.backGroundColor)
        pl.setColor(QPalette.ColorRole.HighlightedText, self.highLightColor)
        self.setPalette(pl)
        self.update()

    # def resizeEvent(self, e):
    #     self.nullNum = self.height() / self.margin

