
from mememaker import MemeMaker
class Protocol:

    @staticmethod
    def receive(socket):
        return socket.recv(1024)

    # receives the http request and returns the type of request
    @staticmethod
    def proces_request(request):
        data = request.split("\r\n\r\n")
        header = data[0].split("\r\n")
        header = header[0].split(" ")

        response = {
            "header_top": header,
            "type": header[0],
            "body": data[1]
        }
        return header, data[1]

    @staticmethod
    def get_file_type(filenames):

        filename = filenames.split(".")[-1]

        if 'jpg' in filename or 'jpeg' in filename or 'ico' in filename or 'gif' in filename or 'png' in filename:
            filename = f"image/{filename}"
        elif 'js' in filename:
            filename = f"text/javascript"
        else:
            filename = f"text/{filename}"

        return filename


    @staticmethod
    def create_msg(body: bytes, body_type):

        # gets the message body and its type, and returns the full http request template for use
        header = f"HTTP/1.0 200 OK\r\nContent-Length:{len(body)}\r\nContent-Type:{body_type}; charset=utf-8 \r\n\r\n"
        response = header.encode()
        response += body
        return response

    @staticmethod
    def update_json(rnd: int, time: int):

        styles = MemeMaker.getStyles(rnd)
        captions = MemeMaker.get_caption_amount(rnd)

        res = ("{" + f'''
                "isOk": true,
               "memeIndex": {rnd},
               "captions": {captions},
               "styles":"{f'{styles}'[2:][:-1]}",
               "time": {time}
               ''' + "}").encode()
        return res
