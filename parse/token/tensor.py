from felix.parse.note import Note
from felix.parse.group import Group
from felix.parse.blank import Blank
from felix.parse.signature import Signature
from felix.parse.bar import Bar
from felix.parse.bol import BOL
from felix.parse.token.tokens import ComponentTypes, Token, Tokens
from felix.parse.errors import TooManyLines, InvalidToken


class TokenTensor:
    TOKEN_BACKENDS = [Signature, Note, Bar, Blank, Group]

    def __init__(self, source):
        self.source = source
        self.tensor = []

    def __iter__(self):
        for line in self.tensor:
            yield line

    def __repr__(self):
        output = ''

        for line in self.tensor:
            for component in line:
                for token in component:
                    output += str(token) + '\n\t'
                output += '\n'
            output += '-' * 10 + '\n'

        return output[:-14]

    def longest_token(self, tokens):
        longest = tokens[0]

        for token in tokens[1:]:
            if len(token.content) > len(longest.content):
                longest = token

        return longest

    def get_tokens(self, line_num, component, component_type):
        bol_token = Token('', component_type, BOL, line_num, component)
        bol_token.type = Tokens.BOL

        token_list = [bol_token]

        original_component = component
        char_index = 0

        while len(component) > 0:
            tokens = [Token(component, component_type, backend, line_num, original_component) for backend in TokenTensor.TOKEN_BACKENDS]
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

    def construct(self):
        line_num = 0

        token_tensor = []

        for line in self.get_components():
            if line is not ComponentTypes.BLANK:
                line_matrix = []
                for component_source, component_type in line:
                    line_matrix.append(
                        [component_type] + self.get_tokens(
                            line_num,
                            component_source,
                            component_type
                        )
                    )

                    line_num += 1

                token_tensor.append(line_matrix)
            else:
                line_num += 1

        self.tensor = token_tensor
