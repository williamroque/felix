import re

from felix.parse.grammar.tree import Tree


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

    def construct(self):
        for line in self.token_tensor:
            forest = []

            for component in line:
                tree = Tree(component)
                tree.construct()

                forest.append(tree)

            self.forests.append(forest)
