import sys


class Error:
    MESSAGE = 'Parsing error.'
    PRIORITY = 1

    def __init__(self, **kwargs):
        self.message = self.__class__.MESSAGE.format(**kwargs)
        self.priority = self.__class__.PRIORITY

    def effect(self):
        sys.stderr.write(self.message)
        sys.stderr.flush()

        if self.priority == 0:
            sys.exit(1)


class TooManyLines(Error):
    MESSAGE = 'A line can have between 1 and 4 components.  The line on {line} exceeds 4.'
    PRIORITY = 0
