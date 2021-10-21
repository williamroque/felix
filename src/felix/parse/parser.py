"Main entry point for parser."

from felix.parse.note import Note
from felix.parse.tokens import ComponentTypes
from felix.parse.errors import TooManyLines


class Parser:
    "The syntax parser."

    def __init__(self, source):
        "The syntax parser."

        self.source = source

    def get_tokens(self, component, line_type):
        pass

    def parse(self):
        line_lengths = [0]
        component_types = []

        for line_num, source_line in enumerate(self.source.split('\n')):
            if source_line == '':
                length = line_lengths[-1]

                if length == 0:
                    component_types.append(ComponentTypes.BLANK)
                elif length == 1:
                    component_types.append((ComponentTypes.RIGHT))
                elif length == 2:
                    component_types.append((
                        ComponentTypes.RIGHT,
                        ComponentTypes.LEFT
                    ))
                elif length == 3:
                    component_types.append((
                        ComponentTypes.RIGHT,
                        ComponentTypes.MIDDLE,
                        ComponentTypes.LEFT
                    ))
                elif length == 4:
                    component_types.append((
                        ComponentTypes.RIGHT,
                        ComponentTypes.MIDDLE,
                        ComponentTypes.LEFT,
                        ComponentTypes.BOTTOM
                    ))

                line_lengths.append(0)

            elif line_lengths[-1] > 3:
                error = TooManyLines(line_num)
                error.effect()

            else:
                line_lengths[-1] += 1

        print(component_types)
