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


queue = deque([])
currentVideo = ""


class Server(QThread):
    def run(self):
        self._server = HTTPServer(('localhost', 8000), RequestHandler)
        self._server.serve_forever()


class Window():
    appctxt = ApplicationContext()
    v_window = VideoWindow()


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        temp_dict = {}
        global queue
        for key, value in dict(parse_qs(self.rfile.read(content_length))).items():
            temp_dict[key.decode("utf-8")] = value[0].decode("utf-8")
        
        queue.appendleft(temp_dict)
        self.send_response(200)
        self.end_headers()
        response_queue = []
        for d in reversed(queue):
            response_queue.append(d['title'])

        self.wfile.write(json.dumps({"currentVideo": currentVideo, "queue": response_queue}).encode("utf-8"))

        
def run():
    while True:
        if not window.v_window.mediaPlayer.is_playing() and queue:
            global currentVideo
            temp_dict = queue.pop()
            currentVideo = temp_dict['title']
            duration = Window.v_window.PlayVideo(videoId=temp_dict['video_id'])
            print(currentVideo)
            time.sleep(duration - 0.5) #minimize delay

if __name__ == '__main__':
    httpd = Server()
    httpd.start()
    window = Window()
    window.v_window.show()
    _thread.start_new_thread(run, ())
    exit_code = window.appctxt.app.exec_()
    sys.exit(0)