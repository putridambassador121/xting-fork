#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: track.py

import sys, os

from mutagen.mp3 import MP3

from mutagen.flac import FLAC


class track:

    def __init__(self, f):

        self.trackFile = f

        if os.path.splitext(f)[1].lower() == ".mp3":
            self.trackType = "mp3"
            self.audio = MP3(f)
            try:
                self.trackTitle = str(self.audio["TIT2"].text[0])
            except:
                 self.trackTitle = "unknow"
            try:
                self.trackAlbum = str(self.audio["TALB"].text[0])
            except:
                self.trackAlbum = "unknow"
            try:
                self.trackArtist = str(self.audio["TPE1"].text[0])
            except:
                self.trackArtist = "unknow"
            try:
                self.trackDate = str(self.audio["TDRC"].text[0])
            except:
                self.trackDate = "unknow"
            try:
                self.trackBitrate = int(self.audio.info.bitrate)
            except:
                self.trackBitrate = 0
            try:
                self.trackSamplerate = int(self.audio.info.sample_rate)
            except:
                self.trackSamplerate = 0
            try:
                self.trackLength = int(self.audio.info.length)
            except:
                self.trackLength = 0

        elif os.path.splitext(f)[1].lower() == ".flac":
            self.trackType = "flac"
            self.audio = FLAC(f)
            try:
                self.trackTitle = self.audio["title"][0]
            except:
                self.trackTitle = "unknow"
            try:
                self.trackAlbum = self.audio["album"][0]
            except:
                self.trackAlbum = "unknow"
            try:
                self.trackArtist = self.audio["artist"][0]
            except:
                self.trackArtist = "unknow"
            try:
                self.trackDate = self.audio["date"][0]
            except:
                self.trackDate = "unknow"
            try:
                self.trackBitrate = int(self.audio.info.bitrate)
            except:
                self.trackBitrate = 0
            try:
                self.trackSamplerate = int(self.audio.info.sample_rate)
            except:
                self.trackSamplerate = 0
            try:
                self.trackLength = int(self.audio.info.length)
            except:
                self.trackLength = 0
        else:
            self.trackType = "unknow"
            self.audio = None
            self.trackTitle = "unknow"
            self.trackAlbum = "unknow"
            self.trackArtist = "unknow"
            self.trackDate = "unknow"
            self.trackBitrate = 0
            self.trackSamplerate = 0
            self.trackLength = 0

