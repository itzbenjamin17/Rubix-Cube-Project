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

    def getEdgeOrientation(self):
        orientations = []
        print("Edge orientation")
        for edge in self.edges:
            orientations.append(f"{round(edge.x),round(edge.y),round(edge.z)}:{edge.orientation}")
        return orientations

    def getCornerOrientation(self):
        orientations = []
        print("Corner orientation")
        for corner in self.corners:
            orientations.append(f"{round(corner.x),round(corner.y),round(corner.z)}:{corner.orientation}")
        return orientations
    def findKey(self,targetKey):
        for key in self.cubeDict.keys():
            roundedKey = tuple(round(coord,0) for coord in key)
            if roundedKey == targetKey:
                return key
            
    def getEdgePerumation(self):
        permutations = []
        print("Edge permutation")
        for x in range(self.typeOfCube):
            for y in range(self.typeOfCube):
                for z in range(self.typeOfCube):
                    targetCubie = self.cubeDict[self.findKey((x,y,z))]
                    if type(targetCubie) is Edge:
                        permutations.append(f"{round(targetCubie.x),round(targetCubie.y),round(targetCubie.z)}:{targetCubie.permutation}")
        '''
        for edge in self.edges:
                permutations.append(f"{round(edge.x),round(edge.y),round(edge.z)}:{edge.permutation}")
        return permutations
        '''
    def getCornerPerumation(self):
        permutations = []
        print("Corner permutation")
        for x in range(self.typeOfCube):
            for y in range(self.typeOfCube):
                for z in range(self.typeOfCube):
                    targetCubie = self.cubeDict[self.findKey((x,y,z))]
                    if type(targetCubie) is Corner:
                        permutations.append(f"{round(targetCubie.x),round(targetCubie.y),round(targetCubie.z)}:{targetCubie.permutation}")
        '''
        for corner in self.corners:
                permutations.append(f"{round(corner.x),round(corner.y),round(corner.z)}:{corner.permutation}")
        return permutations
    '''
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
        for _ in range(ANIMATION_DIVISION):
            self.rotateFace(0,"x",angle/ANIMATION_DIVISION)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.render()
            pygame.display.flip()
            sleep(TIME_WAIT)

        for (x,_,_), cubie in self.cubeDict.items():
          if round(x) == 0:
              cubie.rotateFaces("x",angle)
                

    def rightMove(self, angle: float):
        for _ in range(ANIMATION_DIVISION):
            self.rotateFace(2,"x",angle/ANIMATION_DIVISION)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.render()
            pygame.display.flip()
            sleep(TIME_WAIT)

        for (x,_,_), cubie in self.cubeDict.items():
          if round(x) == 2:
              cubie.rotateFaces("x",angle)


    def upMove(self, angle: float):
        for _ in range(ANIMATION_DIVISION):
            self.rotateFace(2,"y",angle/ANIMATION_DIVISION)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.render()
            pygame.display.flip()
            sleep(TIME_WAIT)

        for (_,y,_), cubie in self.cubeDict.items():
          if round(y) == 2:
              cubie.rotateFaces("y",angle)

        for cubie in self.edges:
            if round(cubie.y) + self.offset == 2:
                cubie.flipOrientation()
        for cubie in self.corners:
            if round(cubie.y) + self.offset == 2:
                cubie.setOrientation()

        #print(self.getCornerOrientation())
        #print(self.getEdgeOrientation())
        print(self.getCornerPerumation())
        print(self.getEdgePerumation())

    def downMove(self, angle: float):
        for _ in range(ANIMATION_DIVISION):
            self.rotateFace(0,"y",angle/ANIMATION_DIVISION)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.render()
            pygame.display.flip()
            sleep(TIME_WAIT)

        for (_,y,_), cubie in self.cubeDict.items():
          if round(y) == 0:
              cubie.rotateFaces("y",angle)

        for cubie in self.edges:
            if round(cubie.y) + self.offset == 0:
                cubie.flipOrientation()
        for cubie in self.corners:
            if round(cubie.y) + self.offset == 0:
                cubie.setOrientation()
         
    def backMove(self, angle: float):
        for _ in range(ANIMATION_DIVISION):
            self.rotateFace(0,"z",angle/ANIMATION_DIVISION)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.render()
            pygame.display.flip()
            sleep(TIME_WAIT)

        for (_,_,z), cubie in self.cubeDict.items():
          if round(z) == 0:
              cubie.rotateFaces("z",angle)

    def frontMove(self,angle: float):
        for _ in range(ANIMATION_DIVISION):
            self.rotateFace(2,"z",angle/ANIMATION_DIVISION)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.render()
            pygame.display.flip()
            sleep(TIME_WAIT)

        for (_,_,z), cubie in self.cubeDict.items():
          if round(z) == 2:
              cubie.rotateFaces("z",angle)