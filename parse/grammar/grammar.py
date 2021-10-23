from felix.parse.grammar.forest import Bioregion


class Grammar:
    def __init__(self, token_tensor):
        self.token_tensor = token_tensor

        self.bioregion = None

    def analyze(self):
        self.bioregion = Bioregion(self.token_tensor)
        self.bioregion.construct()
