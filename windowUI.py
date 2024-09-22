#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: windowUI.py


import os, sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from dockWidgets import *

class windowUI(QMainWindow):

    def __init__(self, devices):
        super().__init__()

        self.devices =devices
        self.initDockwidget()
        self.initCentralWidget()
        self.initMenuBar()
        # self.initStatusBar()

    def initCentralWidget(self):
        self.centralWidget = controlWidget(self)
        self.setCentralWidget(self.centralWidget)

    def initMenuBar(self):
        self.fileMenu = self.menuBar().addMenu("File")
        self.openFileAction = QAction("Open...")
        self.quitAction = QAction("Quit")
        self.fileMenu.addAction(self.openFileAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)

        self.playbackMenu = self.menuBar().addMenu("Playback")
        self.previousAction = QAction("Previous")
        self.previousAction.setEnabled(False)
        self.playorpauseAction = QAction("Play")
        self.stopAction = QAction("Stop")
        self.stopAction.setEnabled(False)
        self.nextAction = QAction("Next")
        self.nextAction.setEnabled(False)
        self.repeatAction = QAction("Repeat")
        self.repeatAction.setEnabled(False)
        self.playbackMenu.addAction(self.previousAction)
        self.playbackMenu.addAction(self.playorpauseAction)
        self.playbackMenu.addAction(self.stopAction)
        self.playbackMenu.addAction(self.nextAction)

        self.playlistMenu = self.menuBar().addMenu("Playlist")
        self.loopMenu = self.playlistMenu.addMenu("Loop")
        self.loopTrackAction = QAction("Track")
        self.loopTrackAction.setCheckable(True)
        self.loopPlaylistAction = QAction("Playlist")
        self.loopPlaylistAction.setCheckable(True)
        self.loopGroup = QActionGroup(self)
        self.loopGroup.addAction(self.loopTrackAction)
        self.loopGroup.addAction(self.loopPlaylistAction)
        self.loopMenu.addAction(self.loopTrackAction)
        self.loopMenu.addAction(self.loopPlaylistAction)
        self.sequenceMenu = self.playlistMenu.addMenu("Sequence")
        self.sequenceRandomAction = QAction("Random")
        self.sequenceRandomAction.setCheckable(True)
        self.sequenceOrderAction = QAction("Order")
        self.sequenceOrderAction.setCheckable(True)
        self.sequenceReverseOrderAction = QAction("Reverse order")
        self.sequenceReverseOrderAction.setCheckable(True)
        self.sequenceGroup = QActionGroup(self)
        self.sequenceGroup.addAction(self.sequenceOrderAction)
        self.sequenceGroup.addAction(self.sequenceReverseOrderAction)
        self.sequenceGroup.addAction(self.sequenceRandomAction)
        self.sequenceMenu.addAction(self.sequenceOrderAction)
        self.sequenceMenu.addAction(self.sequenceReverseOrderAction)
        self.sequenceMenu.addAction(self.sequenceRandomAction)

        self.audioMenu = self.menuBar().addMenu("Audio")
        self.deviceMenu = self.audioMenu.addMenu("Device")
        self.deviceGroup = QActionGroup(self)
        n = 0
        for d in self.devices:
            exec(f"self.device{n}Action = QAction(d.description())")
            exec(f"self.device{n}Action.setObjectName('{n}')")
            exec(f"self.device{n}Action.setCheckable(True)")
            exec(f"self.deviceGroup.addAction(self.device{n}Action)")
            exec(f"self.deviceMenu.addAction(self.device{n}Action)")
            n += 1



        self.toolsMenu = self.menuBar().addMenu("Tools")
        self.scanAction = QAction("Scan collection")
        self.toolsMenu.addAction(self.scanAction)

        self.settingMenu = self.menuBar().addMenu("Setting")
        self.configurateAction = QAction("Configurate...")
        self.settingMenu.addAction(self.configurateAction)

        self.helpMenu = self.menuBar().addMenu("Help")
        self.aboutAppAction = QAction("About App...")
        self.aboutQtAction = QAction("About Qt...")
        self.helpMenu.addAction(self.aboutAppAction)
        self.helpMenu.addAction(self.aboutQtAction)

    def initDockwidget(self):
        self.lrcShowDock = lrcShowDock("lrcShow", self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.lrcShowDock)

        self.playlistDock = playlistDock("playlist", self)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.playlistDock)

        self.setCorner(Qt.Corner.TopLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)






class controlWidget(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        buttonLayout = QHBoxLayout(None)
        self.previousButton = QPushButton("Previous", self)
        self.previousButton.setEnabled(False)
        self.playorpauseButton = QPushButton("Play", self)
        self.stopButton = QPushButton("Stop", self)
        self.stopButton.setEnabled(False)
        self.nextButton = QPushButton("Next", self)
        self.nextButton.setEnabled(False)
        self.repeatButton = QPushButton("Repeat", self)
        self.repeatButton.setEnabled(False)
        self.volumeSlider = QSlider(self)
        self.volumeSlider.setOrientation(Qt.Orientation.Horizontal)
        self.volumeSlider.setTracking(False)
        self.volumeSlider.setRange(0, 10)
        buttonLayout.addWidget(self.previousButton)
        buttonLayout.addWidget(self.playorpauseButton)
        buttonLayout.addWidget(self.stopButton)
        buttonLayout.addWidget(self.nextButton)
        buttonLayout.addWidget(self.repeatButton)
        buttonLayout.addWidget(self.volumeSlider)

        progressLayout = QHBoxLayout(None)
        self.progressSlider = QSlider(self)
        self.progressSlider.setTracking(False)
        self.progressSlider.setOrientation(Qt.Orientation.Horizontal)
        self.progressSlider.setEnabled(False)
        self.timeLabel = QLabel("--:--", self)
        self.lengthLabel = QLabel("--:--", self)
        progressLayout.addWidget(self.timeLabel)
        progressLayout.addWidget(self.progressSlider)
        progressLayout.addWidget(self.lengthLabel)

        mainLayout = QVBoxLayout(None)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(progressLayout)
        self.setLayout(mainLayout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = windowUI()
    w.show()

    sys.exit(app.exec())
