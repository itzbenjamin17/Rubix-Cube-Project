import numpy as np
from math import sin, cos, degrees
from Corner import Corner
from Edge import Edge
from Centre import Centre
from time import sleep
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
import pygame
FACE_COLOURS = {
    'U': (1, 1, 1),  # White
    'D': (1, 1, 0),  # Yellow
    'B': (1, 0, 0),  # Red
    'L': (0, 0, 1),  # Blue
    'R': (0, 1, 0),  # Green
    'F': (1, 0.65, 0)  # Orange
}

class Cube:
    def __init__(self, typeOfCube: int):
        self.typeOfCube = typeOfCube
        self.cubeDict = {}
        self.offset = (self.typeOfCube - 1) / 2.0
        self.corners = []
        self.edges = []
        self.centres = []

    def createEntireCube(self):
        '''Create the entire cube structure with cubies positioned at their coordinates'''
        cornerIndex = 0
        edgeIndex = 0
        for x in range(self.typeOfCube):
            for y in range(self.typeOfCube):
                for z in range(self.typeOfCube):
                    if (x,y,z) == (1,1,1):
                        continue
                    else:
                        colours = self.assignColours(x, y, z)
                        if len(colours) == 3:
                            cubie = Corner(x - self.offset, y - self.offset, z - self.offset, colours,cornerIndex)
                            self.corners.append(cubie)
                            cornerIndex += 1
                        elif len(colours) == 2:
                            if y == 2 or y == 0:
                                pieceType = "top"
                            elif x == 0 or x == 2:
                                pieceType = "side"
                            cubie = Edge(x - self.offset, y - self.offset, z - self.offset, colours,edgeIndex,pieceType)
                            self.edges.append(cubie)
                            edgeIndex += 1
                        else:
                            cubie = Centre(x - self.offset, y - self.offset, z - self.offset, colours)
                            self.centres.append(cubie)
                        self.cubeDict[(x, y, z)] = cubie


    def assignColours(self, x: int, y: int, z: int):
        '''Assign the correct colours to each face of the cubie based on its position'''
        colours = {}
        if y == self.typeOfCube - 1:  # Top face
            colours['U'] = FACE_COLOURS['U']
        if y == 0:  # Bottom face
            colours['D'] = FACE_COLOURS['D']
        if z == self.typeOfCube - 1:  # Front face
            colours['F'] = FACE_COLOURS['F']
        if z == 0:  # Back face
            colours['B'] = FACE_COLOURS['B']
        if x == 0:  # Left face
            colours['L'] = FACE_COLOURS['L']
        if x == self.typeOfCube - 1:  # Right face
            colours['R'] = FACE_COLOURS['R']
        return colours

    def render(self):
        '''Render the entire cube/rendering each cubie'''
        for cubie in self.cubeDict.values():
            cubie.createCubie()
    '''
    def getEdgePermutations(self):
        permutations = []
        for x in range(self.typeOfCube):
            for y in range(self.typeOfCube):
                for z in range(self.typeOfCube):
                    if (x,y,z) != (1,1,1):
                        if isinstance(self.cubeDict[(x,y,z)],Edge):
                            permutations.append(self.cubeDict[(x,y,z)].permutation)
        return permutations
             
    def getCornerPermutations(self):
        permutations = []
        for x in range(self.typeOfCube):
            for y in range(self.typeOfCube):
                for z in range(self.typeOfCube):
                    if (x,y,z) != (1,1,1):
                        if isinstance(self.cubeDict[(x,y,z)],Corner):
                            permutations.append(self.cubeDict[(x,y,z)].permutation)
        return permutations
    
    def getCornerOrientations(self):
        orientations = []
        for x in range(self.typeOfCube):
            for y in range(self.typeOfCube):
                for z in range(self.typeOfCube):
                    if (x,y,z) != (1,1,1):
                        if isinstance(self.cubeDict[(x,y,z)],Corner):
                            orientations.append(self.cubeDict[(x,y,z)].orientation)
        return orientations
    
    def getEdgeOrientations(self):
        orientations = []
        for x in range(self.typeOfCube):
            for y in range(self.typeOfCube):
                for z in range(self.typeOfCube):
                    if (x,y,z) != (1,1,1):
                        if isinstance(self.cubeDict[(x,y,z)],Edge):
                            orientations.append(self.cubeDict[(x,y,z)].orientation)
        return orientations
    
    
    def changeEdgeOrientations(self,oldPoints):
        for cubie in oldPoints.values():
            if isinstance(cubie,Edge):
                cubie.flipOrientation()
        
    def changeCornerOrientations(self, oldPoints):
        for cubie in oldPoints.values():
            if isinstance(cubie,Corner):
                cubie.setOrientation()
    '''

    def rotateFace(self, layer: int, axis: str, angle: float):
        if axis == "x":
            dimension = 0
        elif axis == "y":
            dimension = 1
        else:
            dimension = 2
        
        oldPoints = {pos: cubie for pos, cubie in self.cubeDict.items() if pos[dimension] == layer}


        for point in oldPoints.keys():
            if point in self.cubeDict:
                del self.cubeDict[point]

        xRotationMatrix = np.array([
                [1, 0, 0],
                [0, cos(angle), -sin(angle)],
                [0, sin(angle), cos(angle)]])
          
        yRotationMatrix = np.array([[cos(angle), 0, sin(angle)],
                [0, 1, 0],
                [-sin(angle), 0, cos(angle)]])
            
        zRotationMatrix = np.array([[cos(angle), -sin(angle), 0],
                [sin(angle), cos(angle), 0],
                [0, 0, 1]])
            
        if axis == "x":
            rotationMatrix = xRotationMatrix
        elif axis == "y":
            rotationMatrix = yRotationMatrix
        else:
            rotationMatrix = zRotationMatrix

        for (x,y,z), cubie in oldPoints.items():
            x -= self.offset
            y -= self.offset
            z -= self.offset
            newPoint = np.dot(rotationMatrix,np.array((x,y,z)))

            newX = round(newPoint[0] + self.offset)
            newY = round(newPoint[1] + self.offset)
            newZ = round(newPoint[2] + self.offset)

            
            cubie.updateCoordinates(newX - self.offset ,newY - self.offset ,newZ - self.offset)
            cubie.rotateVertices(rotationMatrix)
            self.cubeDict[(newX,newY,newZ)] = cubie

            #cubie.rotateFaces(axis,angle)
        '''    
        if axis == "z":
            self.changeCornerOrientations(oldPoints)   
        elif axis == "y":
            self.changeEdgeOrientations(oldPoints) 
        print("                    corner                                    edge")
        print(f"permutation {self.getCornerPermutations()}        {self.getEdgePermutations()} ")
        print(f"orientation {self.getCornerOrientations()}        {self.getEdgeOrientations()} ")
       

#faceNames = {"B" : 0, "L" : 1, "F" : 2 , "R" : 3, "U" : 4, "D" : 5}
    def isSolved(self):
        for (x,y,z),cube in self.cubeDict.items():
            if x == 0 and cube.faces[1].colour != (0,0,1):
                return False                     # R,G,B
            if x == 2 and cube.faces[3].colour != (0,1,0):
                return False
            if y == 2 and cube.faces[4].colour != (1,1,1):
                return False
            if y == 0 and cube.faces[5].colour != (1,1,0):
                return False
            if z == 0 and cube.faces[0].colour != (1,0,0):
                return False
            if z == 2 and cube.faces[2].colour != (1,0.65,0):
                return False
        return True
      '''

    def leftMove(self,angle: float):
        self.rotateFace(0,"x",angle)

    def upMove(self, angle: float):
        self.rotateFace(2,"y",angle)

    def downMove(self, angle: float):
        self.rotateFace(0,"y",angle)

    def rightMove(self, angle: float):
        for i in range(9):
            self.rotateFace(2,"x",angle/9)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.render()
            pygame.display.flip()
            sleep(0.005)
            
        
    def backMove(self, angle: float):
        self.rotateFace(0,"z",angle)

    def frontMove(self,angle: float):
        self.rotateFace(2,"z",angle)

    def middleMove(self,angle: float):
        self.rotateFace(1,"x",angle)

    def sliceSMove(self, angle: float):
        self.rotateFace(1,"z",angle)
    
    def sliceEMove(self,angle: float):
        self.rotateFace(1,"y",angle)