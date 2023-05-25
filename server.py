import socket
import os
from socket import create_server
from select import select
from random import randint


from Protocol import Protocol
from mememaker import MemeMaker

#['GET', '127.0.0.1/FirstPage?s=t&i=2&c=%20Caption%201%20hello%20my%20frient,Caption%202', 'HTTP/1.1']
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

        if "GetTime" in header[1]:
            with open("response.json", "wb") as r:
                r.write(b'"time":20')
            with open("response.json", "rb").read() as r:
                msg = Protocol.create_msg(r, "text/json")
                return msg

        if "FirstPage" in header[1]:
            status = header[1].split("?")[1:]
            status = "?".join(status).split("&")

            if status[0] == "s=t":
                #need to save the player submit data
                memeId = status[1].split("=")[-1]
                print(memeId)
                captions = status[2:]
                captions = "&".join(captions)
                # captions = captions.replace("&amp;", "&")
                # captions = captions.replace("%20", " ")
                return Protocol.create_msg(captions.encode(),"text/txt")

            else:
                action = status[1][2:]
                if action == "startgame":
                    # with open("response.json", "wb") as r:
                    #     r.write(b'"time" : 20')
                    rnd = randint(1,2)
                    style = MemeMaker.getStyles(rnd)
                    Protocol.update_json(rnd, 120)

                    with open("response.json", "rb") as r:
                        msg = Protocol.create_msg(r.read(), "text/json")
                        return msg
                if action == "newmeme":
                    rnd = randint(1, 2)
                    style = MemeMaker.getStyles(rnd)

                    Protocol.update_json(rnd, 50)

                    with open("response.json", "rb") as r:
                        f = r.read()
                        #MAKE IT WORK, IM TOO LAZY RN 
                        f = f.split(b",")

                        f = b",".join(f[:-1]) + b"\n}"
                        print(f)
                        msg = Protocol.create_msg(f, "text/json")

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