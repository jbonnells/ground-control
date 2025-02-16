# https://stackoverflow.com/a/72702853

import asyncio
import random
import websockets
import json


async def recv(websocket, path):
    try:
        name = await asyncio.wait_for(websocket.recv(), timeout=0.1)
        print("name", name)
    except asyncio.TimeoutError:
        print("No Data")
    await asyncio.sleep(0.1)

async def send(websocket, path):
    data = [
            {
              "name": "altitude",
              "number": round(random.uniform(100, 10000), 2)
            },
            {
              "name": "speed",
              "number": round(random.uniform(0, 900), 2)
            },
            {
              "name": "heading",
              "number": round(random.uniform(0, 360), 2)
            }
    ]
    await websocket.send(json.dumps(data))
    await asyncio.sleep(0.1)


async def main2(websocket):
    path=''
    while True:
        send_task = asyncio.create_task(send(websocket, path))
        await send_task
        recv_task = asyncio.create_task(recv(websocket, path))
        await recv_task

#rewrite of this part is to remove Deprecation Warning
async def main():
    server = await websockets.serve(main2, 'localhost', 4000, ping_interval=None)
    await server.wait_closed()

asyncio.run(main())