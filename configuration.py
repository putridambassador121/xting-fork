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
        mainLayout.addWidget(self.lrcPathBox)
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

        self.setLayout(mainLayout)

        self.llButton.clicked.connect(self.getLocalPath)


    def getLocalPath(self):
        v = QFileDialog.getExistingDirectoryUrl(self, self.tr("Lrc search/save path"), QUrl.fromLocalFile(self.parent.parent.parent.parameter.lrcLocalPath))
        v = v.toLocalFile()
        if v:
            self.llLine.setText(v)


##########################################################

class shortcutConfig(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = configuration()
    w.show()

    sys.exit(app.exec())
