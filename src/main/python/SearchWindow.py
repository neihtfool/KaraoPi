from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QListWidgetItem, QListView, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QTextDocument, QPixmap, QIcon, QStandardItem, QStandardItemModel
from CustomListItem import CustomListItem
from tornado.httpclient import HTTPClient, HTTPRequest
import youtube_api as youtube
import json
import urllib


class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
    
        self.tmp = {}

        self.textbox = QLineEdit(self)
        self.textbox.returnPressed.connect(self.search)

        self.searchResultLabel = QLabel()
        self.searchResultLabel.setText("Search Results")
        self.searchResultLabel.setStyleSheet('color: white')

        self.currentVideoLabel = QLabel("Currently Playing: ")
        self.currentVideoLabel.setStyleSheet('color: white')
        self.currentVideo = QLabel()
        self.currentVideo.setStyleSheet('color: white')
        self.currentVideoHBox = QHBoxLayout()
        self.currentVideoHBox.addWidget(self.currentVideoLabel)
        self.currentVideoHBox.addWidget(self.currentVideo)

        self.queueLabel = QLabel("Coming up next:")
        self.queueLabel.setStyleSheet('color: white')

        self.searchResultsList = QListView()
        self.searchResultsList.setIconSize(QSize(90,90))
        self.model = QStandardItemModel(self.searchResultsList)
        self.searchResultsList.clicked.connect(self.clicked_item)

        self.queueList = QListView()
        self.queueList.setIconSize(QSize(90,90))
        self.queueModel = QStandardItemModel(self.queueList)

        self.button = QPushButton('Search', self)
        self.button.clicked.connect(self.search)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.textbox)
        self.hbox.addWidget(self.button)
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(5, 5, 5, 5)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.searchResultLabel)
        self.vbox.addWidget(self.searchResultsList)
        self.vbox.addLayout(self.currentVideoHBox)
        self.vbox.addWidget(self.queueLabel)
        self.vbox.addWidget(self.queueList)
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

        self.searchResultsList.setModel(self.model)

    def clicked_item(self, item):
        title = self.model.itemFromIndex(item).text()
        data = {'title': title, 'video_id': self.tmp[title]}
        body = urllib.parse.urlencode(data)
        http_client = HTTPClient()
        try:
            res = http_client.fetch('http://localhost:8000/add', method='POST', headers=None, body=body)
            content = json.loads(res.body.decode("utf-8"))
            self.currentVideo.setText(content['currentVideo'])
            self.setupQueue(content['queue'])
        except Exception as e:
            print(str(e))
        

    def setupQueue(self, queue):
        self.queueModel.clear()
        for q in queue:
            qItem = QStandardItem(q)
            self.queueModel.appendRow(qItem)
        self.queueList.setModel(self.queueModel)




