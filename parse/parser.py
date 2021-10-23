"Main entry point for parser."

from felix.parse.token.tensor import TokenTensor
from felix.parse.grammar.grammar import Grammar
from felix.parse.errors import TooManyLines, InvalidToken


class Parser:
    "The syntax parser."

    def __init__(self, source):
        "The syntax parser."

        self.source = source

    def parse(self):
        token_tensor = TokenTensor(self.source)
        token_tensor.construct()

        grammar = Grammar(token_tensor)
        grammar.analyze()
