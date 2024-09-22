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
        self.initStatusBar()

    def initStatusBar(self):
        self.infoLabel = QLabel()
        self.statusBar().addPermanentWidget(self.infoLabel)

    def initCentralWidget(self):
        self.centralWidget = controlWidget(self)
        self.setCentralWidget(self.centralWidget)

    def initMenuBar(self):
        self.fileMenu = self.menuBar().addMenu(self.tr("File"))
        self.openFileAction = QAction(self.tr("Open..."))
        self.quitAction = QAction(self.tr("Quit"))
        self.fileMenu.addAction(self.openFileAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)

        self.playbackMenu = self.menuBar().addMenu(self.tr("Playback"))
        self.previousAction = QAction(self.tr("Previous"))
        self.previousAction.setEnabled(False)
        self.playorpauseAction = QAction(self.tr("Play"))
        self.stopAction = QAction(self.tr("Stop"))
        self.stopAction.setEnabled(False)
        self.nextAction = QAction(self.tr("Next"))
        self.nextAction.setEnabled(False)
        self.repeatAction = QAction(self.tr("Repeat"))
        self.repeatAction.setEnabled(False)
        self.playbackMenu.addAction(self.previousAction)
        self.playbackMenu.addAction(self.playorpauseAction)
        self.playbackMenu.addAction(self.stopAction)
        self.playbackMenu.addAction(self.nextAction)
        self.playbackMenu.addAction(self.repeatAction)

        self.playlistMenu = self.menuBar().addMenu(self.tr("Playlist"))
        self.loopMenu = self.playlistMenu.addMenu(self.tr("Loop"))
        self.loopTrackAction = QAction(self.tr("Track"))
        self.loopTrackAction.setCheckable(True)
        self.loopPlaylistAction = QAction(self.tr("Playlist"))
        self.loopPlaylistAction.setCheckable(True)
        self.loopGroup = QActionGroup(self)
        self.loopGroup.addAction(self.loopTrackAction)
        self.loopGroup.addAction(self.loopPlaylistAction)
        self.loopMenu.addAction(self.loopTrackAction)
        self.loopMenu.addAction(self.loopPlaylistAction)
        self.sequenceMenu = self.playlistMenu.addMenu(self.tr("Sequence"))
        self.sequenceRandomAction = QAction(self.tr("Random"))
        self.sequenceRandomAction.setCheckable(True)
        self.sequenceOrderAction = QAction(self.tr("Order"))
        self.sequenceOrderAction.setCheckable(True)
        self.sequenceReverseOrderAction = QAction(self.tr("Reverse order"))
        self.sequenceReverseOrderAction.setCheckable(True)
        self.sequenceGroup = QActionGroup(self)
        self.sequenceGroup.addAction(self.sequenceOrderAction)
        self.sequenceGroup.addAction(self.sequenceReverseOrderAction)
        self.sequenceGroup.addAction(self.sequenceRandomAction)
        self.sequenceMenu.addAction(self.sequenceOrderAction)
        self.sequenceMenu.addAction(self.sequenceReverseOrderAction)
        self.sequenceMenu.addAction(self.sequenceRandomAction)

        self.viewMenu = self.menuBar().addMenu(self.tr("View"))
        self.viewMenu.addAction(self.lrcShowxDock.toggleViewAction())
        self.viewMenu.addAction(self.playlistDock.toggleViewAction())
        self.viewMenu.addAction(self.albumCoverDock.toggleViewAction())

        self.audioMenu = self.menuBar().addMenu(self.tr("Audio"))
        self.deviceMenu = self.audioMenu.addMenu(self.tr("Device"))
        self.deviceGroup = QActionGroup(self)
        n = 0
        for d in self.devices:
            exec(f"self.device{n}Action = QAction(d.description())")
            exec(f"self.device{n}Action.setObjectName('{n}')")
            exec(f"self.device{n}Action.setCheckable(True)")
            exec(f"self.deviceGroup.addAction(self.device{n}Action)")
            exec(f"self.deviceMenu.addAction(self.device{n}Action)")
            n += 1

        self.toolsMenu = self.menuBar().addMenu(self.tr("Tools"))
        self.scanAction = QAction(self.tr("Scan collection"))
        self.toolsMenu.addAction(self.scanAction)

        self.settingMenu = self.menuBar().addMenu(self.tr("Setting"))
        self.configurateAction = QAction(self.tr("Configurate..."))
        self.settingMenu.addAction(self.configurateAction)

        self.helpMenu = self.menuBar().addMenu(self.tr("Help"))
        self.aboutAppAction = QAction(self.tr("About ting..."))
        self.aboutQtAction = QAction(self.tr("About Qt..."))
        self.helpMenu.addAction(self.aboutAppAction)
        self.helpMenu.addAction(self.aboutQtAction)

    def initDockwidget(self):
        self.lrcShowxDock = lrcShowxDock(self.tr("lrcShow-X"), self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.lrcShowxDock)
        self.lrcShowxDock.setObjectName("lrcShow-X")

        self.playlistDock = playlistDock(self.tr("Playlist"), self)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.playlistDock)
        self.playlistDock.setObjectName("Playlist")

        self.albumCoverDock = albumCoverDock(self.tr("Album cover"), self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.albumCoverDock)
        self.albumCoverDock.setObjectName("Album cover")

        self.setCorner(Qt.Corner.TopLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setCorner(Qt.Corner.TopRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)
        self.setCorner(Qt.Corner.BottomLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setCorner(Qt.Corner.BottomRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)



class controlWidget(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        buttonLayout = QHBoxLayout(None)
        self.previousButton = QPushButton(self.tr("Previous"), self)
        self.previousButton.setEnabled(False)
        self.playorpauseButton = QPushButton(self.tr("Play"), self)
        self.stopButton = QPushButton(self.tr("Stop"), self)
        self.stopButton.setEnabled(False)
        self.nextButton = QPushButton(self.tr("Next"), self)
        self.nextButton.setEnabled(False)
        self.repeatButton = QPushButton(self.tr("Repeat"), self)
        self.repeatButton.setEnabled(False)
        self.volumeSlider = QSlider(self)
        self.volumeSlider.setOrientation(Qt.Orientation.Horizontal)
        self.volumeSlider.setTracking(False)
        self.volumeSlider.setRange(0, 10)
        buttonLayout.addStretch(0)
        buttonLayout.addWidget(self.previousButton)
        buttonLayout.addWidget(self.playorpauseButton)
        buttonLayout.addWidget(self.stopButton)
        buttonLayout.addWidget(self.nextButton)
        buttonLayout.addWidget(self.repeatButton)
        buttonLayout.addStretch(0)
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
        #mainLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        mainLayout.addStretch(0)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(progressLayout)
        #mainLayout.addStretch(0)
        self.setLayout(mainLayout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = windowUI()
    w.show()

    sys.exit(app.exec())
