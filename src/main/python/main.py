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
import asyncio
import websockets

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
        global queue

        req = self.rfile.read(content_length).decode("utf-8")
        content = json.loads(req)

        queue.appendleft({'title': content['title'], 'video_id': content['video_id']})
    
        self.send_response(200)
        self.end_headers()
        
        response_queue = []
        for elem in reversed(queue):
            response_queue.append(elem['title'])

        message = json.dumps({"currentVideo": currentVideo, "queue": response_queue}).encode("utf-8")            
        self.wfile.write(message)

        
async def createQueueJSON():
    response_queue = []
    for elem in reversed(queue):
            response_queue.append(elem['title'])
    return await json.dumps({"currentVideo": currentVideo, "queue": response_queue}).encode("utf-8")


async def setPlayer():
    while True:
        if not window.v_window.mediaPlayer.is_playing():
            if queue:
                temp_dict = queue.pop()
                currentVideo = temp_dict['title']
                print("current", currentVideo)
                duration = Window.v_window.PlayVideo(videoId = temp_dict['video_id'])
                #time.sleep(duration - 0.5) #minimize delay
        
    
async def sendQueue(websocket, path):
    global currentVideo
    global queue
    tmp_q = queue.copy()
    tmp_current = currentVideo
    while True:
        print(currentVideo)
        print(tmp_current)
        if not (tmp_q == queue and tmp_current == currentVideo):
            print("koko")
            message = await createQueueJSON()
            await websocket.send(message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    httpd = Server()
    httpd.start()
    print("http")
    window = Window()
    _thread.start_new_thread(window.v_window.show, ())
    print("Qt")
    web_socket_server = websockets.serve(sendQueue, 'localhost', 8765)
    asyncio.ensure_future(setPlayer())
    asyncio.ensure_future(web_socket_server)
    loop.run_forever()
    #_thread.start_new_thread(loop.run_forever(), ())
    #_thread.start_new_thread(asyncio.get_event_loop().run_forever, ())


    exit_code = window.appctxt.app.exec_()
    sys.exit(0)