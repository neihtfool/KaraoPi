from browser_window import BrowserWindow

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import Qt, QDir, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QStyle, QHBoxLayout, QFileDialog, QAction, QMainWindow
from PyQt5.QtGui import QIcon
import requests
import sys
import requests


class MainWindow(QMainWindow):

    secondWindowIsOpen = False

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        text = QLabel()
        text.setWordWrap(True)

        videoWidget = QVideoWidget()
        videoWidget.mouseReleaseEvent = self.openDialog

        self.widget = BrowserWindow()
        
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)

        wid = QWidget(self)
        self.setCentralWidget(wid)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)

        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)

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


if __name__ == '__main__':
    appctxt = ApplicationContext()
    stylesheet = appctxt.get_resource('styles.qss')
    appctxt.app.setStyleSheet(open(stylesheet).read())
    window = MainWindow()
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)