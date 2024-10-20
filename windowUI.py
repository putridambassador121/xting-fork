#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: windowUI.py

import os, sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from dockWidgets import *
from parameterData import parameterData

class windowUI(QMainWindow):

    positionChanged = pyqtSignal()

    def __init__(self, devices):
        super().__init__()
        self.parameter = parameterData()
        self.parameter.read()

        self.devices = devices
        # self.initDockwidget()
        # self.initCentralWidget()
        # self.initMenuBar()
        # self.initStatusBar()

    def initStatusBar(self):
        self.infoLabel = QLabel()
        self.statusBar().addPermanentWidget(self.infoLabel)

    def initCentralWidget(self):
        self.centralWidget = controlWidget(self)
        self.setCentralWidget(self.centralWidget)

    def initMenuBar(self):
        self.fileMenu = self.menuBar().addMenu(self.tr("File"))
        self.openFileAction = QAction(QIcon("icon/open.png"), self.tr("Open..."))
        self.quitAction = QAction(QIcon("icon/quit.png"), self.tr("Quit"))
        self.quitAction.setObjectName("quit")
        self.fileMenu.addAction(self.openFileAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)

        self.playbackMenu = self.menuBar().addMenu(self.tr("Playback"))
        self.previousAction = QAction(QIcon("icon/previous.png"), self.tr("Previous"))
        self.previousAction.setEnabled(False)
        self.playorpauseAction = QAction(QIcon("icon/play.png"), self.tr("Play"))
        self.playorpauseAction.setEnabled(False)
        self.stopAction = QAction(QIcon("icon/stop.png"), self.tr("Stop"))
        self.stopAction.setEnabled(False)
        self.nextAction = QAction(QIcon("icon/next.png"), self.tr("Next"))
        self.nextAction.setEnabled(False)
        self.repeatAction = QAction(QIcon("icon/repeat.png"), self.tr("Repeat"))
        self.repeatAction.setEnabled(False)
        self.playbackMenu.addAction(self.previousAction)
        self.playbackMenu.addAction(self.playorpauseAction)
        self.playbackMenu.addAction(self.stopAction)
        self.playbackMenu.addAction(self.nextAction)
        self.playbackMenu.addAction(self.repeatAction)

        self.playlistMenu = self.menuBar().addMenu(self.tr("Playlist"))
        self.loopMenu = self.playlistMenu.addMenu(self.tr("Loop"))
        self.loopTrackAction = QAction(QIcon("icon/loop track.png"), self.tr("Track"))
        self.loopTrackAction.setCheckable(True)
        self.loopPlaylistAction = QAction(QIcon("icon/loop playlist.png"), self.tr("Playlist"))
        self.loopPlaylistAction.setCheckable(True)
        self.noLoopAction = QAction(QIcon("icon/no loop.png"), self.tr("No loop"))
        self.noLoopAction.setCheckable(True)
        self.loopGroup = QActionGroup(self)
        self.loopGroup.addAction(self.loopTrackAction)
        self.loopGroup.addAction(self.loopPlaylistAction)
        self.loopGroup.addAction(self.noLoopAction)
        self.loopMenu.addAction(self.loopTrackAction)
        self.loopMenu.addAction(self.loopPlaylistAction)
        self.loopMenu.addAction(self.noLoopAction)
        self.sequenceMenu = self.playlistMenu.addMenu(self.tr("Sequence"))
        self.sequenceRandomAction = QAction(QIcon("icon/radom.png"), self.tr("Random"))
        self.sequenceRandomAction.setCheckable(True)
        self.sequenceOrderAction = QAction(QIcon("icon/order.png"), self.tr("Order"))
        self.sequenceOrderAction.setCheckable(True)
        self.sequenceReverseOrderAction = QAction(QIcon("icon/revised.png"), self.tr("Reverse order"))
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
        self.viewMenu.addAction(self.lrcEditorDock.toggleViewAction())
        self.viewMenu.addAction(self.playlistDock.toggleViewAction())
        self.viewMenu.addAction(self.albumCoverDock.toggleViewAction())
        self.viewMenu.addAction(self.collectionDock.toggleViewAction())

        self.audioMenu = self.menuBar().addMenu(self.tr("Audio"))
        self.deviceMenu = self.audioMenu.addMenu(QIcon("icon/device.png"), self.tr("Device"))
        self.deviceGroup = QActionGroup(self)
        n = 0
        for d in self.devices:
            exec(f"self.device{n}Action = QAction(d.description())")
            exec(f"self.device{n}Action.setObjectName('{n}')")
            exec(f"self.device{n}Action.setCheckable(True)")
            exec(f"self.deviceGroup.addAction(self.device{n}Action)")
            exec(f"self.deviceMenu.addAction(self.device{n}Action)")
            n += 1

        # self.toolsMenu = self.menuBar().addMenu(self.tr("Tools"))
        # self.scanAction = QAction(self.tr("Scan collection"))
        # self.toolsMenu.addAction(self.scanAction)

        self.settingMenu = self.menuBar().addMenu(self.tr("Setting"))
        self.configurationAction = QAction(QIcon("icon/configurate.png"), self.tr("Configurate..."))
        self.settingMenu.addAction(self.configurationAction)

        self.helpMenu = self.menuBar().addMenu(self.tr("Help"))
        self.aboutAppAction = QAction(QIcon("icon/logo.png"), self.tr("About xting..."))
        self.aboutQtAction = QAction(QIcon("icon/qt.png"), self.tr("About Qt..."))
        self.helpMenu.addAction(self.aboutAppAction)
        self.helpMenu.addAction(self.aboutQtAction)


        self.trayContextMenu = QMenu(self)
        self.trayContextMenu.addAction(self.previousAction)
        self.trayContextMenu.addAction(self.playorpauseAction)
        self.trayContextMenu.addAction(self.stopAction)
        self.trayContextMenu.addAction(self.nextAction)
        self.trayContextMenu.addAction(self.repeatAction)
        self.trayContextMenu.addSeparator()
        self.trayContextMenu.addAction(self.quitAction)


    def initDockwidget(self):
        self.lrcShowxDock = lrcShowxDock(self.tr("lrcShow-X"), self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.lrcShowxDock)
        self.lrcShowxDock.setObjectName("lrcShow-X")

        self.lrcEditorDock = lrcEditorDock(self.tr("Lrc editor"), self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.lrcEditorDock)
        self.lrcEditorDock.setObjectName("Lrc editor")
        self.lrcEditorDock.setVisible(False)

        self.playlistDock = playlistDock(self.tr("Playlist"), self)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.playlistDock)
        self.playlistDock.setObjectName("Playlist")

        self.collectionDock = collectionDock(self.tr("Collection"), self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.collectionDock)
        self.collectionDock.setObjectName("Collection")

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
        self.previousButton = QPushButton(self)
        self.previousButton.setMinimumSize(50, 50)
        self.previousButton.setIcon(QIcon("icon/previous.png"))
        self.previousButton.setIconSize(QSize(40, 40))
        self.previousButton.setEnabled(False)
        self.playorpauseButton = QPushButton(self)
        self.playorpauseButton.setMinimumSize(50, 50)
        self.playorpauseButton.setIcon(QIcon("icon/play.png"))
        self.playorpauseButton.setIconSize(QSize(40, 40))
        self.playorpauseButton.setEnabled(False)
        self.stopButton = QPushButton(self)
        self.stopButton.setMinimumSize(50, 50)
        self.stopButton.setIcon(QIcon("icon/stop.png"))
        self.stopButton.setIconSize(QSize(40, 40))
        self.stopButton.setEnabled(False)
        self.nextButton = QPushButton(self)
        self.nextButton.setMinimumSize(50, 50)
        self.nextButton.setIcon(QIcon("icon/next.png"))
        self.nextButton.setIconSize(QSize(40, 40))
        self.nextButton.setEnabled(False)
        self.repeatButton = QPushButton(self)
        self.repeatButton.setMinimumSize(50, 50)
        self.repeatButton.setIcon(QIcon("icon/repeat.png"))
        self.repeatButton.setIconSize(QSize(40, 40))
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
