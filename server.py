import json
import socket
import os
from socket import create_server
from select import select
from random import randint
import time


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
                print("hi")

                bodies = json.loads(body)
                print(bodies)
                with open("lobby1.json", "r") as f:
                    data = json.load(f)
                    print(data["players"])

                    for i in range(len(data["players"])):
                        print(data["players"][i])
                        if bodies["username"] == data["players"][i]:
                            data["players_finished"][i] = True
                            meme_submition = {"index": bodies["memeIndex"], "text": bodies["captions"], "creator": i}
                            print(meme_submition["text"])


            else:
                action = status[1][2:]
                if action == "startgame":
                    # with open("response.json", "wb") as r:
                    #     r.write(b'"time" : 20')
                    rnd = randint(1,2)
                    with open("lobby1.json", "r") as f:
                        data = json.load(f)
                        data["round_timer"] = int(time.time() + 120)
                    with open("lobby1.json","w") as f:
                        json.dump(data, f)
                    print(time.time())
                    timer = 120

                    msg = Protocol.update_json(rnd, timer)
                    msg = Protocol.create_msg(msg, "text/json")

                    return msg

                if action == "newmeme":
                    rnd = randint(1, 2)
                    with open("lobby1.json", "r") as f:
                        data = json.load(f)
                        json_file = Protocol.update_json(rnd, data["round_timer"] - time.time())
                        print(json_file)
                        return Protocol.create_msg(json_file, "text/json")


        return Protocol.create_msg(b" ", "text/txt")

    def handle_post(self, data):
        header, body = Protocol.proces_request(data)
        print(body)
        header[1] = header[1][1:]
        if "firstpage" in header[1]:
            status = header[1].split("?")[1:]
            status = "?".join(status).split("&")
            if status[0] == "s=t":
                with open("lobby1.json", "r") as f:
                    lobby_data = json.load(f)
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