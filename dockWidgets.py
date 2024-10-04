#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: dockWidgets.py


import os, sys, re
from track import track
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from lrcShowX.lrcShowX import lrcShowX
from mutagen.flac import FLAC, Picture
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error


class lrcShowxDock(QDockWidget):

    def __init__(self, title, parent = None):
        super().__init__(title)
        self.parent = parent
        self.lrcShowxWidget = lrcShowX(self)
        self.setWidget(self.lrcShowxWidget)
        self.setFloating(False)


class lrcEditorDock(QDockWidget):

    def __init__(self, title, parent = None):
        super().__init__(title)
        self.parent = parent
        self.setWindowTitle = title
        self.lrcEditorWidget = lrcEditorWidget(self)
        self.setWidget(self.lrcEditorWidget)
        self.setFloating(False)

class lrcEditorWidget(QWidget):

    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout(None)

        self.editLrc = QPlainTextEdit(self)
        self.editLrc.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.lrcFile = None

        self.initMenu()
        self.initToolBar()

        layout.addWidget(self.lrcEditMenu)
        layout.addWidget(self.toolBar)
        layout.addWidget(self.editLrc)

        self.setLayout(layout)

        self.newAction.triggered.connect(self.newAction_)
        self.openAction.triggered.connect(self.openAction_)
        self.saveAction.triggered.connect(self.saveAction_)
        self.saveAsAction.triggered.connect(self.saveAsAction_)

        self.editLrc.undoAvailable.connect(self.undoAction.setEnabled)
        self.editLrc.redoAvailable.connect(self.redoAction.setEnabled)
        self.editLrc.copyAvailable.connect(self.cutAction.setEnabled)
        self.editLrc.copyAvailable.connect(self.copyAction.setEnabled)

        self.undoAction.triggered.connect(self.editLrc.undo)
        self.redoAction.triggered.connect(self.editLrc.redo)
        self.cutAction.triggered.connect(self.editLrc.cut)
        self.copyAction.triggered.connect(self.editLrc.copy)
        self.pasteAction.triggered.connect(self.editLrc.paste)
        self.clearAction.triggered.connect(self.editLrc.clear)

        self.insertAction.triggered.connect(self.insertAction_)
        self.removeTagsAction.triggered.connect(self.removeTagsAction_)
        self.removeAllTagsAction.triggered.connect(self.removeAllTagsAction_)
        self.removeAllBlankLinesAction.triggered.connect(self.removeAllBlankLinesAction_)
        self.removeWhiteSpaceAction.triggered.connect(self.removeWhiteSpaceAction_)

    def initMenu(self):
        self.lrcEditMenu = QMenuBar(self)
        fileMenu = self.lrcEditMenu.addMenu(self.tr("File"))
        self.newAction = QAction(self.tr("New"), self)
        self.openAction = QAction(self.tr("Open..."), self)
        self.saveAction = QAction(self.tr("Save"), self)
        self.saveAsAction = QAction(self.tr('Save as...'), self)
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        editMenu = self.lrcEditMenu.addMenu(self.tr("Edit"))
        self.undoAction = QAction(self.tr("Undo"), self)
        self.undoAction.setEnabled(False)
        self.redoAction = QAction(self.tr("Redo"), self)
        self.redoAction.setEnabled(False)
        self.cutAction = QAction(self.tr("Cut"), self)
        self.cutAction.setEnabled(False)
        self.copyAction = QAction(self.tr("Copy"), self)
        self.copyAction.setEnabled(False)
        self.pasteAction = QAction(self.tr("Paste"), self)
        self.pasteAction.setEnabled(self.editLrc.canPaste())
        self.clearAction = QAction(self.tr("Clear"), self)
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)
        editMenu.addSeparator()
        editMenu.addAction(self.cutAction)
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addSeparator()
        editMenu.addAction(self.clearAction)

        toolMenu = self.lrcEditMenu.addMenu(self.tr("Tool"))
        self.insertAction = QAction(self.tr("Insert a tag"), self)
        self.removeTagsAction = QAction(self.tr("Remove all tags in current line"), self)
        self.removeAllTagsAction = QAction(self.tr("Remove all tags"), self)
        self.removeAllBlankLinesAction = QAction(self.tr("Remove blank lines"), self)
        self.removeWhiteSpaceAction = QAction(self.tr("Remove whitespace character at start/end of lines"), self)
        toolMenu.addAction(self.insertAction)
        toolMenu.addAction(self.removeTagsAction)
        toolMenu.addAction(self.removeAllTagsAction)
        toolMenu.addAction(self.removeAllBlankLinesAction)
        toolMenu.addAction(self.removeWhiteSpaceAction)

    def initToolBar(self):
        self.toolBar = QToolBar(self)
        self.toolBar.addAction(self.insertAction)
        self.toolBar.addAction(self.removeTagsAction)

    def newAction_(self):
        self.editLrc.clear()
        self.editLrc.setPlainText("[ti:]\n[ar:]\n[al:]\n[by:]\n[offset: 0]\n\n")

    def openAction_(self):
        url, fil = QFileDialog.getOpenFileUrl(None, self.tr("choose a music file"), QUrl.fromLocalFile(self.parent.parent.parameter.lrcLocalPath), "lrc files (*.lrc)")
        if not url.isEmpty():
            with open(url.toLocalFile(), "r") as f:
                text = f.read()
            self.editLrc.setPlainText(text)
            self.lrcFile = url.toLocalFile()

    def saveAction_(self):
        if self.lrcFile:
            with open(self.lrcFile, "w") as f:
                f.write(self.editLrc.toPlainText())
        else:
            self.saveAsAction_()

    def saveAsAction_(self):
        f, r = QFileDialog.getSaveFileName(self, self.tr("Save as"), self.parent.parent.parameter.lrcLocalPath, "lrc files (*.lrc)")
        if f:
            self.lrcFile = f
            self.saveAction_()

    def insertAction_(self):
        m, ts = divmod(self.parent.parent.musicEngine.getPosition(), 60000)
        m = str(m).zfill(2)
        s = str(ts).zfill(5)[:2]
        ms = str(ts).zfill(5)[-3:]
        tag = f"[{m}:{s}.{ms}]"
        self.editLrc.moveCursor(QTextCursor.MoveOperation.StartOfLine)
        self.editLrc.textCursor().insertText(tag)
        self.editLrc.moveCursor(QTextCursor.MoveOperation.StartOfLine)
        self.editLrc.moveCursor(QTextCursor.MoveOperation.Down)

    def removeTagsAction_(self):
        self.editLrc.moveCursor(QTextCursor.MoveOperation.StartOfLine)
        self.editLrc.moveCursor(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
        cursor = self.editLrc.textCursor()
        text = cursor.selectedText()
        newText = re.sub(r'\[\d\d:\d\d.*?\]', "", text)
        self.editLrc.cut()
        self.editLrc.insertPlainText(newText)

    def removeAllTagsAction_(self):
        text = self.editLrc.toPlainText()
        self.editLrc.clear()
        newText = re.sub(r'\[\d\d:\d\d.*?\]', "", text)
        self.editLrc.setPlainText(newText)

    def removeAllBlankLinesAction_(self):
        lines = self.editLrc.toPlainText().split("\n")
        self.editLrc.clear()
        newLines = list(filter(lambda x: x != "", lines))
        text = "\n".join(newLines)
        self.editLrc.setPlainText(text)

    def removeWhiteSpaceAction_(self):
        lines = self.editLrc.toPlainText().split("\n")
        self.editLrc.clear()
        newLines = list(map(lambda x: x.strip(), lines))
        text = "\n".join(newLines)
        self.editLrc.setPlainText(text)




class albumCoverDock(QDockWidget):

    def __init__(self, title, parent = None):
        super().__init__()
        self.setWindowTitle(title)
        self.parent = parent
        self.albumCoverWidget = albumCoverWidget(self)
        self.setWidget(self.albumCoverWidget)
        self.setFloating(False)




class albumCoverWidget(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setBlankCover()

        self.parent.parent.musicEngine.musicEquipment.playbackStateChanged.connect(self.schedule)

    def schedule(self, state):
        if state.value == 0:
            self.setBlankCover()
        elif state.value == 1:
            if self.parent.parent.currentTrack.trackType == "flac":
                self.searchMedia()
            else:
                self.searchOnline()
        else:
            pass

    def setBlankCover(self):
        pix = QPixmap("icon/blankAlbum.png").scaled(270, 270)
        self.setPixmap(pix)

    def searchMedia(self):
        f = self.parent.parent.currentTrack.trackFile
        audio = FLAC(f)
        if audio.pictures:
            p = audio.pictures[0]
            pix = QPixmap()
            pix.loadFromData(p.data)
            pix = pix.scaled(270, 270)
            self.setPixmap(pix)
        else:
            self.searchOnline()

    def searchOnline(self):
        pass



class playlistDock(QDockWidget):

    def __init__(self, title, parent = None):
        super().__init__(title)
        self.parent = parent
        self.playlistWidget = playlistWidget(self)
        self.setWidget(self.playlistWidget)
        self.setFloating(False)


class playlistWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        searchLayout = QHBoxLayout(None)
        self.searchLabel = QLabel(self.tr("Search:"))
        self.searchLine = QLineEdit(self)
        self.searchLine.setClearButtonEnabled(True)

        self.searchLine.textChanged.connect(self.filtItems)

        searchLayout.addWidget(self.searchLabel)
        searchLayout.addWidget(self.searchLine)

        self.playlistTable = QTableView(self)
        self.playlistTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.playlistTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        #self.playlistTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.headers = [self.tr("Title"), self.tr("Artist"), self.tr("Length"), self.tr("Album"), self.tr("Type"), self.tr("Date"), self.tr("Bit rate"), self.tr("Sample rate"), self.tr("File")]

        self.model = QStandardItemModel(0, 8)  # 0 rows, 1 column

        self.model.setHorizontalHeaderLabels(self.headers)
        self.playlistTable.setModel(self.model)


        mainLayout = QVBoxLayout(None)
        mainLayout.addLayout(searchLayout)
        mainLayout.addWidget(self.playlistTable)
        self.setLayout(mainLayout)

    def filtItems(self, t):
        if t == "":
            self.loadItems(self.parent.parent.collectionListTmp)
        else:
            l = self.playlistTable.findItems(t, Qt.MatchFlag.MatchContains)
            rowList = list(set((map(lambda x: x.row(), l))))
            tl = []
            for i in rowList:
                tl.append(self.parent.parent.collectionListTmp[i])
            self.loadItems(tl)

    def loadItems(self, trackList):
        row = 0
        model = QStandardItemModel(len(trackList), 8)
        for i in trackList:
            au = track(i.strip())
            self.model.setItem(row, 0, QStandardItem(au.trackTitle))
            self.model.setItem(row, 1, QStandardItem(au.trackArtist))
            self.model.setItem(row, 2, QStandardItem(self.formatTrackLength(au.trackLength)))
            self.model.setItem(row, 3, QStandardItem(au.trackAlbum))
            self.model.setItem(row, 4, QStandardItem(au.trackType))
            self.model.setItem(row, 5, QStandardItem(au.trackDate))
            self.model.setItem(row, 6, QStandardItem(str(au.trackBitrate)))
            self.model.setItem(row, 7, QStandardItem(str(au.trackFile)))
            self.model.setItem(row, 8, QStandardItem(au.trackFile))
            row += 1
        self.playlistTable.setModel(self.model)

    def getCurrentPlaylist(self):
        l = []
        for i in range(0, self.model.rowCount()):
            l.append(self.model.item(i, 8).text())
        return l










            # self.playlistTable.setItem(row, 0, QTableWidgetItem(au.trackTitle))
            # self.playlistTable.setItem(row, 1, QTableWidgetItem(au.trackArtist))
            # self.playlistTable.setItem(row, 2, QTableWidgetItem(self.formatTrackLength(au.trackLength)))
            # self.playlistTable.setItem(row, 3, QTableWidgetItem(au.trackAlbum))
            # self.playlistTable.setItem(row, 4, QTableWidgetItem(au.trackType))
            # self.playlistTable.setItem(row, 5, QTableWidgetItem(au.trackDate))
            # self.playlistTable.setItem(row, 6, QTableWidgetItem(str(au.trackBitrate)))
            # self.playlistTable.setItem(row, 7, QTableWidgetItem(str(au.trackSamplerate)))
            # self.playlistTable.setItem(row, 8, QTableWidgetItem(au.trackFile))
            # row += 1

    def formatTrackLength(self, t):
        m, s = divmod(t, 60)
        if s < 10:
            return f"{m}:0{s}"
        else:
            return f"{m}:{s}"
#########################################################################################


class collectionDock(QDockWidget):

    def __init__(self, title, parent = None):
        super().__init__(title)
        self.parent = parent
        self.setWindowTitle = title
        self.collectionWidget = collectionWidget(self)
        self.setWidget(self.collectionWidget)
        self.setFloating(False)

class collectionWidget(QWidget):

    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

        di = QDir("/home/frank/Music/", "Media files (*.mp3 *.flac)")
        layout = QVBoxLayout(None)
        self.model = QFileSystemModel()
        self.model.setNameFilters(["*.mp3", "*.flac"])
        self.model.setNameFilterDisables(False)
        self.model.setRootPath(di.path())

        self.collectionView = collectionView(self)

        self.collectionView.setModel(self.model)
        self.collectionView.setRootIndex(self.model.index(di.path()))
        layout.addWidget(self.collectionView)
        self.setLayout(layout)





class collectionView(QListView):

    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        #self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.initContextMenu()

        self.addToPlaylistAction.triggered.connect(self.addToPlaylistAction_)

    def initContextMenu(self):
        self.contextMenu = QMenu(self)
        self.addToPlaylistAction = QAction(self.tr("add to playlist"), self)
        self.contextMenu.addAction(self.addToPlaylistAction)


    def contextMenuEvent(self, ev):
        self.contextMenu.popup(self.mapToGlobal(ev.pos()))

    def addToPlaylistAction_(self):
        root = self.model().rootPath()
        mediaList = []
        for i in self.selectedIndexes():
            mediaList.append(os.path.join(root, i.data()))
        self.parent.parent.parent.addToPlaylist(mediaList)



if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = albumCoverDock("Album cover")
    w.show()

    sys.exit(app.exec())



