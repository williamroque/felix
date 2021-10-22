"Contains the Blank class."

import re
from felix.parse.token.tokens import Tokens, Backend
from felix.parse.grammar.expectations import ExpectationTypes, Expectation
from felix.parse.grammar.tree import Leaf


class Blank(Backend):
    "For representing whitespace."
    def __init__(self):
        "For representing whitespace."

    def __repr__(self):
        return 'BLANK'

    @staticmethod
    def test_token(string, _):
        if re.match(r'^\s*$', string):
            return Tokens.BLANK

    @staticmethod
    def build_expectation(token):
        return Expectation(None, ExpectationTypes.AUTO)

    @staticmethod
    def build_node(token):
        return Leaf(Blank())
