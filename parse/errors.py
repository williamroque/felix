import sys
import re


class Error:
    MESSAGE = 'Parsing error.'
    ALTERNATIVE_MESSAGES = []
    PRIORITY = 1

    FORMATS = {
        'reset': '\033[0m',
        'cursor': '\033[31m',
        'error': '\033[31m',
        'warning': '\u001b[33m',
        'help': '\033[32m->\x1B[3m '
    }

    def __init__(self, **kwargs):
        self.message = None

        try:
            self.message = self.__class__.MESSAGE.format(
                **kwargs | Error.FORMATS
            )
        except KeyError:
            for message in self.__class__.ALTERNATIVE_MESSAGES:
                try:
                    self.message = message.format(**kwargs | Error.FORMATS)
                    break
                except KeyError:
                    pass
            else:
                self.message = 'Parsing error.'

        self.message = self.message.strip()
        self.message = re.sub(r' {4}', '', self.message)

        if 'char_index' in kwargs:
            self.message = self.message.replace('~', ' ' * kwargs['char_index'])

        self.priority = self.__class__.PRIORITY

    def effect(self):
        sys.stderr.write(self.message + '\n')
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
    {error}ERROR: Invalid token on source line {line}:{reset}
    {source}
    ~{error}^{reset}
    """
    PRIORITY = 0


class UnexpectedToken(Error):
    MESSAGE = """
    {help}Check documentation for component type {component_type}.{reset}
    {error}ERROR: Expected one of [{expected_tokens}] but got {token} on source line {line}:{reset}
    {source}
    ~{error}^{reset}
    """
    ALTERNATIVE_MESSAGES = [
        """
        {help}Check documentation for component type {component_type}.{reset}
        {error}ERROR: Expected {expected_token} but got {token} on source line {line}:{reset}
        {source}
        ~{error}^{reset}
        """,
        """
        {help}Check documentation for component type {component_type}.{reset}
        {error}ERROR: Unexpected {token} on source line {line}:{reset}
        {source}
        ~{error}^{reset}
        """
    ]
    PRIORITY = 0


class InvalidMeasure(Error):
    MESSAGE = """
    {help}Try changing note lengths or adding rests.{reset}
    {warning}WARNING: Wrong measure length on sheet line {line} (expected {beats} beats):{reset}
    {source}
    ~{warning}^{reset}
    """
    PRIORITY = 1
