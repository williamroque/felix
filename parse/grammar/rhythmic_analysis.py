from felix.parse.signature import Signature
from felix.parse.grammar.tree import Node, Tree
from felix.parse.group import Group
from felix.parse.note import Note
from felix.parse.errors import InvalidMeasure


class RhythmicAnalyzer:
    def __init__(self, tree, line_num):
        self.tree = tree
        self.line_num = line_num

        first_leaf = self.tree.children[1].content

        self.beats = 4
        self.unit = 4

        if isinstance(first_leaf, Signature):
            if first_leaf.time.upper() != 'C':
                self.beats, self.unit = map(int, first_leaf.time.split('/'))

        self.measure = self.beats/self.unit

    def collapse(self, node):
        if isinstance(node, (Tree, Group)):
            leaves = []

            for child in node.children:
                leaves += self.collapse(child)

            return leaves
        elif isinstance(node, Note):
            return [node]
        elif isinstance(node, Node):
            return self.collapse(node.content)

        return []

    def analyze(self):
        notes = self.collapse(self.tree)

        current_measure = 0
        formatted_notes = []

        for note in notes:
            length = 1/note.length

            if note.dotted:
                length += length/2

            current_measure += length
            formatted_notes.append('{}<{}>'.format(
                note.key,
                length*self.unit
            ))

            if current_measure > self.measure:
                source = ' '.join(formatted_notes)

                error = InvalidMeasure(
                    line = self.line_num,
                    source = source,
                    char_index = len(source) - 1,
                    beats = self.beats
                )
                error.effect()

                return
            if current_measure == self.measure:
                current_measure = 0
                formatted_notes.append('|')

        if current_measure:
            source = ' '.join(formatted_notes)

            error = InvalidMeasure(
                line = self.line_num,
                source = source,
                char_index = len(source) - 1,
                beats = self.beats
            )
            error.effect()
