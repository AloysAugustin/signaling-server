#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import json
import time
import random
import asyncio
import websockets

def data_message(dest, data):
    d = {
        "type" : "data",
        "dest" : dest,
        "data" : data,
    }
    return json.dumps(d)

async def client_handler():
    async with websockets.connect('ws://localhost:6000/') as websocket:
        hellomsg = await websocket.recv()
        hellodata = json.loads(hellomsg)
        print("Received hello. My ID is {}".format(hellodata["id"]))
        print("{} peers available.".format(len(hellodata["peers"])))
        # Send 10 messages at 10s interval and then exit. Print messages received in the mean time
        for i in range(10):
            end = time.time() + 5.0
            while True:
                try:
                    msg = await asyncio.wait_for(asyncio.ensure_future(websocket.recv()), timeout=end - time.time())
                    msgdata = json.loads(msg)
                    if "type" in msgdata:
                        if msgdata["type"] == "data":
                            print("Received {} from {}.".format(msgdata["data"], msgdata["src"]))
                        elif msgdata["type"] == "error":
                            print("Error: client {} is not available anymore".format(msgdata["info"]))
                except asyncio.TimeoutError:
                    break
            if len(hellodata["peers"]) > 0:
                dest = random.choice(hellodata["peers"])
                print("Sending to {}".format(dest))
                await websocket.send(data_message(dest, "blah"))

if __name__ == '__main__':
    asyncio.get_event_loop().set_debug(True)
    asyncio.get_event_loop().run_until_complete(client_handler())
