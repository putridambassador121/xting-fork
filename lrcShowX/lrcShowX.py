#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: lrcShow-X.py

import os, glob
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
        self.parent.parent.positionChanged.connect(self.trackPositionChanged)
        self.timer.timeout.connect(self.scroll)
        self.animateTimer.timeout.connect(self.animate)

    def playbackStateChanged_(self, state):
        sv = state.value
        if sv == 0: # stoped state
            if self.timer.isActive():
                self.timer.stop()
            if self.animateTimer.isActive():
                self.animateTimer.stop()
            self.lrcScheduleList = None
            self.currentTag = None
            self.showInfo("No music is playing")

        elif sv == 1: # playing state
            fi = self.searchLocal()
            if fi:
                p = lrcParser(fi)
                self.lrcScheduleList = p.parse()
                self.showLrc()
                self.locateCurrentTag()
                self.scrolLToCurrent()
            else:
                self.lrcScheduleList = None
                self.currentTag = None
                self.showInfo("No local lrc file found")
                # seach engines


        else:  # paused state
            self.locateCurrentTag()
            self.scrolLToCurrent()

    def searchLocal(self):
        title = self.parent.parent.currentTrack.trackTitle
        artist = self.parent.parent.currentTrack.trackArtist
        if title == "unknow":
            title = ""
        else:
            title = title.lower()
        if artist == "unknow":
            artist == ""
        else:
            artist = artist.lower()
        if (not title) and (not artist):
            return False

        for i in glob.glob(os.path.join(self.lrcLocalPath, "*.lrc")):
            if title in i.lower() and artist in i.lower():
                return i
        return False


    def trackPositionChanged(self):
        if not self.lrcScheduleList:
            return

        if self.timer.isActive():
            self.timer.stop()
        if self.animateTimer.isActive():
            self.animateTimer.stop()
        self.showLrc()
        self.locateCurrentTag()
        self.scrolLToCurrent()

    def locateCurrentTag(self):
        self.trackPos = self.parent.parent.musicEngine.getPosition()
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
        for count in range(0, self.topMarginLines + self.currentTag - 1):
            self.moveCursor(QTextCursor.MoveOperation.Down)
        self.highLightCurrentLine()
        duaration = self.lrcScheduleList[self.currentTag][0] - self.trackPos
        self.verticalScrollBar().setValue((self.currentTag - 1) * self.margin)
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
        self.backGroundColor = self.parent.parent.parameter.backGroundColor
        self.foreGroundColor = self.parent.parent.parameter.foreGroundColor
        self.highLightColor = self.parent.parent.parameter.highLightColor
        self.lrcLocalPath = self.parent.parent.parameter.lrcLocalPath

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
        pl.setColor(QPalette.ColorRole.Window, QColor(self.backGroundColor))
        pl.setColor(QPalette.ColorRole.Base, QColor(self.backGroundColor))
        pl.setColor(QPalette.ColorRole.Text, QColor(self.foreGroundColor))
        pl.setColor(QPalette.ColorRole.Highlight, QColor(self.backGroundColor))
        pl.setColor(QPalette.ColorRole.HighlightedText, QColor(self.highLightColor))
        self.setPalette(pl)
        self.update()

    # def resizeEvent(self, e):
    #     self.nullNum = self.height() / self.margin

