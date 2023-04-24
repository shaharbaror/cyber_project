class MemeMaker:
    def __init__(self):
        pass
    @staticmethod
    def getStyles(number: bytes):
        with open("paths.txt", "rb") as f:
            style = f.read().split(b"\n")[number - 1]
        return style


    @staticmethod
    def getImage(number: bytes):
        with open(f"./MemeBank/meme{get_path(number)}", "rb") as f:
            return f.read()


def get_path(number: bytes):
    if number < 10:
        return f"0{number}"
    else:
        return number