import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from Cube import Cube
from math import pi

CLOCKWISE_TURN_ANGLE = pi/2
ANTICLOCKWISE_TURN_ANGLE = -pi/2

def main():
    #Setting up the pygame and OpenGL environment
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST) 
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0,-5, -30)

    #creating a 3x3x3 cube
    EntireCube = Cube(3) 
    EntireCube.createEntireCube()

    #Booleans for each type of rotation that may occur
    rotateUpKey, rotateDownKey, rotateLeftKey, rotateRightKey = False, False, False, False
    rotationalSensitivity = 2
    input = ""
    inputChanged = False
    while True:
        if inputChanged:
            print(input)
            inputChanged = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #input.rstrip()
                #print(input)
                quit()

            #Determining which key is pressed and which action needs to be taken
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
                    inputChanged = True

                if event.key == K_d:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.downMove(ANTICLOCKWISE_TURN_ANGLE)
                        input += "D' "
                    else:
                        EntireCube.downMove(CLOCKWISE_TURN_ANGLE)   
                        input += "D "
                    inputChanged = True
                if event.key == K_f:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.frontMove(CLOCKWISE_TURN_ANGLE)
                        input += "F' "
                    else:
                        EntireCube.frontMove(ANTICLOCKWISE_TURN_ANGLE)
                        input += "F "
                    inputChanged = True
                if event.key == K_b:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.backMove(ANTICLOCKWISE_TURN_ANGLE)
                        input += "B' "
                    else:
                        EntireCube.backMove(CLOCKWISE_TURN_ANGLE) 
                        input += "B "
                    inputChanged = True
                if event.key == K_r:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.rightMove(CLOCKWISE_TURN_ANGLE)
                        input += "R' "
                    else:
                        EntireCube.rightMove(ANTICLOCKWISE_TURN_ANGLE)
                        input += "R "
                    inputChanged = True
                if event.key == K_l:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.leftMove(ANTICLOCKWISE_TURN_ANGLE)
                        input += "L' "
                    else:
                        EntireCube.leftMove(CLOCKWISE_TURN_ANGLE)                    
                        input += "L "
                    inputChanged = True
                    '''
                if event.key == K_m:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.middleMove(ANTICLOCKWISE_TURN_ANGLE)
                        input += "M' "
                    else:
                        EntireCube.middleMove(CLOCKWISE_TURN_ANGLE)
                        input += "M "
                    inputChanged = True
                if event.key == K_s:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.sliceSMove(CLOCKWISE_TURN_ANGLE)
                        input += "S' "
                    else:
                        EntireCube.sliceSMove(ANTICLOCKWISE_TURN_ANGLE)                
                        input += "S "
                    inputChanged = True
                if event.key == K_e:
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        EntireCube.sliceEMove(ANTICLOCKWISE_TURN_ANGLE)
                        input += "E' "
                    else:
                        EntireCube.sliceEMove(CLOCKWISE_TURN_ANGLE)
                        input += "E "
                    inputChanged = True
                    '''
        if rotateUpKey:
            glRotatef(rotationalSensitivity,-rotationalSensitivity,0,0)
        if rotateDownKey:
            glRotatef(rotationalSensitivity,rotationalSensitivity,0,0)
        if rotateLeftKey:
            glRotatef(rotationalSensitivity,0,-rotationalSensitivity,0)
        if rotateRightKey:
            glRotatef(rotationalSensitivity,0,rotationalSensitivity,0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #Rendering cube on every frame to show changes
        EntireCube.render()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    main()
