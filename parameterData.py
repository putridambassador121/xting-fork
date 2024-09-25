#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: parameterData.py


from PyQt6.QtCore import QSettings
import os.path


class parameterData:

    def __init__(self):
        configPath = os.path.join(os.path.expanduser("~"), ".xting/xting.conf")
        self.iniFile = QSettings(configPath, QSettings.Format.IniFormat)
        self.doQuit = False

    def read(self):
        self.collectionPath = self.iniFile.value("/player/collectionpath", os.path.expanduser("~"))
        self.trayIcon = self.stringToBool(self.iniFile.value("/player/trayicon", False))
        self.trayInfo = self.stringToBool(self.iniFile.value("/player/trayinfo", False))
        self.closeNotQuit = self.stringToBool(self.iniFile.value("/player/closenotquit", False))
        self.loop = self.iniFile.value("/player/loop", "playlist")
        self.sequence = self.iniFile.value("/player/sequence", "order")

        self.windowState = self.iniFile.value("/session/windowstate/", "")
        self.windowGeometry = self.iniFile.value("/session/windowgeometry", "")
        self.lrcShowxDockGeometry = self.iniFile.value("/session/lrcshowxdockgeometry", "")
        self.playlistDockGeometry = self.iniFile.value("/session/playlistdockgeometry", "")
        self.albumCoverDockGeometry = self.iniFile.value("/session/albumcoverdockgeometry", "")
        self.playlistDockAllTableState = self.iniFile.value("/session/playlistdockalltablestate", "")
        self.playlistDockCustomTableState = self.iniFile.value("/session/playlistdockcustomtablestate", "")

        self.lineMargin = self.iniFile.value("/lrcshowx/linemargin", 5)
        self.topMarginLines = self.iniFile.value("/lrcshowx/topmarginlines", 5)


    def save(self):
        self.iniFile.setValue("player/collectionpath", self.collectionPath)
        self.iniFile.setValue("player/trayicon", self.trayIcon)
        self.iniFile.setValue("player/trayinfo", self.trayInfo)
        self.iniFile.setValue("player/closenotquit", self.closeNotQuit)
        self.iniFile.setValue("player/loop", self.loop)
        self.iniFile.setValue("player/sequence", self.sequence)

        self.iniFile.setValue("/session/windowstate", self.windowState)
        self.iniFile.setValue("/session/windowgeometry", self.windowGeometry)
        self.iniFile.setValue("/session/lrcshowxdockgeometry", self.lrcShowxDockGeometry)
        self.iniFile.setValue("/session/playlistdockgeometry", self.playlistDockGeometry)
        self.iniFile.setValue("/session/albumcoverdockgeometry", self.albumCoverDockGeometry)
        self.iniFile.setValue("/session/playlistdockalltablestate", self.playlistDockAllTableState)
        self.iniFile.setValue("/session/playlistdockcustomtablestate", self.playlistDockCustomTableState)

    def stringToBool(self, s):
        if type(s) == bool:
            return s
        else:
            if s.lower() == "false":
                return False
            else:
                return True
