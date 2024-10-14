from Cubie import Cubie

class Corner(Cubie):
    def __init__(self, x: int, y: int, z: int, colours: dict, permutation: int):
        super().__init__(x, y, z, colours)
        self.orientation = 0
        self.permutation = permutation

    #if either the top or bottom face is either yellow or white its orientated correctly (0)
    #if either the front face or the back face is either yellow or white its orientated wrong (1)
    #else its 2 left or right
    def setOrientation(self):
        Colours = [(1,1,1),(1,1,0)]

        if self.faces[4].getColour() in Colours or self.faces[5].getColour() in Colours:
            self.orientation = 0
        elif self.faces[0].getColour() in Colours or self.faces[2].getColour() in Colours:
            self.orientation =  1
        else:
            self.orientation = 2
        
