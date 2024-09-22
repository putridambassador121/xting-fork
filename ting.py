#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: ting.py

from PyQt6.QtWidgets import QApplication, QMessageBox
from mainWindow import mainWindow
import sys, os



if __name__ == "__main__":

    appdir = os.path.join(os.path.expanduser("~"), ".ting")
    if not os.path.isdir(appdir):
        os.mkdir(appdir)

    app = QApplication(sys.argv)
    w = mainWindow()
    w.show()
    sys.exit(app.exec())
