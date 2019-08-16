from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QAction, QFrame, QSlider, QMainWindow, QStyle
from PyQt5.QtGui import QIcon, QColor, QPalette
import time
import sys
import vlc
import pafy

class VideoWindow(QMainWindow):
    secondWindowIsOpen = False

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        
        self.instance = vlc.Instance()
        self.mediaPlayer = self.instance.media_list_player_new()

        self.instance = vlc.Instance()
        self.mediaPlayer = self.instance.media_player_new()

        self.setUpGUI()
        self.isPaused = False
    
    def setUpGUI(self):
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.videoframe = QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor(QPalette.Window, QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.hbuttonbox = QHBoxLayout()
        self.playButton = QPushButton()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.hbuttonbox.addWidget(self.playButton)
        self.playButton.clicked.connect(self.PlayPause)

        self.openButton = QPushButton("Open")
        self.hbuttonbox.addWidget(self.openButton)
        self.openButton.clicked.connect(self.OpenFile)

        self.stopbutton = QPushButton("Stop")
        self.stopbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.hbuttonbox.addWidget(self.stopbutton)
        self.stopbutton.clicked.connect(self.Stop)

        self.hbuttonbox.addStretch(1)
        self.volumeSlider = QSlider(Qt.Horizontal, self)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setValue(self.mediaPlayer.audio_get_volume())
        self.volumeSlider.setToolTip("Volume")
        self.hbuttonbox.addWidget(self.volumeSlider)

        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.addWidget(self.videoframe)
        self.vboxLayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxLayout)

        _open = QAction("&Open", self)
        _open.triggered.connect(sys.exit)     

        self.timer = QTimer(self)
        self.timer.setInterval(200)

    def PlayPause(self):
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.isPaused = True
        else:
            if self.mediaPlayer.play() == -1:
                self.OpenFile()
                return
            self.mediaPlayer.play()
            self.playButton.setText("Pause")
            self.timer.start()
            self.isPaused = False

    def Stop(self):
        self.mediaPlayer.stop()
        self.playButton.setText("Play")
    
    def OpenFile(self, filename=None):
        testVideo = "https://www.youtube.com/watch?v=s9nxlfS-RCs"
        video = pafy.new(testVideo)
        best = video.getbest()
        playurl = best.url
        self.media = self.instance.media_new(playurl)
        self.media.get_mrl()
        self.mediaPlayer.set_media(self.media)

        self.mediaPlayer.set_xwindow(self.videoframe.winId())
        self.mediaPlayer.play()

    def setVolume(self, Volume):
        self.mediaPlayer.audio_set_volume(Volume)
    