from enum import Enum, auto
from collections import namedtuple


class ExpectationTypes(Enum):
    NEXT = auto()
    LINE = auto()
    AUTO = auto()


Expectation = namedtuple('Expectation', ['type', 'token_type'])
