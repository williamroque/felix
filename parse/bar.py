from felix.parse.token.tokens import ComponentTypes, Tokens, Backend
from felix.parse.grammar.expectations import ExpectationTypes, Expectation
from felix.parse.grammar.tree import Leaf


class Bar(Backend):
    def __init__(self):
        pass

    def __repr__(self):
        return '<Bar: \'|\'>'

    @staticmethod
    def test_token(string, line_type):
        if string == '|':
            return Tokens.BAR

    @staticmethod
    def require_expectation(token):
        return False

    @staticmethod
    def build_expectations(token):
        return Expectation(ExpectationTypes.AUTO, None),

    @staticmethod
    def build_node(token):
        return Leaf(Bar())
