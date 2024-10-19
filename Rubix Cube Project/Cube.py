import numpy as np
from math import sin, cos
from Corner import Corner
from Edge import Edge
from Centre import Centre
from time import sleep
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
import pygame

ANIMATION_DIVISION = 9
TIME_WAIT = 0.005

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

    def rotateFace(self, layer: int, axis: str, angle: float):
        if axis == "x":
            dimension = 0
        elif axis == "y":
            dimension = 1
        else:
            dimension = 2
        # Finding all the cubies that are going to be rotated
        oldPoints = {pos: cubie for pos, cubie in self.cubeDict.items() if round(pos[dimension]) == layer}

        for point in oldPoints.keys():
            if point in self.cubeDict:
                del self.cubeDict[point]
                             
        if axis == "x":
            rotationMatrix = np.array([
                [1, 0, 0],
                [0, cos(angle), -sin(angle)],
                [0, sin(angle), cos(angle)]])
            
        elif axis == "y":
            rotationMatrix = np.array([[cos(angle), 0, sin(angle)],
                [0, 1, 0],
                [-sin(angle), 0, cos(angle)]])
        else:
            rotationMatrix = np.array([[cos(angle), -sin(angle), 0],
                [sin(angle), cos(angle), 0],
                [0, 0, 1]])

        for (x,y,z), cubie in oldPoints.items():
            x -= self.offset
            y -= self.offset
            z -= self.offset
            
            newPoint = np.dot(rotationMatrix,np.array((x,y,z)))

            newX = (newPoint[0] + self.offset)
            newY = (newPoint[1] + self.offset)
            newZ = (newPoint[2] + self.offset)
            
            cubie.updateCoordinates(newX - self.offset ,newY - self.offset ,newZ - self.offset)
            cubie.rotateVertices(rotationMatrix)
            self.cubeDict[(newX,newY,newZ)] = cubie

    def leftMove(self,angle: float):
        #self.rotateFace(0,"x",angle)
        for _ in range(ANIMATION_DIVISION):
            self.rotateFace(0,"x",angle/ANIMATION_DIVISION)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.render()
            pygame.display.flip()
            sleep(TIME_WAIT)

    def rightMove(self, angle: float):
        #self.rotateFace(2,"x",angle)
        for _ in range(ANIMATION_DIVISION):
            self.rotateFace(2,"x",angle/ANIMATION_DIVISION)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.render()
            pygame.display.flip()
            sleep(TIME_WAIT)

    def upMove(self, angle: float):
        #self.rotateFace(2,"y",angle)
        for _ in range(ANIMATION_DIVISION):
            self.rotateFace(2,"y",angle/ANIMATION_DIVISION)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.render()
            pygame.display.flip()
            sleep(TIME_WAIT)

    def downMove(self, angle: float):
        #self.rotateFace(0,"y",angle)
        for _ in range(ANIMATION_DIVISION):
            self.rotateFace(0,"y",angle/ANIMATION_DIVISION)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.render()
            pygame.display.flip()
            sleep(TIME_WAIT)
         
    def backMove(self, angle: float):
        #self.rotateFace(0,"z",angle)
        for _ in range(ANIMATION_DIVISION):
            self.rotateFace(0,"z",angle/ANIMATION_DIVISION)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.render()
            pygame.display.flip()
            sleep(TIME_WAIT)

    def frontMove(self,angle: float):
        #self.rotateFace(2,"z",angle)
        for _ in range(ANIMATION_DIVISION):
            self.rotateFace(2,"z",angle/ANIMATION_DIVISION)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.render()
            pygame.display.flip()
            sleep(TIME_WAIT)
