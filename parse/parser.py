"Main entry point for parser."

from felix.parse.note import Note
from felix.parse.group import Group
from felix.parse.blank import Blank
from felix.parse.tokens import ComponentTypes, Token, Tokens
from felix.parse.errors import TooManyLines, InvalidToken


class Parser:
    "The syntax parser."

    TOKEN_BACKENDS = [Note, Blank, Group]

    def __init__(self, source):
        "The syntax parser."

        self.source = source

    def longest_token(self, tokens):
        longest = tokens[0]

        for token in tokens[1:]:
            if len(token.content) > len(longest.content):
                longest = token

        return longest

    def get_tokens(self, line_num, component, component_type):
        token_list = []

        original_component = component
        char_index = 0

        while len(component) > 0:
            tokens = [Token(component, component_type, backend) for backend in Parser.TOKEN_BACKENDS]
            potential_tokens = []

            for token in tokens:
                token.consume()

                if token.type not in (None, Tokens.MAYBE):
                    potential_tokens.append(token)

            if len(potential_tokens) == 0:
                error = InvalidToken(
                    line=line_num + 1,
                    component_type=component_type.name,
                    source=original_component,
                    char_index=char_index,
                )
                error.effect()

            token = self.longest_token(potential_tokens)

            token_list.append(token)
            component = component[token.end:]

            char_index += token.end

        return token_list

    def get_components(self):
        line_lengths = [0]
        components = []

        source_lines = self.source.split('\n')

        for line_num, source_line in enumerate(source_lines):
            length = line_lengths[-1]

            if source_line == '':
                line_source = source_lines[line_num-length:line_num]

                if length == 0:
                    components.append(ComponentTypes.BLANK)
                elif length == 1:
                    components.append(zip(
                        line_source,
                        (ComponentTypes.RIGHT,)
                    ))
                elif length == 2:
                    components.append(zip(line_source, (
                        ComponentTypes.RIGHT,
                        ComponentTypes.LEFT
                    )))
                elif length == 3:
                    components.append(zip(line_source, (
                        ComponentTypes.RIGHT,
                        ComponentTypes.MIDDLE,
                        ComponentTypes.LEFT
                    )))
                elif length == 4:
                    components.append(zip(line_source, (
                        ComponentTypes.RIGHT,
                        ComponentTypes.MIDDLE,
                        ComponentTypes.LEFT,
                        ComponentTypes.BOTTOM
                    )))

                line_lengths.append(0)

            elif line_lengths[-1] > 3:
                error = TooManyLines(
                    line=line_num,
                    source='\n'.join(
                        source_lines[line_num-length:line_num + 1]
                    )
                )
                error.effect()

            else:
                line_lengths[-1] += 1

        return components

    def parse(self):
        line_num = 0

        token_matrix = []

        for line in self.get_components():
            if line is not ComponentTypes.BLANK:
                for component_source, component_type in line:
                    token_matrix.append(
                        self.get_tokens(
                            line_num,
                            component_source,
                            component_type
                        )
                    )

                    line_num += 1
            else:
                line_num += 1

        return token_matrix
