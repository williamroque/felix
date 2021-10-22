import sys
import re


class Error:
    MESSAGE = 'Parsing error.'
    PRIORITY = 1

    FORMATS = {
        'reset': '\033[0m',
        'cursor': '\033[31m',
        'error': '\033[31m',
        'help': '\033[32m->\x1B[3m '
    }

    def __init__(self, **kwargs):
        self.message = self.__class__.MESSAGE.format(**kwargs | Error.FORMATS)

        self.message = self.message.strip()
        self.message = re.sub(r' {4}', '', self.message)

        if 'char_index' in kwargs:
            self.message = self.message.replace('~', ' ' * kwargs['char_index'])

        self.priority = self.__class__.PRIORITY

    def effect(self):
        sys.stderr.write(self.message)
        sys.stderr.flush()

        if self.priority == 0:
            sys.exit(1)


class TooManyLines(Error):
    MESSAGE = """
    {help}A line can have between 1 and 4 components.{reset}
    {error}ERROR: Source line {line} exceeds 4:{reset}
    {source} {error}<--{reset}
    """
    PRIORITY = 0


class InvalidToken(Error):
    MESSAGE = """
    {help}Check documentation for component type {component_type}.{reset}
    {error}ERROR: Invalid token at source line {line}:{reset}
    {source}
    ~{cursor}^{reset}
    """
    PRIORITY = 0
