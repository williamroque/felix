"Contains the Group class."

import re

from felix.parse.token.tokens import Tokens, ComponentTypes, Backend
from felix.parse.grammar.expectations import ExpectationTypes, Expectation
from felix.parse.grammar.tree import Node, Leaf


class Group(Backend):
    "For representing annotated groups of notes."
    def __init__(self, children):
        "For representing annotated groups of notes."

        self.children = children[:-1]
        self.annotations = children[-1]

    def __repr__(self):
        output = '<Group: {}>'.format(self.annotations)

        for member in self.children:
            output += '\n' + re.sub('(^|\n)', '\\1\t', repr(member))

        return output

    @staticmethod
    def test_token(string, component_type):
        annotation_tests = ['1', '2', '3', '4', '5', 'lig', 'app', 'tr']

        if component_type in (ComponentTypes.RIGHT, ComponentTypes.LEFT):
            if string == '(':
                return Tokens.GROUP_START
            if string == ')':
                return Tokens.GROUP_END
            if string == '[':
                return Tokens.GROUP_ANNOTATION_START
            if string == ']':
                return Tokens.GROUP_ANNOTATION_END
            if (test := Group.incremental_test(
                    annotation_tests,
                    string,
                    Tokens.GROUP_ANNOTATION
            )) is not None:
                return test

    @staticmethod
    def require_expectation(token):
        return token in (Tokens.GROUP_END, Tokens.GROUP_ANNOTATION, Tokens.GROUP_ANNOTATION_END)

    @staticmethod
    def build_expectations(token):
        if token.type is Tokens.GROUP_START:
            return Expectation(ExpectationTypes.LINE, Tokens.GROUP_END),
        if token.type is Tokens.GROUP_END:
            return Expectation(ExpectationTypes.NEXT, Tokens.GROUP_ANNOTATION_START),
        if token.type is Tokens.GROUP_ANNOTATION_START:
            return (
                Expectation(ExpectationTypes.NEXT, Tokens.GROUP_ANNOTATION),
                Expectation(ExpectationTypes.LINE, Tokens.GROUP_ANNOTATION_END)
            )
        if token.type is Tokens.GROUP_ANNOTATION:
            return Expectation(ExpectationTypes.NEXT, (
                Tokens.GROUP_ANNOTATION_END,
                Tokens.GROUP_ANNOTATION
            )),

        return Expectation(ExpectationTypes.AUTO, None),

    @staticmethod
    def build_node(token):
        if token.type is Tokens.GROUP_START:
            return Node(Tokens.GROUP_ANNOTATION_END, False, Group)
        if token.type is Tokens.GROUP_ANNOTATION_START:
            return Node(Tokens.GROUP_ANNOTATION_END, True, Annotations)
        if token.type is Tokens.GROUP_ANNOTATION:
            return Leaf(token.content)


class Annotations:
    def __init__(self, annotations):
        self.annotations = annotations

    def __repr__(self):
        return ' '.join(self.annotations)
