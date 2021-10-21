from enum import Enum, auto


class Tokens(Enum):
    MAYBE = auto()
    NOTE  = auto()


class ComponentTypes(Enum):
    BLANK  = auto()
    RIGHT  = auto()
    MIDDLE = auto()
    LEFT   = auto()
    BOTTOM = auto()
