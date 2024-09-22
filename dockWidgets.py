#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: dockWidgets.py


import os, sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class lrcShowDock(QDockWidget):

    def __init__(self, title, parent = None):
        super().__init__(title)
        self.lrcShowWidget = lrcShowWidget(parent)
        self.setWidget(self.lrcShowWidget)
        self.setFloating(False)


class lrcShowWidget(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent


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
        self.searchLabel = QLabel("Search:")
        self.searchLine = QLineEdit(self)
        searchLayout.addWidget(self.searchLabel)
        searchLayout.addWidget(self.searchLine)

        self.allTable = QTableWidget(0, 9)
        self.allTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.allTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        #self.allTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        header = ["Title", "Artist", "Length", "Album", "Type", "Date", "Bit rate", "Sample rate", "File"]
        self.allTable.setHorizontalHeaderLabels(header)

        self.customTable = QTableWidget(0, 9)
        self.customTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.customTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        #self.customTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.customTable.setHorizontalHeaderLabels(header)

        self.tabArea = QTabWidget(self)
        self.tabArea.addTab(self.allTable, "All tracks")
        self.tabArea.addTab(self.customTable, "Playlist")

        mainLayout = QVBoxLayout(None)
        mainLayout.addLayout(searchLayout)
        mainLayout.addWidget(self.tabArea)
        self.setLayout(mainLayout)

