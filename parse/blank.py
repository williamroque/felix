"Contains the Blank class."

import re
from felix.parse.tokens import Tokens, Backend


class Blank(Backend):
    "For representing whitespace."
    def __init__(self):
        "For representing whitespace."

    @staticmethod
    def test_token(string, _):
        if re.match(r'^\s*$', string):
            return Tokens.BLANK
