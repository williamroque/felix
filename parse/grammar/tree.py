import re

from felix.parse.errors import UnexpectedToken
from felix.parse.grammar.expectations import ExpectationTypes
from felix.parse.token.tokens import Tokens


class Tree:
    def __init__(self, component):
        self.children = []

        self.component_type, *self.component = component

        self.char_index = 0
        self.active_nodes = []
        self.line_expectations = []
        self.next_expectation = None

    def check_token(self, token):
        if token.backend.require_expectation(token.type):
            if not (
                    self.next_expectation is not None and token.type in self.next_expectation
                    or any(token.type in exp for exp in self.line_expectations)
            ):
                error = UnexpectedToken(
                    component_type = self.component_type.name,
                    token = token.type.value,
                    line = token.line_num + 1,
                    source = token.line_source,
                    char_index = self.char_index
                )
                error.effect()

        if self.next_expectation is not None and token.type not in self.next_expectation:
            error = UnexpectedToken(
                component_type = self.component_type.name,
                expected_token = self.next_expectation[0].value,
                token = token.type.value,
                line = token.line_num + 1,
                source = token.line_source,
                char_index = self.char_index
            )
            error.effect()

    def build_expectations(self, token):
        self.next_expectation = None

        if self.line_expectations and token.type in self.line_expectations[-1]:
            self.line_expectations.pop()

        expectations = token.backend.build_expectations(token)

        for expectation in expectations:
            if expectation.type is not ExpectationTypes.AUTO:
                token_type = expectation.token_type
                if not isinstance(token_type, tuple):
                    token_type = tuple([token_type])

                if expectation.type is ExpectationTypes.LINE:
                    self.line_expectations.append(token_type)
                elif expectation.type is ExpectationTypes.NEXT:
                    self.next_expectation = token_type

    def update_active_nodes(self, token):
        for active_node in self.active_nodes[::-1]:
            if token.type is active_node.terminator:
                active_node.collapse()

                if not active_node.propagate_terminator:
                    break

        self.active_nodes = [node for node in self.active_nodes if not node.is_leaf]

    def construct_node(self, token):
        if token.type is Tokens.BLANK:
            self.char_index += token.end
            return

        self.check_token(token)
        self.build_expectations(token)
        self.update_active_nodes(token)

        node = token.backend.build_node(token)

        if node is not None:
            if self.active_nodes:
                self.active_nodes[-1].add_child(node)
            else:
                self.add_child(node)

            if not node.is_leaf:
                self.active_nodes.append(node)

        self.char_index += token.end

    def construct(self):
        for token in self.component:
            self.construct_node(token)

        if self.line_expectations or self.active_nodes:
            error = UnexpectedToken(
                component_type = self.component_type.name,
                expected_token = self.line_expectations[0][0].value,
                token = 'EOL',
                line = token.line_num + 1,
                source = token.line_source,
                char_index = len(token.line_source)
            )
            error.effect()

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
