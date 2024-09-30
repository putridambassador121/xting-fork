#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: lrcShow-X.py

import os, glob, re
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from lrcShowX.lrcParser import lrcParser

from lrcShowX.lrclib import LrcLibAPI
from lrcShowX.lrclibThread import lrclibSearchThread, lrclibGetThread
from lrcShowX.resultDisplay import resultDisplay
from lrcShowX.tsTool import tsTool


class lrcShowX(QTextBrowser):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.constructMenu()

        self.lrclibApi = LrcLibAPI(user_agent="xting")
        self.lrclibSearchThread = lrclibSearchThread(self.lrclibApi)
        self.lrclibGetThread = lrclibGetThread(self.lrclibApi)

        self.transferTool = tsTool()

        self.timer = QTimer()
        self.animateTimer = QTimer()

        self.readParameters()

        self.lrcScheduleList = None
        self.currentTag = None

        self.initFont()
        self.initColor()

        self.showInfo("No music is playing")

        self.parent.parent.musicEngine.musicEquipment.playbackStateChanged.connect(self.playbackStateChanged_)
        self.parent.parent.positionChanged.connect(self.trackPositionChanged)
        self.timer.timeout.connect(self.scroll)
        self.animateTimer.timeout.connect(self.animate)

        self.lrclibSearchThread.lrcSearched.connect(self.lrclibSearchResult)
        self.lrclibGetThread.lrcGot.connect(self.lrclibGotLrc)

        self.customContextMenuRequested.connect(self.showContextMenu)


        self.copyPlainAction.triggered.connect(self.copyAction)
        self.copyLrcAction.triggered.connect(self.copyAction)
        self.reloadAction.triggered.connect(self.reloadAction_)
        self.closeLrcAction.triggered.connect(self.closeLrcAction_)


    def playbackStateChanged_(self, state):
        sv = state.value
        if sv == 0: # stoped state
            if self.timer.isActive():
                self.timer.stop()
            if self.animateTimer.isActive():
                self.animateTimer.stop()
            self.lrcScheduleList = None
            self.currentTag = None
            self.copyPlainAction.setEnabled(False)
            self.copyLrcAction.setEnabled(False)
            self.closeLrcAction.setEnabled(False)
            self.reloadAction.setEnabled(False)
            self.s2tAction.setEnabled(False)
            self.t2sAction.setEnabled(False)
            self.showInfo("No music is playing")

        elif sv == 1: # playing state
            if self.lrcScheduleList and self.currentTag:
                self.showLrc()
                self.locateCurrentTag()
                self.scrolLToCurrent()
            else:
                self.showInfo("Searching lrc...")
                fi = self.searchLocal()
                if fi:
                    p = lrcParser(fi, True)
                    self.lrcScheduleList = p.parse()
                    self.showLrc()
                    self.copyPlainAction.setEnabled(True)
                    self.copyLrcAction.setEnabled(True)
                    self.closeLrcAction.setEnabled(True)
                    self.reloadAction.setEnabled(True)
                    self.s2tAction.setEnabled(True)
                    self.t2sAction.setEnabled(True)
                    self.locateCurrentTag()
                    self.scrolLToCurrent()
                else:
                    self.searchLrclib()

                    # ll = self.searchOnline()
                    # if ll:
                    #     p = lrcParser(ll, False)
                    #     self.lrcScheduleList = p.parse()
                    #     self.showLrc()
                    #     self.locateCurrentTag()
                    #     self.scrolLToCurrent()
                    #     if self.autoSaveLrc:
                    #         with open(os.path.join(self.lrcLocalPath, f"{self.parent.parent.currentTrack.trackTitle} - {self.parent.parent.currentTrack.trackArtist}.lrc"), "w") as ff:
                    #             ff.write(ll)
                    # else:
                    #     self.lrcScheduleList = None
                    #     self.currentTag = None
                    #     self.copyPlainAction.setEnabled(False)
                    #     self.copyLrcAction.setEnabled(False)
                    #     self.closeLrcAction.setEnabled(True)
                    #     self.reloadAction.setEnabled(False)
                    #     self.s2tAction.setEnabled(False)
                    #     self.t2sAction.setEnabled(False)
                    #     self.showInfo("No lrc found")

        else:  # paused state
            if self.timer.isActive():
                self.timer.stop()
            if self.animateTimer.isActive():
                self.animateTimer.stop()

    def searchLrclib(self):
        self.lrclibSearchThread.title = self.parent.parent.currentTrack.trackTitle
        self.lrclibSearchThread.artist = self.parent.parent.currentTrack.trackArtist
        self.lrclibSearchThread.start()

    def lrclibSearchResult(self, l):
        if not l:
            self.lrcScheduleList = None
            self.currentTag = None
            self.showInfo("No lrc found")
            return

        if self.parent.parent.parameter.autoChooseTheFirst or len(l) == 1:
            self.lrclibGetThread.idd = l[0].id
            self.lrclibGetThread.start()
        else:
            dis = resultDisplay(self)
            dis.table.setRowCount(len(l))
            row = 0
            for i in l:
                dis.table.setItem(row, 0, QTableWidgetItem(i.track_name))
                dis.table.setItem(row, 1, QTableWidgetItem(i.artist_name))
                dis.table.setItem(row, 2, QTableWidgetItem(i.album_name))
                dis.table.setItem(row, 3, QTableWidgetItem(str(i.duration)))
                row += 1

            r = dis.exec()

            if r == 1:
                self.lrclibGetThread.idd = l[dis.currentRow].id
                self.lrclibGetThread.start()
            else:
                self.lrcScheduleList = None
                self.currentTag = None
                self.copyPlainAction.setEnabled(False)
                self.copyLrcAction.setEnabled(False)
                self.closeLrcAction.setEnabled(False)
                self.reloadAction.setEnabled(True)
                self.s2tAction.setEnabled(False)
                self.t2sAction.setEnabled(False)
                self.showInfo("Cancel getting lrc by user")


    def lrclibGotLrc(self, lrc):
        if lrc:
            if self.parent.parent.parameter.autoT2S:
                lrc = self.transferTool.transfer(lrc)
            p = lrcParser(lrc, False)
            self.lrcScheduleList = p.parse()
            self.showLrc()
            self.copyPlainAction.setEnabled(True)
            self.copyLrcAction.setEnabled(True)
            self.closeLrcAction.setEnabled(True)
            self.reloadAction.setEnabled(True)
            self.s2tAction.setEnabled(True)
            self.t2sAction.setEnabled(True)
            self.locateCurrentTag()
            self.scrolLToCurrent()
            if self.autoSaveLrc:
                with open(os.path.join(self.lrcLocalPath, f"{self.parent.parent.currentTrack.trackTitle} - {self.parent.parent.currentTrack.trackArtist}.lrc"), "w") as ff:
                    ff.write(lrc)
        else:
            self.lrcScheduleList = None
            self.currentTag = None
            self.copyPlainAction.setEnabled(False)
            self.copyLrcAction.setEnabled(False)
            self.closeLrcAction.setEnabled(False)
            self.reloadAction.setEnabled(True)
            self.s2tAction.setEnabled(False)
            self.t2sAction.setEnabled(False)
            self.showInfo("lrc error")

    def searchOnline(self):
        title = self.parent.parent.currentTrack.trackTitle
        artist = self.parent.parent.currentTrack.trackArtist
        e = searchEngine()
        l = e.search(title, artist)
        if l:
            return l
        else:
            return False

    def searchLocal(self):
        title = self.parent.parent.currentTrack.trackTitle
        artist = self.parent.parent.currentTrack.trackArtist
        if title == "unknow" or (not title):
            return False
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
        duration = self.lrcScheduleList[self.currentTag][0] - self.trackPos
        self.verticalScrollBar().setValue((self.currentTag - 1) * self.margin)
        self.timer.start(duration)

    def scroll(self):
        duration = self.lrcScheduleList[self.currentTag][2]
        if duration < 0:
            pass
        else:
            if duration < 700:
                self.verticalScrollBar().setValue(self.currentTag * self.margin)
            else:
                self.animateStartTag = self.currentTag
                self.animate()
            self.timer.start(duration)
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
        self.autoSaveLrc = self.parent.parent.parameter.autoSaveLrc
        if not self.parent.parent.parameter.lrcFont:
            self.lrcFont = self.parent.parent.parameter.lrcFont = self.font().toString()
        else:
            self.lrcFont = self.parent.parent.parameter.lrcFont

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

    def initFont(self):
        f = QFont()
        f.fromString(self.lrcFont)
        self.setFont(f)
        self.margin = QFontMetrics(self.font()).height() + self.lineMargin
        self.nullNum = int(self.viewport().height() / self.margin)

    def initColor(self):
        pl = QPalette()
        pl.setColor(QPalette.ColorRole.Window, QColor(self.backGroundColor))
        pl.setColor(QPalette.ColorRole.Base, QColor(self.backGroundColor))
        pl.setColor(QPalette.ColorRole.Text, QColor(self.foreGroundColor))
        pl.setColor(QPalette.ColorRole.Highlight, QColor(self.backGroundColor))
        pl.setColor(QPalette.ColorRole.HighlightedText, QColor(self.highLightColor))
        self.setPalette(pl)
        self.update()

    def showContextMenu(self, pos):
        self.contextMenu.popup(self.mapToGlobal(pos))

    def constructMenu(self):
        self.contextMenu = QMenu(self)
        offsetMenu = self.contextMenu.addMenu(self.tr("Offset"))
        self.forwardAction = QAction(QIcon("icon/forward.png"), "+200ms")
        self.forwardAction.setEnabled(False)
        self.backwardAction = QAction(QIcon("icon/backward.png"), "-200ms")
        self.backwardAction.setEnabled(False)
        self.saveTheOffsetAction = QAction(self.tr("Save the offset"))
        self.saveTheOffsetAction.setEnabled(False)
        offsetMenu.addAction(self.forwardAction)
        offsetMenu.addAction(self.backwardAction)
        self.saveTheLrcAction = QAction(self.tr("Save the lrc"))
        self.contextMenu.addAction(self.saveTheLrcAction)
        self.reloadAction = QAction(self.tr("Reload lrc"))
        self.reloadAction.setEnabled(False)
        self.contextMenu.addAction(self.reloadAction)
        self.closeLrcAction = QAction(self.tr("Close the lrc"))
        self.contextMenu.addAction(self.closeLrcAction)
        copyMenu = self.contextMenu.addMenu(self.tr("Copy"))
        self.copyPlainAction = QAction(self.tr("Copy plain lyrics"))
        self.copyPlainAction.setEnabled(False)
        self.copyLrcAction = QAction(self.tr("Copy synced lyrics"))
        self.copyLrcAction.setEnabled(False)
        copyMenu.addAction(self.copyPlainAction)
        copyMenu.addAction(self.copyLrcAction)
        stToolMenu = self.contextMenu.addMenu(self.tr("S-T transfer"))
        self.s2tAction = QAction(self.tr("s2t"))
        self.s2tAction.setEnabled(False)
        stToolMenu.addAction(self.s2tAction)
        self.t2sAction = QAction(self.tr("t2s"))
        self.t2sAction.setEnabled(False)
        stToolMenu.addAction(self.t2sAction)


    def copyAction(self):
        l = self.toPlainText().strip()
        if self.sender().iconText() == "Copy plain lyrics":
            t = re.sub(r"\[\d\d:\d\d.*?\]", "", l)
        else:
            t = self.constructLrcFromPlain()
        clipboard = QApplication.clipboard()
        clipboard.setText(t)

    def constructLrcFromPlain(self):
        if self.lrcScheduleList:
            t = ""
            for i in self.lrcScheduleList[1:]:
                t += f"{self.msTotag(i[0])}{i[1]}\n"
            return t
        else:
            return False

    def msTotag(self, t):
        m, ts = divmod(t, 60000)
        if m < 10:
            m = f'0{m}'
        else:
            m = str(m)
        ms = str(ts)[-3:]
        s = str(ts)[:2]
        return f"[{m}:{s}.{ms}]"

    def reloadAction_(self):
        self.lrcScheduleList = self.currentTag = None
        self.playbackStateChanged_(self.parent.parent.musicEngine.getPlaybackState())

    def closeLrcAction_(self):
        if self.timer.isActive():
            self.timer.stop()
        if self.animateTimer.isActive():
            self.animateTimer.stop()
        self.lrcScheduleList = None
        self.currentTag = None
        self.copyPlainAction.setEnabled(False)
        self.copyLrcAction.setEnabled(False)
        self.closeLrcAction.setEnabled(False)
        self.s2tAction.setEnabled(False)
        self.t2sAction.setEnabled(False)
        self.showInfo("Current lrc was closed")



    def mouseDoubleClickEvent(self, e):
        e.ignore()

    def mouseClickEvent(self, e):
        e.ignore()

    def mousePressEvent(self, e):
        e.ignore()

    def mouseReleaseEvent(self, e):
        e.ignore()

    def wheelEvent(self, e):
        e.ignore()

