import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from Cube import Cube
from math import pi
import Solver

CLOCKWISE_TURN_ANGLE = pi/2
ANTICLOCKWISE_TURN_ANGLE = -pi/2
FPS = 60  # Target frames per second


def print_keybind_menu() -> None:
    """Prints a formatted menu of keybinds in the console"""
    print("\n" + "="*50)
    print("{:^50}".format("RUBIK'S CUBE SIMULATOR - KEYBINDS"))
    print("="*50)

    # Movement controls
    print("\n{:^50}".format("CUBE ROTATION"))
    print("-"*50)
    print("{:<30} : {}".format("Arrow Up/Down/Left/Right", "Rotate view"))

    # Face rotations
    print("\n{:^50}".format("FACE ROTATIONS"))
    print("-"*50)
    print("{:<30} : {}".format("U / Shift+U",
          "Up face clockwise / counterclockwise"))
    print("{:<30} : {}".format("D / Shift+D",
          "Down face clockwise / counterclockwise"))
    print("{:<30} : {}".format("F / Shift+F",
          "Front face clockwise / counterclockwise"))
    print("{:<30} : {}".format("B / Shift+B",
          "Back face clockwise / counterclockwise"))
    print("{:<30} : {}".format("R / Shift+R",
          "Right face clockwise / counterclockwise"))
    print("{:<30} : {}".format("L / Shift+L",
          "Left face clockwise / counterclockwise"))

    # Other controls
    print("\n{:^50}".format("OTHER CONTROLS"))
    print("-"*50)
    print("{:<30} : {}".format(
        "Space", "Print move history (Resets after solving)"))
    print("{:<30} : {}".format("`", "Auto-solve cube"))


def main():
    # Print keybind menu in console at startup
    print_keybind_menu()

    # Setting up the pygame and OpenGL environment
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0, -5, -30)

    # Creating a 3x3x3 cube
    EntireCube = Cube(3)
    EntireCube.createEntireCube()

    # Booleans for each type of rotation that may occur
    rotateUpKey, rotateDownKey, rotateLeftKey, rotateRightKey = False, False, False, False
    rotationalSensitivity = 2
    input = ""
    isSolving = False

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if isSolving:
                continue

            # Determining which key is pressed and which action needs to be taken
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    rotateUpKey = True
                if event.key == K_DOWN:
                    rotateDownKey = True
                if event.key == K_LEFT:
                    rotateLeftKey = True
                if event.key == K_RIGHT:
                    rotateRightKey = True

            if event.type == KEYUP:
                if event.key == K_UP:
                    rotateUpKey = False
                if event.key == K_DOWN:
                    rotateDownKey = False
                if event.key == K_LEFT:
                    rotateLeftKey = False
                if event.key == K_RIGHT:
                    rotateRightKey = False

                # Actual angles are wrong in the real world for some turns maybe the axes are point in wrong directions
                if event.key == K_u:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.upMove(CLOCKWISE_TURN_ANGLE)
                        input += "U' "
                    else:
                        EntireCube.upMove(ANTICLOCKWISE_TURN_ANGLE)
                        input += "U "

                if event.key == K_d:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.downMove(ANTICLOCKWISE_TURN_ANGLE)
                        input += "D' "
                    else:
                        EntireCube.downMove(CLOCKWISE_TURN_ANGLE)
                        input += "D "

                if event.key == K_f:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.frontMove(CLOCKWISE_TURN_ANGLE)
                        input += "F' "
                    else:
                        EntireCube.frontMove(ANTICLOCKWISE_TURN_ANGLE)
                        input += "F "

                if event.key == K_b:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.backMove(ANTICLOCKWISE_TURN_ANGLE)
                        input += "B' "
                    else:
                        EntireCube.backMove(CLOCKWISE_TURN_ANGLE)
                        input += "B "

                if event.key == K_r:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.rightMove(CLOCKWISE_TURN_ANGLE)
                        input += "R' "
                    else:
                        EntireCube.rightMove(ANTICLOCKWISE_TURN_ANGLE)
                        input += "R "

                if event.key == K_l:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.leftMove(ANTICLOCKWISE_TURN_ANGLE)
                        input += "L' "
                    else:
                        EntireCube.leftMove(CLOCKWISE_TURN_ANGLE)
                        input += "L "

                if event.key == K_SPACE:
                    print(input)

                if event.key == K_BACKQUOTE:
                    isSolving = True
                    solution = Solver.solve(EntireCube)
                    print("Solution:", solution)
                    print("Executing solution...")
                    Solver.executeSolve(EntireCube, solution)
                    print("Done executing")
                    input = ""
                    isSolving = False

        # Logic for rotating the entire cube for the user to get a different view, not the faces
        if rotateUpKey:
            glRotatef(rotationalSensitivity, -rotationalSensitivity, 0, 0)
        if rotateDownKey:
            glRotatef(rotationalSensitivity, rotationalSensitivity, 0, 0)
        if rotateLeftKey:
            glRotatef(rotationalSensitivity, 0, -rotationalSensitivity, 0)
        if rotateRightKey:
            glRotatef(rotationalSensitivity, 0, rotationalSensitivity, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Rendering cube on every frame to show changes
        EntireCube.render()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
