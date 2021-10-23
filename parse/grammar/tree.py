import re


class Tree:
    def __init__(self):
        self.children = []

    def __repr__(self):
        output = 'Tree\n'

        for child in self.children:
            output += re.sub('(^|\n)', '\\1\t', repr(child))

            if child.is_leaf:
                output += '\n'

        return output

    def add_child(self, child):
        self.children.append(child)

    def collapse(self):
        for child in self.children:
            if not child.is_leaf:
                child.collapse()


class Node:
    def __init__(self, terminator, propagate_terminator, backend, *backend_arguments):
        self.terminator = terminator
        self.propagate_terminator = propagate_terminator
        self.backend = backend
        self.backend_arguments = backend_arguments

        self.children = []

        self.is_leaf = False
        self.content = None

    def __repr__(self):
        if self.is_leaf:
            return '<Leaf: {}>'.format(self.content)

        output = '<Node: {}>\n'.format(self.backend.__name__)

        for child in self.children:
            output += re.sub('(^|\n)', '\\1\t', repr(child))

            if child.is_leaf:
                output += '\n'

        return output

    def add_child(self, child):
        if not self.is_leaf:
            self.children.append(child)

    def collapse(self):
        for child in self.children:
            if not child.is_leaf:
                child.collapse()

        self.content = self.backend(
            [child.content for child in self.children],
            *self.backend_arguments
        )
        self.children = []
        self.is_leaf = True


class Leaf(Node):
    def __init__(self, content):
        self.is_leaf = True
        self.content = content
