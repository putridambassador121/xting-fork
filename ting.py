#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: ting.py

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtMultimedia import QMediaDevices
from PyQt6.QtCore import QLocale, QTranslator
from mainWindow import mainWindow
import sys, os



if __name__ == "__main__":

    appdir = os.path.join(os.path.expanduser("~"), ".ting")
    if not os.path.isdir(appdir):
        os.mkdir(appdir)


    app = QApplication(sys.argv)

    devices = QMediaDevices.audioOutputs()

    locale = QLocale.system().name()
    translator = QTranslator()
    if translator.load(f'translations/{locale}/ting.qm'):
        app.installTranslator(translator)
    else:
        print(f'No translation file found for {locale}')

    w = mainWindow(devices)
    w.show()
    sys.exit(app.exec())
