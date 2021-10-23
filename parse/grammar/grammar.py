from felix.parse.grammar.forest import Bioregion


class Grammar:
    def __init__(self, token_tensor):
        self.token_tensor = token_tensor

    def parse(self):
        bioregion = Bioregion(self.token_tensor)
        bioregion.construct()

        return bioregion
