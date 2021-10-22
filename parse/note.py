"Contains the Note class."

import re
from felix.parse.tokens import ComponentTypes, Tokens, Backend


class Note(Backend):
    "For representing notes."
    def __init__(self, pitch, length):
        "For representing notes."

        self.pitch = pitch
        self.length = length

    @staticmethod
    def test_token(string, line_type):
        if line_type in (ComponentTypes.RIGHT, ComponentTypes.LEFT):
            maybe_test = r'^(1|2|4|8|16)$'
            note_test = r'^(1|2|4|8|16)?[A-Ga-g](b|#|n)?\.?$'

            if re.match(maybe_test, string):
                return Tokens.MAYBE
            if re.match(note_test, string):
                return Tokens.NOTE
