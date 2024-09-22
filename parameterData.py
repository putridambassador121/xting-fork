#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: parameterData.py


from PyQt6.QtCore import QSettings
import os.path


class parameterData:

    def __init__(self):
        configPath = os.path.join(os.path.expanduser("~"), ".ting/ting.conf")
        self.iniFile = QSettings(configPath, QSettings.Format.IniFormat)

    def read(self):
        self.collectionPath = self.iniFile.value("player/collectionpath", os.path.expanduser("~"))
        self.trayIcon = self.stringToBool(self.iniFile.value("player/trayicon", False))
        self.trayInfo = self.stringToBool(self.iniFile.value("player/trayinfo", False))
        self.loop = self.iniFile.value("player/loop", "playlist")
        self.sequence = self.iniFile.value("player/sequence", "order")

    def save(self):
        self.iniFile.setValue("player/collectionpath", self.collectionPath)
        self.iniFile.setValue("player/trayicon", self.trayIcon)
        self.iniFile.setValue("player/trayinfo", self.trayInfo)
        self.iniFile.setValue("player/loop", self.loop)
        self.iniFile.setValue("player/sequence", self.sequence)

    def stringToBool(self, s):
        if type(s) == bool:
            return s
        else:
            if s.lower() == "false":
                return False
            else:
                return True
