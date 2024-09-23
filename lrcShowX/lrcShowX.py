#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: lrcShow-X.py


from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class lrcShowX(QTextBrowser):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setText("lrcShow-X is not available yet, temporarily serving as an easy guide. Modify the collection path in config file ($HOME/.xting/xting.conf), then click Tools-Scan collection, app will load your media files (mp3 and flac temporarily) in 'All tracks' tab in playlist dock, now you can listen music with xting app. It's a personal app, if you don't like it, forget it!")
