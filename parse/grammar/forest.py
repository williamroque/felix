import re

from felix.parse.grammar.tree import Node, Leaf, Tree
from felix.parse.grammar.expectations import ExpectationTypes
from felix.parse.token.tokens import Tokens
from felix.parse.errors import UnexpectedToken


class Bioregion:
    def __init__(self, token_tensor):
        self.token_tensor = token_tensor
        self.forests = []

    def __repr__(self):
        output = ''

        for forest in self.forests:
            output += 'Forest\n'

            for tree in forest:
                output += repr(tree)

            output += '\n'

        return output

    def plant(self):
        for line in self.token_tensor:
            forest = []

            for component in line:
                tree = Tree()

                char_index = 0
                line_expectations = []
                next_expectation = None
                active_nodes = []

                component_type = component[0]

                for token in component[1:]:
                    if token.type is Tokens.BLANK:
                        char_index += token.end
                        continue
                    
                    if next_expectation is not None and token.type not in next_expectation:
                        error = UnexpectedToken(
                            component_type = component_type.name,
                            expected_token = next_expectation[0].value,
                            token = token.type.value,
                            line = token.line_num + 1,
                            source = token.line_source,
                            char_index = char_index
                        )
                        error.effect()
                    else:
                        next_expectation = None

                    if line_expectations and token.type in line_expectations[-1]:
                        line_expectations.pop()

                    expectations = token.backend.build_expectation(token)
                    if type(expectations) != tuple:
                        expectations = tuple([expectations])

                    for expectation in expectations:
                        if expectation.type is ExpectationTypes.AUTO:
                            continue

                        token_type = expectation.token_type
                        if not isinstance(token_type, tuple):
                            token_type = tuple([token_type])

                        if expectation.type is ExpectationTypes.LINE:
                            line_expectations.append(token_type)
                        elif expectation.type is ExpectationTypes.NEXT:
                            next_expectation = token_type

                    for active_node in active_nodes[::-1]:
                        if token.type is active_node.terminator:
                            active_node.collapse()

                            if not active_node.propagate_terminator:
                                break

                    active_nodes = [node for node in active_nodes if not node.is_leaf]

                    node = token.backend.build_node(token)

                    if node is not None:
                        if active_nodes:
                            active_nodes[-1].add_child(node)
                        else:
                            tree.add_child(node)

                        if not node.is_leaf:
                            active_nodes.append(node)

                    char_index += token.end

                if line_expectations or active_nodes:
                    error = UnexpectedToken(
                        component_type = component_type.name,
                        expected_token = line_expectations[0][0].value,
                        token = 'EOL',
                        line = token.line_num + 1,
                        source = token.line_source,
                        char_index = len(token.line_source)
                    )
                    error.effect()

                forest.append(tree)

            self.forests.append(forest)
