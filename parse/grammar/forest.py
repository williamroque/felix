import re

from felix.parse.grammar.tree import Node, Leaf, Tree
from felix.parse.grammar.expectations import ExpectationTypes
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

            output += '\n' + '-' * 10 + '\n'

        return output

    def plant(self):
        for line in self.token_tensor:
            forest = []

            for component in line:
                tree = Tree()

                line_expectations = []
                next_expectation = None
                active_nodes = []

                component_type = component[0]

                for token in component[1:]:
                    if next_expectation is not None and token.token_type is not next_expectation:
                        error = UnexpectedToken(
                            component_type = component_type,
                            expected_token = next_expectation.token_type.name,
                            token = token.token_type.name,
                            line_num = token.line_num,
                            source = token.line_source,
                            char_index = token.end - len(token.content)
                        )
                        error.effect()

                    line_expectations = [exp for exp in line_expectations if token.token_type is not exp]

                    expectation = token.backend.build_expectation(token)

                    if expectation.type is ExpectationTypes.LINE:
                        line_expectations.append(expectation.token_type)
                    elif expectation.type is ExpectationTypes.NEXT:
                        next_expectation = expectation.token_type

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

                if line_expectations or active_nodes:
                    error = UnexpectedToken(
                        component_type = component_type,
                        expected_token = line_expectations[0].token_type.name,
                        token = 'EOL',
                        line_num = token.line_num,
                        source = token.line_source,
                        char_index = len(token.line_source)
                    )
                    error.effect()


                forest.append(tree)

            self.forests.append(forest)
