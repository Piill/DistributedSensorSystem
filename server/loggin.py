
class Logger:
    def __init__(self, level):
        self.level = level

    def log(self, level, message):
        if level >= self.level:
            print(message)

