#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: configuration.py


import os, sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class configuration(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        l = [self.tr("Player"), self.tr("lrcShow-X"), self.tr("Shortcuts")]
        self.catalogList = QListWidget(self)
        for i in l:
            self.catalogList.addItem(i)
        self.catalogList.setCurrentRow(0)

        self.stackArea = QStackedWidget(self)
        self.playerConfig = playerConfig(self)
        self.stackArea.addWidget(self.playerConfig)
        self.lrcShowxConfig = lrcShowxConfig(self)
        self.stackArea.addWidget(self.lrcShowxConfig)
        self.shortcutConfig = shortcutConfig(self)
        self.stackArea.addWidget(self.shortcutConfig)

        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.catalogList)
        self.splitter.addWidget(self.stackArea)

        state = self.parent.parameter.configurationSplitterState
        try:
            self.splitter.restoreState(state)
        except:
            pass

        buttonBox = QDialogButtonBox(self)
        cancelButton = QPushButton(self.tr("Cancel"))
        okButton = QPushButton(self.tr("OK"))
        buttonBox.addButton(cancelButton, QDialogButtonBox.ButtonRole.RejectRole)
        buttonBox.addButton(okButton, QDialogButtonBox.ButtonRole.AcceptRole)

        mainLayout = QVBoxLayout(None)
        mainLayout.addWidget(self.splitter)
        mainLayout.addStretch(0)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)


        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.catalogList.itemActivated.connect(self.switchStack)


    def switchStack(self, i):
        if i.text() == "Player":
            self.stackArea.setCurrentIndex(0)
        elif i.text() == "lrcShow-X":
            self.stackArea.setCurrentIndex(1)
        else:
            self.stackArea.setCurrentIndex(2)

##########################################################
class playerConfig(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        mainLayout = QVBoxLayout(None)

        self.playerPathBox = playerPathBox(self)
        self.playerTrayBox = playerTrayBox(self)
        mainLayout.addWidget(self.playerPathBox)
        mainLayout.addWidget(self.playerTrayBox)
        self.setLayout(mainLayout)

class playerPathBox(QGroupBox):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setTitle(self.tr("Path"))
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        mainLayout = QGridLayout(None)

        self.cpLabel = QLabel("Collection path:")
        self.cpLine = QLineEdit(self)
        self.cpLine.setReadOnly(True)
        self.cpButton = QPushButton("...", self)
        mainLayout.addWidget(self.cpLabel, 0, 0)
        mainLayout.addWidget(self.cpLine, 0, 1)
        mainLayout.addWidget(self.cpButton, 0, 2)

        self.setLayout(mainLayout)

        self.cpButton.clicked.connect(self.getLocalPath)

    def getLocalPath(self):
        v = QFileDialog.getExistingDirectoryUrl(self, self.tr("Collection path"), QUrl.fromLocalFile(self.parent.parent.parent.parameter.collectionPath))
        v = v.toLocalFile()
        if v:
            self.cpLine.setText(v)

class playerTrayBox(QGroupBox):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setTitle(self.tr("System tray"))
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        mainLayout = QVBoxLayout(None)

        self.trayIcon = QCheckBox(self.tr("Enable system tray"), self)
        self.closeNotQuit = QCheckBox(self.tr("Do not quit when close the window"), self)
        self.trayInfo = QCheckBox(self.tr("Display the information from application"), self)
        mainLayout.addWidget(self.trayIcon)
        mainLayout.addWidget(self.closeNotQuit)
        mainLayout.addWidget(self.trayInfo)

        self.setLayout(mainLayout)

        self.trayIcon.toggled.connect(self.trayIcon_)

    def trayIcon_(self, b):
        self.closeNotQuit.setEnabled(b)
        self.trayInfo.setEnabled(b)

##########################################################
class lrcShowxConfig(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        mainLayout = QVBoxLayout(None)

        self.lrcPathBox = lrcPathBox(self)
        self.appearenceBox = appearenceBox(self)
        mainLayout.addWidget(self.lrcPathBox)
        mainLayout.addWidget(self.appearenceBox)
        self.setLayout(mainLayout)


class lrcPathBox(QGroupBox):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setTitle(self.tr("Path"))
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        mainLayout = QGridLayout(None)

        self.llLabel = QLabel("Lrc search/save path:")
        self.llLine = QLineEdit(self)
        self.llLine.setReadOnly(True)
        self.llButton = QPushButton("...", self)
        mainLayout.addWidget(self.llLabel, 0, 0)
        mainLayout.addWidget(self.llLine, 0, 1)
        mainLayout.addWidget(self.llButton, 0, 2)

        self.auto = QCheckBox(self.tr("Auto save lrc from net"), self)
        mainLayout.addWidget(self.auto, 1, 0)

        self.setLayout(mainLayout)

        self.llButton.clicked.connect(self.getLocalPath)


    def getLocalPath(self):
        v = QFileDialog.getExistingDirectoryUrl(self, self.tr("Lrc search/save path"), QUrl.fromLocalFile(self.parent.parent.parent.parameter.lrcLocalPath))
        v = v.toLocalFile()
        if v:
            self.llLine.setText(v)


class appearenceBox(QGroupBox):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setTitle(self.tr("Appearence"))
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.backGroundColor = self.parent.parent.parent.parameter.backGroundColor
        self.foreGroundColor = self.parent.parent.parent.parameter.foreGroundColor
        self.highLightColor = self.parent.parent.parent.parameter.highLightColor

        mainLayout = QGridLayout(None)

        self.tlLabel = QLabel(self.tr("Highlight line from top:"), self)
        self.tlLine = QSpinBox(self)
        self.tlLine.setMaximum(20)
        mainLayout.addWidget(self.tlLabel, 0, 0)
        mainLayout.addWidget(self.tlLine, 0, 1)

        mainLayout.addItem(QSpacerItem(10, 10), 1, 0)

        self.lmLabel = QLabel(self.tr("Line space:"), self)
        self.lmLine = QSpinBox(self)
        self.lmLine.setMaximum(50)
        mainLayout.addWidget(self.lmLabel, 2, 0)
        mainLayout.addWidget(self.lmLine, 2, 1)

        mainLayout.addItem(QSpacerItem(10, 20), 3, 0)

        self.bgLabel = QLabel(self.tr("Background color:"), self)
        self.bgEffectLabel = QLabel(self)
        self.bgButton = QPushButton("...")
        self.bgButton.setObjectName("bg")
        mainLayout.addWidget(self.bgLabel, 4, 0)
        mainLayout.addWidget(self.bgEffectLabel, 4, 1)
        mainLayout.addWidget(self.bgButton, 4, 2)
        self.fgLabel = QLabel(self.tr("Foreground color:"), self)
        self.fgEffectLabel = QLabel(self)
        self.fgButton = QPushButton("...")
        self.fgButton.setObjectName("fg")
        mainLayout.addWidget(self.fgLabel, 5, 0)
        mainLayout.addWidget(self.fgEffectLabel, 5, 1)
        mainLayout.addWidget(self.fgButton, 5, 2)
        self.hlLabel = QLabel(self.tr("Highlight color:"), self)
        self.hlEffectLabel = QLabel(self)
        self.hlButton = QPushButton("...")
        self.hlButton.setObjectName("hl")
        mainLayout.addWidget(self.hlLabel, 6, 0)
        mainLayout.addWidget(self.hlEffectLabel, 6, 1)
        mainLayout.addWidget(self.hlButton, 6, 2)

        mainLayout.addItem(QSpacerItem(10, 20), 7, 0)

        self.fontLabel = QLabel(self.tr("Lyrics font:"), self)
        self.fontEffectLabel = QLabel(self.tr("The music is wonderful!"), self)

        self.fontButton = QPushButton("...")

        mainLayout.addWidget(self.fontLabel, 8, 0)
        mainLayout.addWidget(self.fontEffectLabel, 8, 1)
        mainLayout.addWidget(self.fontButton, 8, 2)



        self.setLayout(mainLayout)

        self.bgButton.clicked.connect(self.changeColor)
        self.fgButton.clicked.connect(self.changeColor)
        self.hlButton.clicked.connect(self.changeColor)

        self.fontButton.clicked.connect(self.changeFont)

    def changeFont(self):

        font, ok = QFontDialog.getFont(QFont(self.parent.parent.parent.parameter.lrcFont), self)
        if ok:
            self.fontEffectLabel.setFont(font)



    def changeColor(self):
        obName = self.sender().objectName()
        if  obName == "bg":
            initColor = QColor(self.parent.parent.parent.parameter.backGroundColor)
            title = "Pick a background color"
        elif obName == "fg":
            initColor = QColor(self.parent.parent.parent.parameter.foreGroundColor)
            title = "Pick a foreground color"
        else:
            initColor = QColor(self.parent.parent.parent.parameter.highLightColor)
            title = "Pick a highlight color"
        color = QColorDialog.getColor(initColor, self, title)

        if color.isValid:
            tt = "QLabel { background-color: " + color.name() + "; color: white; }"
            if  obName == "bg":
                self.backGroundColor = color.name()
                self.bgEffectLabel.setStyleSheet(tt)
            elif obName == "fg":
                self.foreGroundColor = color.name()
                self.fgEffectLabel.setStyleSheet(tt)
            else:
                self.highLightColor = color.name()
                self.hlEffectLabel.setStyleSheet(tt)



##########################################################

class shortcutConfig(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = configuration(None)
    w.show()

    sys.exit(app.exec())
