from SearchWindow import SearchWindow
from VideoWindow import VideoWindow
from http.server import HTTPServer, BaseHTTPRequestHandler
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import QThread
from PyQt5 import QtWebEngineWidgets
from io import BytesIO
from urllib.parse import parse_qs
from collections import deque
from tornado.platform import asyncio
import sys
import os
import _thread
import time
import json
import tornado.ioloop
import tornado.web
import tornado.websocket
import threading
import datetime

root = os.path.dirname(__file__)

queue = deque([])
currentVideo = ""

NODATA = "No data received!"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Window():
    appctxt = ApplicationContext()
    stylesheet = appctxt.get_resource('styles.qss')
    appctxt.app.setStyleSheet(open(stylesheet).read())
    v_window = VideoWindow()


class QueueWebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        self.connections.add(self)
        self.write_message(createQueueResponse())
    
    def on_message(self, message):
        print("client wrote:", message)

    def on_close(self):
        self.connections.remove(self)

    @classmethod 
    def send_message(cls):
        removable = set()
        for ws in cls.connections:
            if not ws.ws_connection or not ws.ws_connection.stream.socket:
                removable.add(ws)
            else:
                ws.write_message(createQueueResponse())
        
        for ws in removable:
            cls.connections.remove(ws)
        
        tornado.ioloop.IOLoop.current().add_timeout(datetime.timedelta(seconds=3), QueueWebSocketHandler.send_message)


class RemoveVideoHandler(tornado.web.RequestHandler):
    def post(self):
        global queue
        index = self.get_argument("index", NODATA)
        del queue[len(queue) - 1 - int(index)]
        self.write(createQueueResponse())


class AddVideoHandler(tornado.web.RequestHandler):    
    def post(self):
        global queue
        title = self.get_argument("title", NODATA)
        video_id = self.get_argument('video_id', NODATA)
        queue.appendleft({'title': title, 'video_id': video_id})
        self.write(createQueueResponse())

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('../web/index.html')

        
def createQueueResponse():
    response_queue = [elem['title'] for elem in reversed(queue)]
    return {"currentVideo": currentVideo, "queue": response_queue}


def setPlayer():
    global currentVideo
    global queue
    while True:
        if not (window.v_window.mediaPlayer.is_playing() or Window.v_window.paused):
            if queue:
                temp_dict = queue.pop()
                currentVideo = temp_dict['title']
                Window.v_window.PlayVideo(videoId=temp_dict['video_id'])
                time.sleep(0.3)

def make_app():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/images/(.*)",tornado.web.StaticFileHandler, {"path": "./src/main/web/images/"},),
        (r"/add", AddVideoHandler),
        (r"/remove", RemoveVideoHandler),
        (r"/queue",QueueWebSocketHandler)
    ])

if __name__ == '__main__':
    print("intialize server")
    app = make_app()
    app.listen(8000)

    print("intialize Websocket Push Service")
    main_loop = tornado.ioloop.IOLoop.current()
    main_loop.add_timeout(datetime.timedelta(seconds=5), QueueWebSocketHandler.send_message)
    _thread.start_new_thread(main_loop.start, ())
    
    print("Initialize Videoframe")
    window = Window()
    window.v_window.search_window.start_listener()
    window.v_window.show()
    _thread.start_new_thread(setPlayer, ())

    exit_code = window.appctxt.app.exec_()
    sys.exit(0)