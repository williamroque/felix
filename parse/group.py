"Contains the Group class."

import re

from felix.parse.token.tokens import Tokens, ComponentTypes, Backend
from felix.parse.grammar.expectations import ExpectationTypes, Expectation
from felix.parse.grammar.tree import Node


class Group(Backend):
    "For representing annotated groups of notes."
    def __init__(self, elements):
        "For representing annotated groups of notes."

        self.elements = elements

    def __repr__(self):
        return '<Group>'

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
            if string == ';':
                return Tokens.GROUP_ANNOTATION_SEPARATOR
            if (test := Group.incremental_test(
                    annotation_tests,
                    string,
                    Tokens.GROUP_ANNOTATION
            )) is not None:
                return test

    @staticmethod
    def build_expectation(token):
        if token.type is Tokens.GROUP_START:
            return Expectation(Tokens.GROUP_END, ExpectationTypes.LINE)
        if token.type is Tokens.GROUP_END:
            return Expectation(Tokens.GROUP_ANNOTATION_START, ExpectationTypes.NEXT)
        if token.type is Tokens.GROUP_ANNOTATION_START:
            return (
                Expectation(Tokens.GROUP_ANNOTATION_END, ExpectationTypes.LINE),
                Expectation(Tokens.GROUP_ANNOTATION, ExpectationTypes.NEXT),
            )
        if token.type is Tokens.GROUP_ANNOTATION:
            return Expectation((
                Tokens.GROUP_ANNOTATION_END,
                Tokens.GROUP_ANNOTATION
            ), ExpectationTypes.NEXT),

        return Expectation(None, ExpectationTypes.AUTO)

    @staticmethod
    def build_node(token):
        if token.type is Tokens.GROUP_START:
            return Node(Tokens.GROUP_ANNOTATION_END, False, Group)
        if token.type is Tokens.GROUP_ANNOTATION_START:
            return Node(Tokens.GROUP_ANNOTATION_END, True, Annotation)


class Annotation:
    def __init__(self, annotations):
        self.annotations = annotations
