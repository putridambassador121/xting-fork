#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: dockWidgets.py


import os, sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class lrcShowxDock(QDockWidget):

    def __init__(self, title, parent = None):
        super().__init__(title)
        self.lrcShowxWidget = lrcShowxWidget(parent)
        self.setWidget(self.lrcShowxWidget)
        self.setFloating(False)


class lrcShowxWidget(QTextBrowser):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setText("lrcShow-X is not available yet, temporarily serving as an easy guide. Modify the collection path in config file ($HOME/.ting/ting.conf), then click Tools-Scan collection, app will load your media files (mp3 and flac temporarily) in 'All tracks' tab in playlist dock, now you can listen music with ting app. It's a personal app, if you don't like it, forget it!")


class playlistDock(QDockWidget):

    def __init__(self, title, parent = None):
        super().__init__(title)
        self.playlistWidget = playlistWidget(self)
        self.setWidget(self.playlistWidget)
        self.setFloating(False)


class playlistWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        searchLayout = QHBoxLayout(None)
        self.searchLabel = QLabel(self.tr("Search:"))
        self.searchLine = QLineEdit(self)
        searchLayout.addWidget(self.searchLabel)
        searchLayout.addWidget(self.searchLine)

        self.allTable = QTableWidget(0, 9)
        self.allTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.allTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        #self.allTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        header = [self.tr("Title"), self.tr("Artist"), self.tr("Length"), self.tr("Album"), self.tr("Type"), self.tr("Date"), self.tr("Bit rate"), self.tr("Sample rate"), self.tr("File")]
        self.allTable.setHorizontalHeaderLabels(header)

        self.customTable = QTableWidget(0, 9)
        self.customTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.customTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        #self.customTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.customTable.setHorizontalHeaderLabels(header)

        self.tabArea = QTabWidget(self)
        self.tabArea.addTab(self.allTable, self.tr("All tracks"))
        self.tabArea.addTab(self.customTable, self.tr("Playlist"))

        mainLayout = QVBoxLayout(None)
        mainLayout.addLayout(searchLayout)
        mainLayout.addWidget(self.tabArea)
        self.setLayout(mainLayout)


class albumCoverDock(QDockWidget):

    def __init__(self, title, parent = None):
        super().__init__(title)
        self.albumCoverWidget = albumCoverWidget(self)
        self.setWidget(self.albumCoverWidget)
        self.setFloating(False)

        try:
            self.restorGeometry(parent.parameter.albumCoverDockGeometry)
        except:
            pass


class albumCoverWidget(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
