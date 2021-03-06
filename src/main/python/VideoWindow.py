from SearchWindow import SearchWindow
from PyQt5.QtCore import Qt, QTimer, QEventLoop, QPoint
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QAction, QFrame, QSlider, QMainWindow, QStyle, QApplication, QLabel
from PyQt5.QtGui import QIcon, QColor, QPalette, QPixmap
from PIL.ImageQt import Image, ImageQt
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
        self.search_window = SearchWindow()
    
    def setUpGUI(self):
        self.resize(800, 480)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        if sys.platform == "darwin":
            from PyQt5.QtWidgets import QMacCocoaViewContainer
            self.videoframe = QMacCocoaViewContainer(0)
        else:
            self.videoframe = QFrame()

        self.videoframe.mouseDoubleClickEvent = self.openDialog
        self.videoframe.mouseReleaseEvent = self.PlayPause
        self.palette = self.videoframe.palette()
        self.palette.setColor(QPalette.Window, QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)
        self.videoframe

        self.positionSlider = QSlider(Qt.Horizontal, self)
        self.positionSlider.setMaximum(1000)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.addWidget(self.positionSlider)
        self.hboxLayout.setSpacing(0)
        self.hboxLayout.setContentsMargins(0, 0, 0, 0)

        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.addWidget(self.videoframe)
        self.vboxLayout.addLayout(self.hboxLayout)
        self.vboxLayout.setSpacing(0)
        self.vboxLayout.setContentsMargins(0, 0, 0, 0)

        self.widget.setLayout(self.vboxLayout)

        _open = QAction("&Open", self)
        _open.triggered.connect(sys.exit)     

        try:
            _thread.start_new_thread(self.updateUI, ())
        except:
            print("error with positionSliderThread")

    def openDialog(self, event):
        self.search_window.hide() if self.search_window.isVisible() else self.search_window.show()
        self.search_window.start_listener()

    def updateUI(self):
        while True:
            if self.mediaPlayer.is_playing():
                self.positionSlider.setValue(self.mediaPlayer.get_position() * 1000)

    def setPosition(self, position):
        self.mediaPlayer.set_position(position / 1000.0)

    def PlayPause(self, event):
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def Stop(self):
        self.mediaPlayer.stop()
    
    def PlayVideo(self, videoId):
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
        
    def setVolume(self, Volume):
        self.mediaPlayer.audio_set_volume(Volume)
    
    def setup_qr_icon(self):
        pixmap = QPixmap('./src/main/resources/qr.jpg')
        self.icon.setPixmap(pixmap)
        p = self.geometry().bottomRight() - self.icon.geometry().bottomRight() - QPoint(100, 100)
        self.icon.move(p)