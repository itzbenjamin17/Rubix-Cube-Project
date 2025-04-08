import twophase.solver as sv
from Cube import Cube
from math import pi
import pygame

TURN = pi / 2
MOVE_DELAY = 2  # Frames per second for the solution animation


def getRepresentation(cube: Cube) -> str:
    '''Converting the cube's current state into a string representation for solving.'''
    face_colours = {
        (1, 1, 1): 'U',    # White
        (1, 1, 0): 'D',    # Yellow
        (1, 0.65, 0): 'F',  # Orange
        (1, 0, 0): 'B',    # Red
        (0, 0, 1): 'L',    # Blue
        (0, 1, 0): 'R'     # Green
    }
    representation = ""

    # Up face
    y = 2
    for z in range(3):
        for x in range(3):
            representation += face_colours[cube.cubeDict[(
                x, y, z)].face_mapping[4].colour]

    # Right face
    x = 2
    for y in range(2, -1, -1):
        for z in range(2, -1, -1):
            representation += face_colours[cube.cubeDict[(
                x, y, z)].face_mapping[3].colour]

    # Front face
    z = 2
    for y in range(2, -1, -1):
        for x in range(3):
            representation += face_colours[cube.cubeDict[(
                x, y, z)].face_mapping[2].colour]

    # Down face
    y = 0
    for z in range(2, -1, -1):
        for x in range(3):
            representation += face_colours[cube.cubeDict[(
                x, y, z)].face_mapping[5].colour]

    # Left face
    x = 0
    for y in range(2, -1, -1):
        for z in range(3):
            representation += face_colours[cube.cubeDict[(
                x, y, z)].face_mapping[1].colour]

    # Back face
    z = 0
    for y in range(2, -1, -1):
        for x in range(2, -1, -1):
            representation += face_colours[cube.cubeDict[(
                x, y, z)].face_mapping[0].colour]

    return representation


def solve(cube: Cube) -> str:
    '''Using the two-phase algorithm to solve the cube.'''
    representation = getRepresentation(cube)
    solution = sv.solve(representation, 20, 5)
    return solution


def executeSolve(cube: Cube, solution: str) -> None:
    '''Executing the solution on the cube.'''
    # Splitting the solution into individual moves
    moves = solution.split()
    clock = pygame.time.Clock()

    # Executing each move on the cube
    for move in moves:
        turns = int(move[1])
        move_type = move[0]

        for _ in range(turns):
            if move_type == 'U':
                cube.upMove(-TURN)
            elif move_type == 'D':
                cube.downMove(TURN)
            elif move_type == 'L':
                cube.leftMove(TURN)
            elif move_type == 'R':
                cube.rightMove(-TURN)
            elif move_type == 'F':
                cube.frontMove(-TURN)
            elif move_type == 'B':
                cube.backMove(TURN)

            # Handle events to prevent freezing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Control animation speed
            clock.tick(MOVE_DELAY)
