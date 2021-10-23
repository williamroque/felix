"Contains the Note class."

import re
from felix.parse.token.tokens import ComponentTypes, Tokens, Backend
from felix.parse.grammar.expectations import ExpectationTypes, Expectation
from felix.parse.grammar.tree import Leaf


class Note(Backend):
    "For representing notes."
    def __init__(self, key, octave, length, semitone, dotted):
        "For representing notes."

        self.key = key
        self.octave = octave
        self.length = length
        self.semitone = semitone
        self.dotted = dotted

    def __repr__(self):
        return '<Note: {}{}, len. {}{}, oct. {}>'.format(
            self.key,
            '' if self.semitone == 'n' else self.semitone,
            self.length,
            '.' if self.dotted else '',
            self.octave
        )

    @staticmethod
    def test_token(string, line_type):
        if line_type in (ComponentTypes.RIGHT, ComponentTypes.LEFT):
            maybe_test = r'^(1|2|4|8|16)$'
            note_test = r'^(1|2|4|8|16)?[A-Ga-g][1-8]?(b|#|n)?\.?$'

            if re.match(maybe_test, string):
                return Tokens.MAYBE
            if re.match(note_test, string):
                return Tokens.NOTE

    @staticmethod
    def build_expectation(token):
        return Expectation(None, ExpectationTypes.AUTO)

    @staticmethod
    def build_node(token):
        match = re.match(r'^(?P<length>1|2|4|8|16)?(?P<key>[A-Ga-g])(?P<octave>[1-8])?(?P<semitone>b|#|n)?(?P<dot>\.)?$', token.content)

        length = 4
        octave = 4
        semitone = 'n'

        key = match.group('key')

        dotted = False

        if (group := match.group('length')) is not None:
            length = int(group)

        if (group := match.group('octave')) is not None:
            octave = int(group)

        if (group := match.group('semitone')) is not None:
            semitone = group

        if match.group('dot') is not None:
            dotted = True

        return Leaf(Note(key, octave, length, semitone, dotted))
