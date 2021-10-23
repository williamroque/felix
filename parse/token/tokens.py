from enum import Enum, auto
import re


class Tokens(Enum):
    MAYBE                      = auto()
    BOL                        = 'BOL'
    BLANK                      = 'BLANK'
    NOTE                       = '<Note>'
    GROUP_START                = '('
    GROUP_END                  = ')'
    GROUP_ANNOTATION_START     = '['
    GROUP_ANNOTATION_END       = ']'
    GROUP_ANNOTATION           = '<Annotation>'
    G_CLEF                     = 'GC'
    F_CLEF                     = 'FC'
    TIME_SIGNATURE             = 'p/q'
    KEY_SIGNATURE              = '<Key>'
    BAR                        = '|'


class ComponentTypes(Enum):
    BLANK  = auto()
    RIGHT  = auto()
    MIDDLE = auto()
    LEFT   = auto()
    BOTTOM = auto()


class Backend:
    @staticmethod
    def incremental_test(tests, string, token_type):
        for test in tests:
            if test.upper() == string.upper():
                return token_type

            for i in range(1, len(test)):
                if test[:i].upper() == string.upper():
                    return Tokens.MAYBE


class Token:
    def __init__(self, source, component_type, backend, line_num, line_source):
        self.source = source
        self.component_type = component_type
        self.backend = backend
        self.line_num = line_num
        self.line_source = line_source

        self.end = 0
        self.content = ''
        self.type = None

    def __repr__(self):
        return '<Token: {}, \'{}\', {}>'.format(
            self.type.name,
            self.content,
            self.backend.__name__
        )

    def consume(self):
        token_type = None

        i = 1

        while i <= len(self.source):
            test_result = self.backend.test_token(
                self.source[:i],
                self.component_type
            )

            if test_result is None:
                break

            token_type = test_result

            i += 1

        self.end = i - 1
        self.content = self.source[:i-1]
        self.type = token_type
