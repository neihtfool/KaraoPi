from PyQt5.QtCore import Qt, QTimer, QEventLoop
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QAction, QFrame, QSlider, QMainWindow, QStyle
from PyQt5.QtGui import QIcon, QColor, QPalette
import _thread
import time
import sys
import vlc
import pafy

URL = "https://www.youtube.com/watch?v="


class VideoWindow(QMainWindow):
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

        if sys.platform == "darwin":
            from PyQt5.QtWidgets import QMacCocoaViewContainer	
            self.videoframe = QMacCocoaViewContainer(0)
        else:
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

        self.stopbutton = QPushButton()
        self.stopbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.hbuttonbox.addWidget(self.stopbutton)
        self.stopbutton.clicked.connect(self.Stop)

        self.hbuttonbox.addStretch(1)

        self.positionSlider = QSlider(Qt.Horizontal, self)
        self.positionSlider.setMaximum(1000)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.addWidget(self.videoframe)
        self.vboxLayout.addWidget(self.positionSlider)
        self.vboxLayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxLayout)

        _open = QAction("&Open", self)
        _open.triggered.connect(sys.exit)     

        try:
            _thread.start_new_thread(self.updateUI, ())
        except:
            print("error with positionSliderThread")

    def updateUI(self):
        while True:
            if self.mediaPlayer.is_playing():
                self.positionSlider.setValue(self.mediaPlayer.get_position() * 1000)

    def setPosition(self, position):
        self.mediaPlayer.set_position(position / 1000.0)

    def PlayPause(self):
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.isPaused = True
        else:
            if self.mediaPlayer.play() == -1:
                self.OpenFile()
                return
            self.mediaPlayer.play()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            #self.timer.start()
            self.isPaused = False

    def Stop(self):
        self.mediaPlayer.stop()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    
    def OpenFile(self, videoId):
        yt_url = URL + videoId
        video = pafy.new(yt_url)
        best = video.getbest()
        playurl = best.url
        self.media = self.instance.media_new(playurl)
        self.media.get_mrl()
        self.mediaPlayer.set_media(self.media)

        if sys.platform.startswith('linux'):
            self.mediaPlayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32":
            self.mediaPlayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin":
            self.mediaPlayer.set_nsobject(int(self.videoframe.winId()))

        self.mediaPlayer.play()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        #self.timer.start()
        self.isPaused = False

    def setVolume(self, Volume):
        self.mediaPlayer.audio_set_volume(Volume)
    