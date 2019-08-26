import websockets
import asyncio
import sys

async def t():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as ws:
        await ws.send("test")
        while True:
            g = await ws.recv()
            print(g)


asyncio.get_event_loop().run_until_complete(t())
sys.exit(0)
