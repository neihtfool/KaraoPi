from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect

class WebSocketClient(object):
    def __init__(self, url):
        self.url = url
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.connect()
        PeriodicCallback(self.keep_alive, 20000).start()
        self.ioloop.start()

    async def connect(self):
        print("trying to connect")
        self.ws = await websocket_connect(self.url)
        if not self.ws:
            print("connection failed ")
        else:
            print("connected")
            self.run()   

    async def run(self):
        while True:
            msg = await self.ws.read_message()
            if msg is None:
                print("Connection closed")
                self.ws = None
                break
            else:
                print(msg)

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message("keep_alive")

    