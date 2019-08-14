from browser_window import BrowserWindow
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import Qt, QDir, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QStyle, QHBoxLayout, QFileDialog, QAction, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5 import QtWebEngineWidgets, QtWebEngineCore
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from threading import Thread
import time
import requests
import sys
import requests

URL = "https://www.youtube.com/embed/"

class MainWindow(QMainWindow):

    secondWindowIsOpen = False

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.active = False
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        text = QLabel()
        text.setWordWrap(True)

        videoWidget = QVideoWidget()
        videoWidget.mouseReleaseEvent = self.openDialog

        # self.webView = QtWebEngineWidgets.QWebEngineView()
        # self.webView.mouseReleaseEvent = self.openDialog
        #self.webView.setUrl(QUrl(URL))

        self.widget = BrowserWindow()
        
        self.playButton = QPushButton("Search")
        self.playButton.setEnabled(True)
        self.playButton.clicked.connect(self.openDialog)

        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        wid = QWidget(self)
        self.setCentralWidget(wid)

        self.layout = QVBoxLayout()
        #layout.addWidget(self.webView)
        self.layout.addWidget(self.playButton)
        wid.setLayout(self.layout)
        #self.mediaPlayer.setVideoOutput(videoWidget)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
        
    def openDialog(self, event):
        if self.secondWindowIsOpen:
            self.widget.hide()
        else:
            self.widget.resize(250, 150)
            self.widget.show()
        self.secondWindowIsOpen = not self.secondWindowIsOpen

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video", QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.play()


def setWebView(window):
    while True:
        if window.widget.active:
            video_id = window.widget.queue[0]
            webView = QtWebEngineWidgets.QWebEngineView()
            webView.setUrl(QUrl(URL + video_id))
            window.layout.addWidget(webView)
            print(video_id)
            window.widget.active = False
            window.active = True
            time.sleep(2)
        


if __name__ == '__main__':
    appctxt = ApplicationContext()
    stylesheet = appctxt.get_resource('styles.qss')
    appctxt.app.setStyleSheet(open(stylesheet).read())
    window = MainWindow()
    window.show()
    #manager = Thread(target=setWebView, args=(window,))
    #manager.start()
    exit_code = appctxt.app.exec_()
    setWebView(window)
    sys.exit(exit_code)
    