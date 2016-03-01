#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import json
import random
import asyncio
import websockets

clients = {}

def new_id():
    testId = ''.join(random.choice('0123456789abcdef') for i in range(16))
    while testId in clients:
        testId = ''.join(random.choice('0123456789abcdef') for i in range(16))
    return testId

def hello_message(clientId):
    d = {
        "type" : "hello",
        "id" : clientId,
        "peers" : [i for i in clients],     # For testing purposes only
    }
    return json.dumps(d)

def data_message(sourceId, data):
    d = {
        "type": "data",
        "src" : sourceId,
        "data" : data,
    }
    return json.dumps(d)

def error_message(description, info):
    d = {
        "type" : "error",
        "desc" : description,
        "info" : info,
    }
    return json.dumps(d)

async def handler(websocket, path):
    global clients

    clientId = new_id()
    print("New client, ID: {}".format(clientId))
    clients[clientId] = websocket
    await websocket.send(hello_message(clientId))

    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            if "type" in data:
                if data["type"] == "data" and "dest" in data and "data" in data:
                    if data["dest"] in clients:
                        try:
                            await clients[data["dest"]].send(data_message(clientId, data["data"]))
                        except websockets.exceptions.ConnectionClosed:
                            if data["dest"] in clients:
                                del clients[data["dest"]]
                            await websocket.send(error_message("client_unavailable", data["dest"]))
                    else:
                        await websocket.send(error_message("client_unavailable", data["dest"]))
        except websockets.exceptions.ConnectionClosed:
            if clientId in clients:
                del clients[clientId]
            break

def run_server():
    start_server = websockets.serve(handler, '0.0.0.0', 6000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    run_server()
