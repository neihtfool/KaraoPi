from SearchWindow import SearchWindow
from VideoWindow import VideoWindow
from http.server import HTTPServer, BaseHTTPRequestHandler
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import QThread
from io import BytesIO
from urllib.parse import parse_qs
from collections import deque
from tornado.platform import asyncio
from qr_code_gen import generate_qr_code
import youtube_api as youtube
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
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP_ADDR = s.getsockname()[0]
s.close()
PORT = 8000
URL = "http://" + IP_ADDR + ":" + str(PORT)

queue = deque([])
currentVideo = ""

NODATA = "No data received!"

class Window():
    def __init__(self, url):
        super().__init__()
        generate_qr_code(url)
        self.appctxt = ApplicationContext()
        stylesheet = self.appctxt.get_resource('styles.qss')
        self.appctxt.app.setStyleSheet(open(stylesheet).read())
        self.v_window = VideoWindow()
        self.s_window = SearchWindow()


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


class xAddVideoHandler(tornado.web.RequestHandler):    
    def post(self):
        global queue
        data = json.loads(self.request.body.decode('utf-8'))
        title = data['title']
        video_id = data['video_id']
        queue.appendleft({'title': title, 'video_id': video_id})
        self.write(title + " added.")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('../web/index.html', url=IP_ADDR)


class YTHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        q = data['query']
        max_results = data['maxResults']
        results = youtube.search(q, max_results)
        res = {}
        for r in results:
            res[youtube.get_id(r)] = youtube.get_title(r)
        self.set_status(200)
        self.write(res)
        self.finish()
        
        
def createQueueResponse():
    response_queue = [elem['title'] for elem in reversed(queue)]
    return {"currentVideo": currentVideo, "queue": response_queue}


def setPlayer(v_window):
    global currentVideo
    global queue
    while True:
        if not v_window.mediaPlayer.is_playing():
            if queue:
                temp_dict = queue.pop()
                currentVideo = temp_dict['title']
                v_window.PlayVideo(videoId=temp_dict['video_id'])
                time.sleep(0.3)

def make_app():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/images/(.*)",tornado.web.StaticFileHandler, {"path": "./src/main/web/images/"},),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': ""}),
        (r'/(favicon\.ico)', tornado.web.StaticFileHandler, {"path": "./src/main/icons/"}),
        (r"/add", AddVideoHandler),
        (r"/xAdd", xAddVideoHandler),
        (r"/remove", RemoveVideoHandler),
        (r"/search", YTHandler),
        (r"/queue",QueueWebSocketHandler)
    ])

if __name__ == '__main__':
    print("intialize server")
    app = make_app()
    app.listen(PORT)

    print("intialize Websocket Push Service")
    main_loop = tornado.ioloop.IOLoop.current()
    main_loop.add_timeout(datetime.timedelta(seconds=3), QueueWebSocketHandler.send_message)
    _thread.start_new_thread(main_loop.start, ())
    
    print("Initialize Videoframe")
    window = Window(URL)
    window.v_window.showFullScreen()
    _thread.start_new_thread(setPlayer, (window.v_window, ))

    print("Initialize SearchWindow")
    window.s_window.start_listener()
    window.s_window.showFullScreen()

    exit_code = window.appctxt.app.exec_()
    sys.exit(0)
