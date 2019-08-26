from SearchWindow import SearchWindow
from VideoWindow import VideoWindow
from http.server import HTTPServer, BaseHTTPRequestHandler
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import QThread
from PyQt5 import QtWebEngineWidgets
from io import BytesIO
from urllib.parse import parse_qs
from collections import deque
import sys
import _thread
import time
import json
import tornado.ioloop
import tornado.web

queue = deque([])
currentVideo = ""
connected = set()


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
    v_window = VideoWindow()


class AddVideoHandler(tornado.web.RequestHandler):    
    def post(self):
        global queue
        title = self.get_argument("title", NODATA)
        video_id = self.get_argument('video_id', NODATA)
        queue.appendleft({'title': title, 'video_id': video_id})

        response_queue = []
        for elem in reversed(queue):
            response_queue.append(elem['title'])
        time.sleep(0.3)
        message = json.dumps({"currentVideo": currentVideo, "queue": response_queue}).encode("utf-8")            
        self.write({"currentVideo": currentVideo, "queue": response_queue})

        
def createQueueJSON():
    response_queue = []
    for elem in reversed(queue):
            response_queue.append(elem['title'])
    return json.dumps({"currentVideo": currentVideo, "queue": response_queue}).encode("utf-8")


def setPlayer():
    global currentVideo
    global queue
    while True:
        if not window.v_window.mediaPlayer.is_playing():
            if queue:
                temp_dict = queue.pop()
                currentVideo = temp_dict['title']
                duration = Window.v_window.PlayVideo(videoId = temp_dict['video_id'])
    

def make_app():
    return tornado.web.Application([
        (r"/add", AddVideoHandler),
    ])

if __name__ == '__main__':
    print("server")
    app = make_app()
    app.listen(8000)
    _thread.start_new_thread(tornado.ioloop.IOLoop.current().start, ())
    
    print("Qt")
    window = Window()
    window.v_window.show()
    
    _thread.start_new_thread(setPlayer, ())

    exit_code = window.appctxt.app.exec_()
    sys.exit(0)