#!/usr/bin/env python


import Brain
import asyncio
import websockets

_socket = None

async def start_listing ():
    await Brain.list(_socket)

async def test_socket(websocket, path):
    global _socket
    _socket = websocket
    await start_listing ()

start_server = websockets.serve(test_socket, '', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
