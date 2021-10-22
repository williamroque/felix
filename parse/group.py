"Contains the Group class."

import re

from felix.parse.tokens import Tokens, ComponentTypes, Backend


class Group(Backend):
    "For representing annotated groups of notes."
    def __init__(self, notes, annotations):
        "For representing annotated groups of notes."

        self.notes = notes
        self.annotations = annotations

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
