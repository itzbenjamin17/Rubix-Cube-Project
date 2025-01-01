from Cubie import Cubie

class Corner(Cubie):
    def __init__(self, x: int, y: int, z: int, colours: dict, permutation: int):
        super().__init__(x, y, z, colours)
        self.orientation = 0
        self.permutation = permutation

    def setOrientation(self):
        if self.faces[1].colour == (0,0,1) or self.faces[3].colour == (0,0,1) or self.faces[1].colour == (0,1,0) or self.faces[3].colour == (0,1,0):
            self.orientation = 0
        elif self.faces[1].colour == (1,0,0) or self.faces[3].colour == (1,0,0) or self.faces[1].colour == (1,0.65,0) or self.faces[3].colour == (1,0.65,0):
            self.orientation = 1
        else:
            self.orientation = 2
        
