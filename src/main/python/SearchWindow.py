from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QListWidgetItem, QListView, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QTextDocument, QPixmap, QIcon, QStandardItem, QStandardItemModel
from CustomListItem import CustomListItem
from tornado.httpclient import HTTPClient, HTTPRequest
from functools import partial
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

        self.queueList = QListWidget()
        self.queueList.setIconSize(QSize(90,90))

        self.button = QPushButton('Search', self)
        self.button.clicked.connect(self.search)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.textbox)
        self.hbox.addWidget(self.button)
        self.hbox.setSpacing(10)
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
        self.send_request(body, 'add')

    def setupQueue(self, queue):
        self.queueList.clear()
        for i in range(0, len(queue)):
            list_item = CustomListItem()
            list_item.setTitle(queue[i])
            list_item.remove_button.clicked.connect(partial( self.remove, index=i))

            q_list_widget_item = QListWidgetItem(self.queueList)
            q_list_widget_item.setSizeHint(list_item.sizeHint())
            self.queueList.addItem(q_list_widget_item)
            self.queueList.setItemWidget(q_list_widget_item, list_item)

    def remove(self, index):
        body = urllib.parse.urlencode({'index': index })
        self.send_request(body, 'remove')

    def send_request(self, body, endpoint):
        http_client = HTTPClient()
        try:
            res = http_client.fetch('http://localhost:8000/' + endpoint, method='POST', headers=None, body=body)
            content = json.loads(res.body.decode("utf-8"))
            self.setupQueue(content['queue'])
            self.currentVideo.setText(content['currentVideo'])
        except Exception as e:
            print(str(e))