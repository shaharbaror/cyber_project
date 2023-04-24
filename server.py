import socket
from socket import create_server
from select import select
from random import randint

from Protocol import Protocol
from mememaker import MemeMaker


class Server:
    def __init__(self, address, port):
        self.port = port
        self.address = address
        self.s = create_server((address, port))
        self.s.listen(9)
        self.clients = {}
        self.running = True

    def handle_request(self, request):
        (header, body) = Protocol.proces_request(request)
        if body.startswith(b"stuff"):
            rnd = str(randint(1, 7)).encode()
            image = MemeMaker.getImage(rnd)
            style = MemeMaker.getStyles(rnd)




    def accept(self):
        readable, _, _ = select([self.s], [], [])
        if self.s in readable:
            connection, address = self.s.accept()
            self.clients.update({connection: address})

    def respond(self):
        readable, _, _ = select(self.clients.keys(), [], [])
        for client in readable:
            data = Protocol.receive(client)
            if data:
                client.send(self.handle_request(data))
            else:
                self.clients.pop(client)

    def run(self):
        while self.running:
            self.accept()
            self.respond()

