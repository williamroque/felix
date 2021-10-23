import re

from felix.parse.token.tokens import Tokens, ComponentTypes, Backend
from felix.parse.grammar.expectations import ExpectationTypes, Expectation
from felix.parse.grammar.tree import Node, Leaf


key_pattern = re.compile(r'^[A-G](b|#)$', re.I)
maybe_key_pattern = re.compile(r'^[A-G]$', re.I)

time_pattern = re.compile(r'^([1-9][0-9]?/[1-9][0-9]?|C)$', re.I)
maybe_time_pattern = re.compile(r'^[1-9][0-9]?/?$', re.I)


class Signature(Backend):
    def __init__(self, children, clef):
        self.clef = clef

        if children and time_pattern.match(children[0]):
            self.time = children[0]
            self.key_signature = children[1:]
        else:
            self.time = 'C'
            self.key_signature = children[1:]

    def __repr__(self):
        return '<Signature: {} {} [{}]>'.format(
            self.clef.name,
            self.time,
            '; '.join(self.key_signature)
        )

    @staticmethod
    def test_token(string, component_type):
        if component_type in (ComponentTypes.RIGHT, ComponentTypes.LEFT):
            if (test := Signature.incremental_test(
                    ['GC'],
                    string,
                    Tokens.G_CLEF
            )) is not None:
                return test
            if (test := Signature.incremental_test(
                    ['FC'],
                    string,
                    Tokens.F_CLEF
            )) is not None:
                return test

            if time_pattern.match(string):
                return Tokens.TIME_SIGNATURE
            if maybe_time_pattern.match(string):
                return Tokens.MAYBE

            if key_pattern.match(string):
                return Tokens.KEY_SIGNATURE
            if maybe_key_pattern.match(string):
                return Tokens.MAYBE

    @staticmethod
    def require_expectation(token):
        return token in (Tokens.G_CLEF, Tokens.F_CLEF, Tokens.TIME_SIGNATURE, Tokens.KEY_SIGNATURE)

    @staticmethod
    def build_expectations(token):
        if token.type in (Tokens.G_CLEF, Tokens.F_CLEF):
            return Expectation(ExpectationTypes.NEXT, (
                Tokens.BAR,
                Tokens.TIME_SIGNATURE,
                Tokens.KEY_SIGNATURE
            )),
        if token.type in (Tokens.TIME_SIGNATURE, Tokens.KEY_SIGNATURE):
            return Expectation(ExpectationTypes.NEXT, (
                Tokens.BAR,
                Tokens.KEY_SIGNATURE
            )),

        return Expectation(ExpectationTypes.AUTO, None),

    @staticmethod
    def build_node(token):
        if token.type in (Tokens.G_CLEF, Tokens.F_CLEF):
            return Node(Tokens.BAR, False, Signature, token.type)
        if token.type in (Tokens.TIME_SIGNATURE, Tokens.KEY_SIGNATURE):
            return Leaf(token.content)
