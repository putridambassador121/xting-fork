#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: track.py

import sys, os, mutagen

from mutagen.mp3 import MP3, HeaderNotFoundError
# from mutagen.mp4 import MP4
from mutagen.id3 import ID3, ID3NoHeaderError

from mutagen.flac import FLAC, FLACNoHeaderError

from mutagen.oggvorbis import OggVorbis

from mutagen.id3 import TIT2
from mutagen.mp4 import MP4


class track:

    def __init__(self, f):

        self.trackFile = f

        if os.path.splitext(f)[1].lower() == ".mp3":
            self.loadMp3()
        elif os.path.splitext(f)[1].lower() == ".flac":
            self.loadFlac()
        elif os.path.splitext(f)[1].lower() == ".ogg":
            self.loadOgg()
        elif os.path.splitext(f)[1].lower() == ".m4a":
            self.loadM4a()
        else:
            self.loadUnkown()

    """
    Changed the way these audio loader functions worked, because it seems kinda strange and
    counter intuitive to write 'unknown' as metadata values to the file itself, and also it just makes it
    hard to use multithreading (because, race conditions, apparently), and so it's read only for 
    metadata and returns of the 'unknown' in cases where the value is None
    
    """

    def loadM4a(self):
        self.trackType = "m4a"
        try:
            self.audio = MP4(self.trackFile)
        except Exception:
            print(f"Invalid or not an M4A/MP4 file: {self.trackFile}")
            self.audio = None
            return

        def safe_get(tag):
            return self.audio.tags.get(tag, ["Unknown"])[0] if self.audio and self.audio.tags else "Unknown"

        self.trackTitle = safe_get("\xa9nam")
        self.trackAlbum = safe_get("\xa9alb")
        self.trackArtist = safe_get("\xa9ART")
        self.trackDate = safe_get("\xa9day")

        if self.audio and self.audio.info:
            self.trackBitrate = int(getattr(self.audio.info, 'bitrate', 0))
            self.trackSamplerate = int(getattr(self.audio.info, 'sample_rate', 0))
            self.trackLength = int(getattr(self.audio.info, 'length', 0))
        else:
            self.trackBitrate = int(getattr(self.audio.info, 'bitrate', 0))
            self.trackSamplerate = int(getattr(self.audio.info, 'sample_rate', 0))
            self.trackLength = int(getattr(self.audio.info, 'length', 0))




    # def loadM4a(self):
    #     self.trackType = "m4a"
    #     self.audio = mutagen.File(self.trackFile, easy = True)
    #     try:
    #         self.trackTitle = self.audio["title"][0]
    #     except:
    #         self.trackTitle = "unknow"
    #     try:
    #         self.trackAlbum = self.audio["album"][0]
    #     except:
    #         self.trackAlbum = "unknow"
    #     try:
    #         self.trackArtist = self.audio["artist"][0]
    #     except:
    #         self.trackArtist = "unknow"
    #     try:
    #         self.trackDate = self.audio["date"][0]
    #     except:
    #         self.trackDate = "unknow"
    #     try:
    #         self.trackBitrate = int(self.audio.info.bitrate)
    #     except:
    #         self.trackBitrate = 0
    #     try:
    #         self.trackSamplerate = int(self.audio.info.sample_rate)
    #     except:
    #         self.trackSamplerate = 0
    #     try:
    #         self.trackLength = int(self.audio.info.length)
    #     except:
    #         self.trackLength = 0
    #     try:
    #         self.trackBitrate = int(self.audio.info.bitrate)
    #     except:
    #         self.trackBitrate = 0
    #     try:
    #         self.trackSamplerate = int(self.audio.info.sample_rate)
    #     except:
    #         self.trackSamplerate = 0
    #     try:
    #         self.trackLength = int(self.audio.info.length)
    #     except:
    #         self.trackLength = 0

    def loadOgg(self):
        self.trackType = "ogg"
        try:
            self.audio = OggVorbis(self.trackFile)
        except Exception:
            print(f"Invalid or not an OGG file: {self.trackFile}")
            self.audio = None
            return

        def safe_get(tag):
            return self.audio.get(tag, ["Unknown"])[0] if self.audio else "Unknown"

        self.trackTitle = safe_get("title")
        self.trackAlbum = safe_get("album")
        self.trackArtist = safe_get("artist")
        self.trackDate = safe_get("date")

        if self.audio and self.audio.info:
            self.trackBitrate = int(getattr(self.audio.info, 'bitrate', 0))
            self.trackSamplerate = int(getattr(self.audio.info, 'sample_rate', 0))
            self.trackLength = int(getattr(self.audio.info, 'length', 0))
        else:
            self.trackBitrate = int(getattr(self.audio.info, 'bitrate', 0))
            self.trackSamplerate = int(getattr(self.audio.info, 'sample_rate', 0))
            self.trackLength = int(getattr(self.audio.info, 'length', 0))







    # def loadOgg(self):
    #     self.trackType = "ogg"
    #     self.audio = OggVorbis(self.trackFile)
    #     self.trackTitle = self.audio.tags.get(("TITLE"), ["unknow"])[0]
    #     self.trackAlbum = self.audio.tags.get(("ALBUM"), ["unknow"])[0]
    #     self.trackArtist = self.audio.tags.get(("ARTIST"), ["unknow"])[0]
    #     self.trackDate = self.audio.tags.get(("DATE"), ["unknow"])[0]
    #     try:
    #         self.trackBitrate = int(self.audio.info.bitrate)
    #     except:
    #         self.trackBitrate = 0
    #     try:
    #         self.trackSamplerate = int(self.audio.info.sample_rate)
    #     except:
    #         self.trackSamplerate = 0
    #     try:
    #         self.trackLength = int(self.audio.info.length)
    #     except:
    #         self.trackLength = 0

    def loadUnknown(self):
        self.trackType = "unknown"
        self.audio = None
        self.trackTitle = "unknown"
        self.trackAlbum = "unknown"
        self.trackArtist = "unknown"
        self.trackDate = "unknown"
        self.trackBitrate = 0
        self.trackSamplerate = 0
        self.trackLength = 0



    def loadFlac(self):
        self.trackType = "flac"
        try:
            self.audio = FLAC(self.trackFile)
        except Exception:
            print(f"Invalid or not a FLAC file: {self.trackFile}")
            self.audio = None
            return

        def safe_get(tag):
            return self.audio.get(tag, ["Unknown"])[0] if self.audio else "Unknown"

        self.trackTitle = safe_get("title")
        self.trackAlbum = safe_get("album")
        self.trackArtist = safe_get("artist")
        self.trackDate = safe_get("date")

        if self.audio and self.audio.info:
            self.trackBitrate = int(getattr(self.audio.info, 'bitrate', 0))
            self.trackSamplerate = int(getattr(self.audio.info, 'sample_rate', 0))
            self.trackLength = int(getattr(self.audio.info, 'length', 0))
        else:
            self.trackBitrate = int(getattr(self.audio.info, 'bitrate', 0)) if self.audio else 0  
            self.trackSamplerate = int(getattr(self.audio.info, 'sample_rate', 0)) if self.audio else 0
            self.trackLength = int(getattr(self.audio.info, 'length', 0)) if self.audio else 0








    # def loadFlac(self):
    #     self.trackType = "flac"
    #     try:
    #         self.audio = FLAC(self.trackFile)
    #     except FLACNoHeaderError:
    #         print(f"Arquivo inválido ou não é um FLAC: {self.trackFile}")
    #         self.audio = None
    #         return

    #     # Função segura pra pegar tags
    #     def safe_get(tag):
    #         return self.audio.get(tag, None)[0] if self.audio else "Unknown"

        
    #     self.trackTitle = safe_get("title")
    #     self.trackAlbum = safe_get("album")
    #     self.trackArtist = safe_get("artist")
    #     self.trackDate = str(safe_get("date"))

    #     # print(self.trackTitle)
    #     # print(self.trackAlbum)
    #     # print(self.trackArtist)
    #     # print(self.trackDate)
    #     # print(round(1.6))
    #     self.trackBitrate = int(getattr(self.audio.info, 'bitrate', 0)) if self.audio else 0  
    #     self.trackSamplerate = int(getattr(self.audio.info, 'sample_rate', 0)) if self.audio else 0
    #     self.trackLength = int(getattr(self.audio.info, 'length', 0)) if self.audio else 0

    
    def loadMp3(self):
        self.trackType = "mp3"
        try:
            self.audio = MP3(self.trackFile)
        except HeaderNotFoundError:
            print(f"Invalid or not an MP3: {self.trackFile}")
            self.audio = None
            return

        try:
            tags = ID3(self.trackFile)
        except ID3NoHeaderError:
            tags = None

        def safe_get(tag):
            return tags.get(tag).text[0] if tags and tags.get(tag) else "Unknown"

        self.trackTitle = safe_get("TIT2")
        self.trackAlbum = safe_get("TALB")
        self.trackArtist = safe_get("TPE1")
        self.trackDate = str(safe_get("TDRC"))

 
        if self.audio and self.audio.info:
            self.trackBitrate = int(getattr(self.audio.info, 'bitrate', 0))
            self.trackSamplerate = int(getattr(self.audio.info, 'sample_rate', 0))
            self.trackLength = int(getattr(self.audio.info, 'length', 0))
        else:
            self.trackBitrate = int(getattr(self.audio.info, 'bitrate', 0))
            self.trackSamplerate = int(getattr(self.audio.info, 'sample_rate', 0))
            self.trackLength = int(getattr(self.audio.info, 'length', 0))

        # print(f"Loaded: {self.trackTitle} | Length: {self.trackLength}s")


    def setTitleTag(self, v):
        if self.trackType == "mp3":
            self.audio['TIT2'] = TIT2(encoding = 3, text = v)
            self.audio.save()
        elif self.trackType == "flac" or self.trackType == "m4a":
            self.audio["title"] = v
            self.audio.save()
        elif  self.trackType == "ogg":
            self.audio["TITLE"] = v
            self.audio.save()
        else:
            print("Unsupported file type")

    def setAlbumTag(self, v):
        if self.trackType == "mp3":
            self.audio['TALB'] = TIT2(encoding = 3, text = v)
            self.audio.save()
        elif self.trackType == "flac" or self.trackType == "m4a":
            self.audio["album"] = v
            self.audio.save()
        elif  self.trackType == "ogg":
            self.audio["ALBUM"] = v
            self.audio.save()
        else:
            print("Unsupported file type")

    def setArtistTag(self, v):
        if self.trackType == "mp3":
            self.audio['TPE1'] = TIT2(encoding = 3, text = v)
            self.audio.save()
        elif self.trackType == "flac" or self.trackType == "m4a":
            self.audio["artist"] = v
            self.audio.save()
        elif  self.trackType == "ogg":
            self.audio["ARTIST"] = v
            self.audio.save()
        else:
            print("Unsupported file type")

    def setDateTag(self, v):
        if self.trackType == "mp3":
            self.audio['TDRC'] = TIT2(encoding = 3, text = v)
            self.audio.save()
        elif self.trackType == "flac" or self.trackType == "m4a":
            self.audio["date"] = v
            self.audio.save()
        elif  self.trackType == "ogg":
            self.audio["DATE"] = v
            self.audio.save()
        else:
            print("Unsupported file type")

    def searchOnline(self):
        pass