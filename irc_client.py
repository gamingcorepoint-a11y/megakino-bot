import socket
import asyncio
from config import SERVER, PORT, TOKEN, NICK, CHANNEL


class IRCClient:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)

    async def connect(self):
        await asyncio.get_event_loop().sock_connect(self.sock, (SERVER, PORT))

        self.sock.send(f"PASS {TOKEN}\r\n".encode())
        self.sock.send(f"NICK {NICK}\r\n".encode())
        self.sock.send(f"JOIN #{CHANNEL}\r\n".encode())

    async def send(self, message):
        self.sock.send(f"PRIVMSG #{CHANNEL} :{message}\r\n".encode())

    async def listen(self, callback):
        loop = asyncio.get_event_loop()

        while True:
            data = await loop.sock_recv(self.sock, 2048)
            lines = data.decode().split("\r\n")

            for line in lines:
                if line.startswith("PING"):
                    self.sock.send("PONG :tmi.twitch.tv\r\n".encode())
                elif line:
                    await callback(line)
