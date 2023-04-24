

class Protocol:

    @staticmethod
    def receive(socket):
        return socket.recv(1024)

    # receives the http request and returns the type of request
    @staticmethod
    def proces_request(request):
        data = request.split(b"\r\n\r\n")
        header = data[0].split(b"\r\n")
        header = header[0].split(b" ")

        response = {
            "header_top": header,
            "type": header[0],
            "body": data[1]
        }
        return response

    @staticmethod
    def create_msg(body: bytes, body_type: bytes):

        # gets the message body and its type, and returns the full http request template for use
        header = f"HTTP/1.0 200 OK\r\nContent-Length:{len(body)}\r\nContent-Type:{body_type}; charset=utf-8 \r\n\r\n"
        response = header.encode()
        response += body
        return response
