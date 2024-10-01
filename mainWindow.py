#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: mainWindow.py


import os, sys, glob, mutagen, random
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaMetaData, QMediaDevices

from configuration import configuration
from windowUI import windowUI
from engine import engine

from track import track



class mainWindow(windowUI):

    def __init__(self, devices):
        super().__init__(devices)

        self.setWindowTitle("xting")
        self.setWindowIcon(QIcon("icon/logo.png"))
        self.appPrivatePath = os.path.expanduser("~/.xting")
        self.timer = QTimer()

        self.musicEngine = engine()
        self.playHistory = []
        self.currentTrack = None
        self.currentNo = -1
        self.schedule = True
        self.addToPlayHistory = True

        self.initCentralWidget()
        self.initDockwidget()
        self.initMenuBar()
        self.initStatusBar()

        self.systemTray = QSystemTrayIcon(QIcon("icon/logo.png"), self)
        self.systemTray.setContextMenu(self.trayContextMenu)
        self.systemTray.setVisible(self.parameter.trayIcon)

        if self.parameter.loop == "playlist":
            self.loopPlaylistAction.setChecked(True)
        else:
            self.loopTrackAction.setChecked(True)

        if self.parameter.sequence == "order":
            self.sequenceOrderAction.setChecked(True)
        elif self.parameter.sequence == "random":
            self.sequenceRandomAction.setChecked(True)
        else:
            self.sequenceReverseOrderAction.setChecked(True)



        k = 0
        for de in self.devices:
            if de.description() == self.musicEngine.audioOutput.device().description():
                break
            else:
                k += 1
        exec(f"self.device{k}Action.setChecked(True)")

        self.musicEngine.setVolume(0.8)
        self.centralWidget.volumeSlider.setValue(8)

        if os.path.exists(os.path.expanduser("~/.xting/collection.txt")):
            self.loadPlaylist()

        self.openFileAction.triggered.connect(self.openFileAction_)
        self.centralWidget.playorpauseButton.clicked.connect(self.playorpause_)
        self.playorpauseAction.triggered.connect(self.playorpause_)
        self.centralWidget.stopButton.clicked.connect(self.stop_)
        self.stopAction.triggered.connect(self.stop_)
        self.centralWidget.previousButton.clicked.connect(self.previous_)
        self.previousAction.triggered.connect(self.previous_)
        self.centralWidget.nextButton.clicked.connect(self.next_)
        self.nextAction.triggered.connect(self.next_)
        self.repeatAction.triggered.connect(self.repeat_)
        self.centralWidget.repeatButton.clicked.connect(self.repeat_)
        self.scanAction.triggered.connect(self.scanAction_)
        self.configurationAction.triggered.connect(self.configurationAction_)

        for q in self.deviceGroup.actions():
            exec(f"q.triggered.connect(self.changeDevice)")


        try:
            self.lrcShowxDock.restoreGeometry(self.parameter.lrcShowxDockGeometry)
        except:
            pass
        try:
            self.playlistDock.restoreGeometry(self.parameter.lrcShowxDockGeometry)
        except:
            pass
        try:
            self.albumCoverDock.restoreGeometry(self.parameter.lrcShowxDockGeometry)
        except:
            pass
        try:
            self.lrcEditorDock.restoreGeometry(self.parameter.lrcEditorDockGeometry)
        except:
            pass
        try:
            self.restoreState(self.parameter.windowState)
        except:
            pass
        try:
            self.restoreGeometry(self.parameter.windowGeometry)
        except:
            pass
        try:
            self.playlistDock.playlistWidget.allTable.horizontalHeader().restoreState(self.parameter.playlistDockAllTableState)
        except:
            pass
        try:
            self.playlistDock.playlistWidget.customTable.horizontalHeader().restoreState(self.parameter.playlistDockCustomTableState)
        except:
            pass

        self.timer.timeout.connect(self.progressForward)

        self.centralWidget.progressSlider.valueChanged.connect(self.adjustTrackPosition)

        self.centralWidget.volumeSlider.valueChanged.connect(self.volumeSlider_)

        self.systemTray.activated.connect(self.showorhideTray_)

        self.playlistDock.playlistWidget.allTable.cellDoubleClicked.connect(self.playorpauseByDoubleClick_)

        self.musicEngine.musicEquipment.playbackStateChanged.connect(self.playbackStateChanged_)

        self.loopTrackAction.toggled.connect(self.changeLoop)
        self.loopPlaylistAction.toggled.connect(self.changeLoop)
        self.sequenceOrderAction.toggled.connect(self.changeSequence)
        self.sequenceReverseOrderAction.toggled.connect(self.changeSequence)
        self.sequenceRandomAction.toggled.connect(self.changeSequence)

        self.aboutAppAction.triggered.connect(self.aboutAppAction_)
        self.aboutQtAction.triggered.connect(self.aboutQt_)
        self.quitAction.triggered.connect(self.quit_)


    def loadPlaylist(self):
        with open(os.path.join(self.appPrivatePath, "collection.txt"), "r") as f:
            self.collectionListTmp = f.readlines()
        self.playlistDock.playlistWidget.loadItems(self.collectionListTmp)


    def playbackStateChanged_(self, status):
        if len(self.playHistory) != 0:
            self.previousAction.setEnabled(True)
            self.centralWidget.previousButton.setEnabled(True)
        else:
            self.previousAction.setEnabled(False)
            self.centralWidget.previousButton.setEnabled(False)

        if status.value == 0: # stoped status
            if self.addToPlayHistory:
                try:
                    a = self.playHistory[-1]
                except:
                    self.playHistory.append(self.currentTrack.trackFile)
                else:
                    if a != self.currentTrack.trackFile:
                        self.playHistory.append(self.currentTrack.trackFile)
            else:
                self.addToPlayHistory = True

            self.centralWidget.playorpauseButton.setText(self.tr("Play"))
            self.playorpauseAction.setText(self.tr("Play"))
            self.centralWidget.stopButton.setEnabled(False)
            self.stopAction.setEnabled(False)
            self.centralWidget.progressSlider.setValue(0)
            self.centralWidget.progressSlider.setEnabled(False)
            self.centralWidget.lengthLabel.setText("--:--")
            self.centralWidget.timeLabel.setText("--:--")
            self.timer.stop()

            if self.schedule:
                self.scheduleNextTrack()
            else:
                self.showTrayInformation(0)
                self.schedule = True
        elif status.value == 1: # playing status
            self.centralWidget.playorpauseButton.setText(self.tr("Pause"))
            self.playorpauseAction.setText(self.tr("Pause"))
            self.centralWidget.stopButton.setEnabled(True)
            self.stopAction.setEnabled(True)
            self.nextAction.setEnabled(True)
            self.centralWidget.nextButton.setEnabled(True)
            self.repeatAction.setEnabled(True)
            self.centralWidget.repeatButton.setEnabled(True)
            self.showTrayInformation(1)
        elif status.value == 2: # paused status
            self.centralWidget.playorpauseButton.setText(self.tr("Play"))
            self.playorpauseAction.setText(self.tr("Play"))
            self.showTrayInformation(2)

    def scheduleNextTrack(self, callby = "auto"): # previous, playorpause, repeat or auto
        if self.playlistDock.playlistWidget.allTable.rowCount() == 0:
            return
        if callby == "playorpause":
            if self.musicEngine.musicEquipment.playbackState().value == 0:
                if self.sequenceRandomAction.isChecked():
                    tr = self.playlistDock.playlistWidget.allTable.rowCount()
                    self.currentNo = random.randint(0, tr - 1)
                else:
                    if len(self.playlistDock.playlistWidget.allTable.selectedItems()) == 0:
                        self.currentNo = 0
                    else:
                        self.currentNo = self.playlistDock.playlistWidget.allTable.currentRow()
                url = self.playlistDock.playlistWidget.allTable.item(self.currentNo, 8).text()
                self.musicEngine.add(url)
                self.currentTrack = track(url)
                self.playlistDock.playlistWidget.allTable.selectRow(self.currentNo)
            self.actualPlayOrPause()

        elif callby == "previous":
            pf = self.playHistory[-1]
            try:
                self.playHistory = self.playHistory[:-1]
            except:
                self.playHistory = []
            self.currentNo = self.getNumberFromFile(pf)
            self.musicEngine.add(pf)
            self.currentTrack = track(pf)
            self.playlistDock.playlistWidget.allTable.selectRow(self.currentNo)
            self.actualPlayOrPause()

        elif callby == "repeat":
            self.playlistDock.playlistWidget.allTable.selectRow(self.currentNo)
            self.actualPlayOrPause()

        else:
            if self.loopTrackAction.isChecked():
                self.playlistDock.playlistWidget.allTable.selectRow(self.currentNo)
                self.actualPlayOrPause()
            elif self.loopPlaylistAction.isChecked():
                if self.sequenceRandomAction.isChecked():
                    tr = self.playlistDock.playlistWidget.allTable.rowCount()
                    self.currentNo = random.randint(0, tr - 1)
                    url = self.playlistDock.playlistWidget.allTable.item(self.currentNo, 8).text()
                    self.musicEngine.add(url)
                    self.currentTrack = track(url)
                    self.playlistDock.playlistWidget.allTable.selectRow(self.currentNo)
                    self.actualPlayOrPause()
                elif self.sequenceOrderAction.isChecked():
                    if self.currentNo + 1 < self.playlistDock.playlistWidget.allTable.rowCount():
                        self.currentNo += 1
                        url = self.playlistDock.playlistWidget.allTable.item(self.currentNo, 8).text()
                        self.musicEngine.add(url)
                        self.currentTrack = track(url)
                        self.playlistDock.playlistWidget.allTable.selectRow(self.currentNo)
                        self.actualPlayOrPause()
                    else:
                        self.stop_()

                elif self.sequenceReverseOrderAction.isChecked():
                    if self.currentNo - 1 >= 0:
                        self.currentNo -= 1
                        url = self.playlistDock.playlistWidget.allTable.item(self.currentNo, 8).text()
                        self.musicEngine.add(url)
                        self.currentTrack = track(url)
                        self.playlistDock.playlistWidget.allTable.selectRow(self.currentNo)
                        self.actualPlayOrPause()
                    else:
                        self.stop_()

    def showTrayInformation(self, v):
        if self.parameter.trayIcon and self.parameter.trayInfo:
            if v == 1:
                self.systemTray.showMessage(self.tr("Status changed"), f"Now playing: {self.currentTrack.trackTitle} by {self.currentTrack.trackArtist}", QIcon("icon/logo.png"), 6000)
            elif v == 2:
                self.systemTray.showMessage(self.tr("Status changed"), f"Paused: {self.currentTrack.trackTitle} by {self.currentTrack.trackArtist}", QIcon("icon/logo.png"), 6000)
            else:
                self.systemTray.showMessage(self.tr("Status changed"), "Stopped", QIcon("icon/logo.png"), 6000)

    def openFileAction_(self):
        url, fil = QFileDialog.getOpenFileUrl(None, self.tr("choose a music file"), QUrl.fromLocalFile(self.parameter.collectionPath), "music files (*.mp3 *.flac)")
        if not url.isEmpty():
            self.musicEngine.add(url)
            self.currentTrack = track(url.toLocalFile())

            # self.currentNo = self.getNumberFromFile(self.currentTrack.trackFile)
            # if self.currentNo != -1:
            #     self.playlistDock.playlistWidget.allTable.selectRow(self.currentNo)
            self.actualPlayOrPause()

    def getNumberFromFile(self, f):
        for i in range(0, self.playlistDock.playlistWidget.allTable.rowCount()):
            if f == self.playlistDock.playlistWidget.allTable.item(i, 8).text():
                break
        return i

    def playorpauseByDoubleClick_(self, row, col):
        self.schedule = False
        url = self.playlistDock.playlistWidget.allTable.item(row, 8).text()
        self.currentNo = row
        self.musicEngine.add(url)
        self.currentTrack = track(url)
        self.actualPlayOrPause()
        self.schedule = True

    def next_(self):
        self.stop_()
        self.scheduleNextTrack("auto")

    def previous_(self):
        self.addToPlayHistory = False
        self.stop_()
        self.scheduleNextTrack("previous")

    def playorpause_(self):
        self.scheduleNextTrack("playorpause")

    def actualPlayOrPause(self):
        if self.musicEngine.isPlaying():
            self.timer.stop()
            self.musicEngine.pause()
        else:
            t = self.currentTrack.trackLength
            self.centralWidget.progressSlider.setEnabled(True)
            self.centralWidget.progressSlider.setRange(0, t * 1000)
            self.timer.start(1000)
            self.centralWidget.lengthLabel.setText(self.formatTrackLength(t))
            self.centralWidget.progressSlider.setValue(self.musicEngine.getPosition())
            self.centralWidget.timeLabel.setText(self.formatTrackLength(self.musicEngine.getPosition()))
            self.musicEngine.play()

    def stop_(self):
        self.schedule = False
        self.timer.stop()
        self.musicEngine.stop()

    def repeat_(self):
        self.stop_()
        self.scheduleNextTrack("repeat")

    def volumeSlider_(self, v):
        self.musicEngine.setVolume(v / 10)

    def progressForward(self):
        v = self.centralWidget.progressSlider.value()
        self.centralWidget.progressSlider.setValue(v + 1000)
        self.centralWidget.timeLabel.setText(self.formatTrackLength(int(v / 1000)))

    def adjustTrackPosition(self, v):
        if abs(v - self.musicEngine.getPosition()) < 1000:
            pass
        else:
            self.timer.stop()
            v = self.centralWidget.progressSlider.value()
            self.musicEngine.setPosition(v)
            self.timer.start(1000)
            self.positionChanged.emit()

    def scanAction_(self, recursive = False):
        musicList = glob.glob(os.path.join(self.parameter.collectionPath, "*.*"))

        t = ""
        for i in musicList:
            if mutagen.File(i) == None:
                continue
            i = i + "\n"
            t += i

        with open(os.path.join(self.appPrivatePath, "collection.txt"), "w") as f:
            f.write(t)

        self.loadPlaylist()

    def showorhideTray_(self, r):
        if r.value == 3:
            if self.isHidden():
                self.show()
            else:
                self.hide()

    def changeLoop(self, b):
        if b:
            self.parameter.loop = self.sender().iconText().lower()

    def changeSequence(self, b):
        if b:
            self.parameter.sequence = self.sender().iconText().lower()

    def changeDevice(self):
        deviceId = self.sender().objectName()
        self.musicEngine.setDevice(self.devices[int(deviceId)])


    def formatTrackLength(self, t):
        m, s = divmod(t, 60)
        if s < 10:
            return f"{m}:0{s}"
        else:
            return f"{m}:{s}"

    def aboutAppAction_(self):
        b = QMessageBox(self)
        b.setIconPixmap(QPixmap('icon/logo.png'))
        b.setWindowTitle(self.tr(f'About {QApplication.arguments()[0]}'))
        b.setText(f'Application: {QApplication.arguments()[0]}\n\nVersion: {QApplication.arguments()[1]}\n\nShort description: xting is a personal local music application, not special. Synced lyrics display is interesting\n\nAuthors: {QApplication.arguments()[2]}\n\nLicense: {QApplication.arguments()[3]}\n\nWebsite: {QApplication.arguments()[4]}')
        b.exec()

    def aboutQt_(self):
        QMessageBox.aboutQt(self, self.tr("About Qt"))

    def configurationAction_(self):
        settingDialog = configuration(self)
        settingDialog.playerConfig.playerPathBox.cpLine.setText(self.parameter.collectionPath)
        settingDialog.playerConfig.playerTrayBox.trayIcon.setChecked(self.parameter.trayIcon)
        settingDialog.playerConfig.playerTrayBox.trayIcon_(self.parameter.trayIcon)
        settingDialog.playerConfig.playerTrayBox.closeNotQuit.setChecked(self.parameter.closeNotQuit)
        settingDialog.playerConfig.playerTrayBox.trayInfo.setChecked(self.parameter.trayInfo)

        settingDialog.lrcShowxConfig.appearenceBox.tlLine.setValue(self.parameter.topMarginLines)
        settingDialog.lrcShowxConfig.appearenceBox.lmLine.setValue(self.parameter.lineMargin)

        settingDialog.lrcShowxConfig.appearenceBox.bgEffectLabel.setStyleSheet("QLabel { background-color: " + self.parameter.backGroundColor + "; color: white; }")
        settingDialog.lrcShowxConfig.appearenceBox.fgEffectLabel.setStyleSheet("QLabel { background-color: " + self.parameter.foreGroundColor + "; color: white; }")
        settingDialog.lrcShowxConfig.appearenceBox.hlEffectLabel.setStyleSheet("QLabel { background-color: " + self.parameter.highLightColor + "; color: white; }")
        ff = QFont()
        ff.fromString(self.parameter.lrcFont)
        settingDialog.lrcShowxConfig.appearenceBox.fontEffectLabel.setFont(ff)

        settingDialog.lrcShowxConfig.lrcPathBox.llLine.setText(self.parameter.lrcLocalPath)
        settingDialog.lrcShowxConfig.lrcPathBox.auto.setChecked(self.parameter.autoSaveLrc)
        r = settingDialog.exec()
        if r == 1:  # accepted
            self.parameter.collectionPath = settingDialog.playerConfig.playerPathBox.cpLine.text()
            self.parameter.trayIcon = settingDialog.playerConfig.playerTrayBox.trayIcon.isChecked()
            self.systemTray.setVisible(self.parameter.trayIcon)
            self.parameter.closeNotQuit = settingDialog.playerConfig.playerTrayBox.closeNotQuit.isChecked()
            self.parameter.trayInfo = settingDialog.playerConfig.playerTrayBox.trayInfo.isChecked()

            self.parameter.lrcLocalPath = self.lrcShowxDock.lrcShowxWidget.lrcLocalPath = settingDialog.lrcShowxConfig.lrcPathBox.llLine.text()
            self.parameter.autoSaveLrc = self.lrcShowxDock.lrcShowxWidget.autoSaveLrc = settingDialog.lrcShowxConfig.lrcPathBox.auto.isChecked()

            if self.parameter.topMarginLines != settingDialog.lrcShowxConfig.appearenceBox.tlLine.value() or self.parameter.lineMargin != settingDialog.lrcShowxConfig.appearenceBox.lmLine.value() or settingDialog.lrcShowxConfig.appearenceBox.fontEffectLabel.font().toString != self.parameter.lrcFont:
                self.parameter.topMarginLines = self.lrcShowxDock.lrcShowxWidget.topMarginLines = settingDialog.lrcShowxConfig.appearenceBox.tlLine.value()
                self.parameter.lineMargin = self.lrcShowxDock.lrcShowxWidget.lineMargin = settingDialog.lrcShowxConfig.appearenceBox.lmLine.value()
                self.parameter.lrcFont = self.lrcShowxDock.lrcShowxWidget.lrcFont = settingDialog.lrcShowxConfig.appearenceBox.fontEffectLabel.font().toString()
                self.lrcShowxDock.lrcShowxWidget.initFont()
                self.lrcShowxDock.lrcShowxWidget.playbackStateChanged_(self.musicEngine.getPlaybackState())

            if self.parameter.backGroundColor != settingDialog.lrcShowxConfig.appearenceBox.backGroundColor or self.parameter.foreGroundColor != settingDialog.lrcShowxConfig.appearenceBox.foreGroundColor or self.parameter.highLightColor != settingDialog.lrcShowxConfig.appearenceBox.highLightColor:
                self.parameter.backGroundColor = self.lrcShowxDock.lrcShowxWidget.backGroundColor = settingDialog.lrcShowxConfig.appearenceBox.backGroundColor
                self.parameter.foreGroundColor = self.lrcShowxDock.lrcShowxWidget.foreGroundColor = settingDialog.lrcShowxConfig.appearenceBox.foreGroundColor
                self.parameter.highLightColor = self.lrcShowxDock.lrcShowxWidget.highLightColor = settingDialog.lrcShowxConfig.appearenceBox.highLightColor

        self.parameter.configurationSplitterState = settingDialog.splitter.saveState()

    def beforeClose(self):
        self.systemTray.hide()

        self.parameter.windowState = self.saveState()
        self.parameter.windowGeometry = self.saveGeometry()
        self.parameter.lrcShowxDockGeometry = self.lrcShowxDock.saveGeometry()
        self.parameter.playlistDockGeometry = self.playlistDock.saveGeometry()
        self.parameter.albumCoverDockGeometry = self.albumCoverDock.saveGeometry()
        self.parameter.lrcEditorDockGeometry = self.lrcEditorDock.saveGeometry()
        self.parameter.playlistDockAllTableState = self.playlistDock.playlistWidget.allTable.horizontalHeader().saveState()
        self.parameter.playlistDockCustomTableState = self.playlistDock.playlistWidget.customTable.horizontalHeader().saveState()


        self.parameter.save()

    def quit_(self):
        self.parameter.doQuit = self.parameter.closeNotQuit
        self.close()

    def closeEvent(self, e):
        if self.parameter.doQuit:
            self.beforeClose()
            e.accept()
        else:
            if self.parameter.trayIcon and self.parameter.closeNotQuit:
                e.ignore()
                self.hide()
            else:
                self.beforeClose()
                e.accept()
