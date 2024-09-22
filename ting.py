#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: ting.py

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtMultimedia import QMediaDevices
from mainWindow import mainWindow
import sys, os



if __name__ == "__main__":

    appdir = os.path.join(os.path.expanduser("~"), ".ting")
    if not os.path.isdir(appdir):
        os.mkdir(appdir)


    app = QApplication(sys.argv)

    devices = QMediaDevices.audioOutputs()

    w = mainWindow(devices)
    w.show()
    sys.exit(app.exec())
