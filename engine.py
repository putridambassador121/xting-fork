#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: engine.py

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaMetaData

class engine:

    def __init__(self):
        self.musicEquipment = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.musicEquipment.setAudioOutput(self.audioOutput)
        self.musicEquipment.setLoops(1)
        self.musicFile = None

    def getPlaybackState(self):
        return self.musicEquipment.playbackState()

    def add(self, f):
        self.musicFile = f
        self.musicEquipment.setSource(QUrl(self.musicFile))

    def play(self):
        if self.musicFile != None:
            self.musicEquipment.play()
        else:
            print(self.tr("please add a track first"))

    def pause(self):
        self.musicEquipment.pause()

    def stop(self):
        self.musicEquipment.stop()

    def getDevice(self):
        d = self.audioOutput.device()
        return (d.id(), d.description())

    def setDevice(self, d):
        self.audioOutput.setDevice(d)

    def getPosition(self):
        return self.musicEquipment.position()

    def setPosition(self, p):
        self.musicEquipment.setPosition(p)

    def getVolume(self):
        return self.audioOutput.volume()

    def setVolume(self, v):
        self.audioOutput.setVolume(v)

    def isPlaying(self):
        return self.musicEquipment.isPlaying()

    def getDuration(self):
        return int(self.musicEquipment.duration())

class mw(QWidget):

    def __init__(self):
        super().__init__()
        mainLayout = QVBoxLayout(None)
        self.add = QPushButton("add", self)
        self.playPause = QPushButton("play", self)
        self.stop = QPushButton("Stop", self)
        self.test = QPushButton("test", self)
        mainLayout.addWidget(self.add)
        mainLayout.addWidget(self.playPause)
        mainLayout.addWidget(self.stop)
        mainLayout.addWidget(self.test)
        self.setLayout(mainLayout)

        self.p = engine()

        self.add.clicked.connect(self.add_)
        self.playPause.clicked.connect(self.playPause_)
        self.stop.clicked.connect(self.stop_)
        self.test.clicked.connect(self.test_)

    def add_(self):
        self.p.add("/home/frank/Music/04 蓝天.mp3")

    def playPause_(self):
        self.p.play()

    def stop_(self):
        self.p.stop()

    def test_(self):
        #self.p.position()
        # m = self.p.metadata()
        # print(m.value(QMediaMetaData.Key.Title))
        print(self.p.getTitle())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = mw()
    w.show()

    sys.exit(app.exec())
