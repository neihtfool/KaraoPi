from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
import youtube_api as youtube
import requests


class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
    
        self.tmp = {}

        self.textbox = QLineEdit(self)

        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(self.clicked_item)

        self.button = QPushButton('Search', self)
        self.button.clicked.connect(self.on_click)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.textbox)
        self.hbox.addWidget(self.button)
        self.hbox.addWidget(self.listWidget)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

    def on_click(self):
        textboxValue = self.textbox.text()
        results = youtube.search(textboxValue)
        self.build_list(results)

    def build_list(self, results):
        self.listWidget.clear()
        for item in results:
            title = youtube.get_title(item)
            self.listWidget.addItem(title)
            self.tmp[title] = youtube.get_id(item)

    def clicked_item(self, item):
        title = str(item.text())
        _id = self.tmp[title]
        r = requests.post('http://localhost:8000', data =_id)
