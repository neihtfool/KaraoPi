from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QListWidgetItem, QListView
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QTextDocument, QPixmap, QIcon, QStandardItem, QStandardItemModel
from CustomListItem import CustomListItem
import youtube_api as youtube
import requests


class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
    
        self.tmp = {}

        self.textbox = QLineEdit(self)
        self.textbox.returnPressed.connect(self.search)

        self.listWidget = QListView()
        self.listWidget.setIconSize(QSize(90,90))
        self.model = QStandardItemModel(self.listWidget)
        self.listWidget.clicked.connect(self.clicked_item)

        self.button = QPushButton('Search', self)
        self.button.clicked.connect(self.search)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.textbox)
        self.hbox.addWidget(self.button)
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(5, 5, 5, 5)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.listWidget)
        self.vbox.setSpacing(0)
        self.vbox.setContentsMargins(5, 5, 5, 5)

        self.setLayout(self.vbox)

    def search(self):
        textboxValue = self.textbox.text()
        results = youtube.search(textboxValue)
        self.build_list(results)

    def build_list(self, results):
        self.model.clear()
        for item in results:
            title = youtube.get_title(item)
            thumbnail = youtube.get_thumbnail_medium(item)
            pixmap = QPixmap()
            pixmap.loadFromData(thumbnail)
            image = QIcon(pixmap)

            qItem = QStandardItem()
            qItem.setText(title)
            qItem.setIcon(image)

            self.model.appendRow(qItem)
            self.tmp[title] = youtube.get_id(item)

        self.listWidget.setModel(self.model)

    def clicked_item(self, item):
        title = self.model.itemFromIndex(item).text()
        requests.post('http://localhost:8000', data=self.tmp[title])
