from SearchWindow import SearchWindow
from VideoWindow import VideoWindow
from http.server import HTTPServer, BaseHTTPRequestHandler
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import QUrl, QThread
from PyQt5 import QtWebEngineWidgets
from io import BytesIO
import sys


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
        print("GET")
    
    def do_POST(self):
        print("POST")
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode("utf-8")
        self.send_response(200)
        self.end_headers()
        Window.v_window.PlayVideo(videoId=body)


if __name__ == '__main__':
    httpd = Server()
    httpd.start()
    window = Window()
    window.v_window.show()
    exit_code = window.appctxt.app.exec_()
    sys.exit(0)