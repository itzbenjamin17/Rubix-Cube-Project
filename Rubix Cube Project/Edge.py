from Cubie import Cubie

class Edge(Cubie):
    def __init__(self, x: int, y: int, z: int, colours: dict,  permutation: int, type: str):
        super().__init__(x, y, z, colours)
        self.orientation = 0
        self.permutation = permutation
        self.type = type

    def flipOrientation(self):
        self.orientation = 1 - self.orientation

          