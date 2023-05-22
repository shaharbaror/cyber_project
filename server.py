import socket
import os
from socket import create_server
from select import select
from random import randint


from Protocol import Protocol
from mememaker import MemeMaker


class Server:

    def __init__(self, address, port):
        self.port = port
        self.address = address
        self.s = create_server(("127.0.0.1", 8000))
        self.s.listen(9)
        self.clients = {}
        self.running = True

    def handle_request(self, requests):
        header, body = Protocol.proces_request(requests)
        http_header = ""
        header[1] = header[1][1:]
        print(header)
        if os.path.isfile(header[1]) or header[1] == "":
            if header[1] == "":
                header[1] = "index.html"
            with open(header[1], "rb") as f:
                f = f.read()

                file_type = Protocol.get_file_type(header[1])
                msg = Protocol.create_msg(f, file_type)
                return msg
        if "get_meme" in header[1]:
            rnd = randint(1, 2)

            style = MemeMaker.getStyles(rnd)
            msg = Protocol.create_msg(style, "text/css")
            return msg
        return b" "

    def accept(self):
        readable, _, _ = select([self.s], [], [])
        if self.s in readable:
            connection, address = self.s.accept()
            self.clients.update({connection: address})

    def respond(self):
        readable, _, _ = select(self.clients.keys(), [], [])
        for client in readable:
            data = Protocol.receive(client).decode()
            print("recieved!")
            if data:
                client.send(self.handle_request(data))
                self.clients.pop(client)
            else:
                self.clients.pop(client)

    def run(self):
        while self.running:
            self.accept()
            self.respond()


def main():
    server = Server("127.0.0.1",8000)
    server.run()


if __name__ == "__main__":
    main()