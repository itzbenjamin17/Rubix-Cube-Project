class Face:
    def __init__(self, colour,name):
        self.colour = colour
        self.name = name

    def setColour(self, colour):
        self.colour = colour

    def getColour(self):
        return self.colour
    
    def getName(self):
        return self.name
    
    def setName(self,name):
        self.name = name
