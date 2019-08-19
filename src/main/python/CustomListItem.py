from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap


class CustomListItem(QWidget):
    def __init__(self, parent=None):
        super(CustomListItem, self).__init__(parent)
        self.textVBox = QVBoxLayout()
        self.titleQLabel = QLabel()
        self.textVBox.addWidget(self.titleQLabel)

        self.allHBox = QHBoxLayout()
        self.thumbnail = QLabel()
        self.allHBox.addWidget(self.thumbnail, 0)
        self.allHBox.addLayout(self.textVBox, 1)
        self.setLayout(self.allHBox)

    def setTitle(self, text):
        self.titleQLabel.setText(text)

    def setIcon(self, image_data):
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        image = pixmap.scaledToWidth(90)
        self.thumbnail.setPixmap(image)