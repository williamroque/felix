"Contains the BOL class."

from felix.parse.token.tokens import Tokens, Backend
from felix.parse.grammar.expectations import ExpectationTypes, Expectation
from felix.parse.grammar.tree import Leaf


class BOL(Backend):
    "For representing the beginning of line."
    def __init__(self):
        "For representing the beginning of line."

    def __repr__(self):
        return 'BOL'

    @staticmethod
    def require_expectation(token):
        return False

    @staticmethod
    def build_expectations(token):
        return Expectation(ExpectationTypes.NEXT, (
            Tokens.G_CLEF,
            Tokens.F_CLEF,
            Tokens.GROUP_START,
            Tokens.NOTE
        )),

    @staticmethod
    def build_node(token):
        return Leaf(BOL())
