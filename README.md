#Signaling-server

A simple WebSocket based server that allows to relay messages between connected clients.

It can be used to relay the webRTC messages necessary to the establishment of a peer-to-peer webRTC connection.

## Protocol

The server and the clients exchange JSON-formatted message, that have one mandatory `"type"` field.

When a client connects, the server assigns it an id (16 characters hex string) and sends it to the client in a `"hello"` message. In the current implementation, the server also sends the list of all connected clients in the hello message. We can imagine that in a real application, it would send a list of potential webRTC peers.

Clients can then send `"data"` message. The `"data"` payload is transmitted as-is to the destination `"dest"`. If the destination has disconnected, an `"error"` message is sent back to the client that generated the data message.

## How to use

### Setup

Requires Python 3.5

```
pip3 install -r requirements.txt
```

### Running the server

```
python3 signaling-server.py
```

### Running the test clients

Launch severl times:

```
python3 test_client.py
```

