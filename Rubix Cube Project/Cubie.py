from OpenGL.GL import *
from OpenGL.GLU import *
from Face import Face
import numpy as np

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

colors = (
    (1, 0, 0),  # Red
    (0, 0, 1),  # Blue
    (1, 0.65, 0),  # Orange
    (0, 1, 0),  # Green
    (1, 1, 1),  # White
    (1, 1, 0),  # Yellow
)

faceNames = {"B": 0, "L": 1, "F": 2, "R": 3, "U": 4, "D": 5}

SCALE_FACTOR = 2.1


class Cubie:
    def __init__(self, x: int, y: int, z: int, colours: dict):
        self.x = x
        self.y = y
        self.z = z
        self.vertices = self.setVertices()
        self.faces = self.assignFaces(colours)
        self.face_mapping = self.faces

    def setVertices(self):
        '''Setting predefined vertices based on cubie's position'''
        newVertices = []
        for vert in vertices:
            newX = vert[0] + self.x * SCALE_FACTOR
            newY = vert[1] + self.y * SCALE_FACTOR
            newZ = vert[2] + self.z * SCALE_FACTOR
            newVertices.append((newX, newY, newZ))
        return newVertices

    def rotateVertices(self, rotationMatrix: np.array):
        '''Rotatating the vertices of the cubie using the given rotation matrix'''
        newVertices = []
        for vert in self.vertices:
            rotatedVertex = np.dot(rotationMatrix, vert)
            newVertices.append(rotatedVertex)
        self.vertices = newVertices

    def assignFaces(self, colours: dict):
        '''Assigning the correct colours to each face of the cubie'''
        faces = {}
        faceOrder = ["B", "L", "F", "R", "U", "D"]
        for i, face in enumerate(faceOrder):
            if face in colours:
                faces[i] = Face(colours[face], faceOrder[i])
            else:
                # Default colour if not specified
                faces[i] = Face((0, 0, 0), faceOrder[i])
        return faces

    def rotateFaces(self, axis: str, angle: float):
        '''Rotating the faces of the cubie based on the given axis and angle and updating the face mapping for solving'''
        # Some axes dont work how i would imagine so face mappings have to be swapped
        newFaces = {}

        if axis == "x":
            if angle > 0:
                faceMapping = {"U": "F", "F": "D", "D": "B", "B": "U"}
                newFaces = self.moveFaces(faceMapping)
            else:
                faceMapping = {"U": "B", "F": "U", "D": "F", "B": "D"}
                newFaces = self.moveFaces(faceMapping)

        elif axis == "y":
            if angle > 0:
                faceMapping = {"F": "R", "R": "B", "B": "L", "L": "F"}
                newFaces = self.moveFaces(faceMapping)
            else:
                faceMapping = {"R": "F", "F": "L", "L": "B", "B": "R"}

                newFaces = self.moveFaces(faceMapping)

        else:
            if angle > 0:
                faceMapping = {"U": "L", "L": "D", "D": "R", "R": "U"}
                newFaces = self.moveFaces(faceMapping)
            else:
                faceMapping = {"U": "R", "R": "D", "D": "L", "L": "U"}
                newFaces = self.moveFaces(faceMapping)

        self.face_mapping = newFaces

    def moveFaces(self, faceMapping: dict):
        # Convoluted way to use the face mapping dictionary to place the right face at each index
        newFaces = {}
        for i, face in self.face_mapping.items():
            if face.name in faceMapping:
                newFaceName = faceMapping[face.name]
                newFaces[faceNames[newFaceName]] = Face(
                    face.colour, newFaceName)
            else:
                newFaces[i] = self.face_mapping[i]
        return newFaces

    def createCubie(self):
        # Open gl syntax to create a single cube
        glBegin(GL_QUADS)
        for i, surface in enumerate(surfaces):
            glColor3fv(self.faces[i].colour)
            for vertex in surface:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def updateCoordinates(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
