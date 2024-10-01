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
