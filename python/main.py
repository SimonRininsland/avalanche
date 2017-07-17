#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import uniform
import multiprocessing
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import particle, object, world

width, height = (1280, 720)

#my originFlake Number
emitterCount = 100

# my EmitterPer Flake Numer
flakesPerEmitter = 1

#enable DebugMode
debug = False

# for the light
lightfv = ctypes.c_float * 4

# ASCII OCTAL for ESCAPE
ESCAPE = '\033'
SPACEBAR = '\040'

# camera variables
ox = 0
oy = 0
buttonState = 0
camera_trans = [0, -2, -25]
camera_rot = [0, 0, 0]
camera_trans_lag = [0, -2, -25]
camera_rot_lag = [0, 0, 0]
inertia = 0.1

# my object array
drawObjectsArray = []

# camera movement
camEyeX, camEyeY, camEyeZ = (0., 0., 0.)
camCenterX, camCenterY, camCenterZ = (1., 1., 1.)
camUpX, camUpY, camUpZ = (0., 0., 0.)

def display(deltaT = 1000 / 60):
    # gets called if glut thinks the window has to be redrawed (by click, resize...)
    # init displaying
    global world, drawObjectsArray, particle
    # display all the stuff
    # which colors will be cleared (all here- without alpha) - every frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()


    for c in xrange(3):
        camera_trans_lag[c] += (camera_trans[c] - camera_trans_lag[c]) * inertia;
        camera_rot_lag[c] += (camera_rot[c] - camera_rot_lag[c]) * inertia;
    glTranslatef(camera_trans_lag[0], camera_trans_lag[1], camera_trans_lag[2])
    glRotatef(camera_rot_lag[0], 1.0, 0.0, 0.0)
    glRotatef(camera_rot_lag[1], 0.0, 1.0, 0.0)

    # draw all my objects
    for index in xrange(len(drawObjectsArray)):

        # draw my object
        drawObjectsArray[index].draw(deltaT, world)

        # Debug Mode Option
        if debug:
            debugDraw()

    # swap the Buffers on Projection Matrix
    glutSwapBuffers()

    # LoopCallback Recursive
    glutTimerFunc(1000 / 60, display, 1000 / 60)

def debugDraw():
    # debug setup
    size = 10.0
    glPointSize(size)

    if True:
        # My Position in Green
        glColor3f(0., 1., 0.)
        for index in xrange(len(drawObjectsArray)):
            glBegin(GL_POINTS)
            glVertex3f(drawObjectsArray[index].position[0], drawObjectsArray[index].position[1],
                       drawObjectsArray[index].position[2])
            glEnd()

    if False:
        # My Voxel in Red
        glColor3f(1., 0., 0.)
        for index in xrange(len(drawObjectsArray)):
            if isinstance(drawObjectsArray[index], particle.particle):
                glBegin(GL_POINTS)
                # we have to recalculate to get it in view Coordinates
                glVertex3f(drawObjectsArray[index].voxel[0][0] - world.worldSize,
                           drawObjectsArray[index].voxel[1][0],
                           drawObjectsArray[index].voxel[2][0] - world.worldSize)
                glEnd()

    if True:
        # My CollisionFace in Yellow
        glColor3f(1., 1., 0.)
        for index in xrange(len(drawObjectsArray)):
            if isinstance(drawObjectsArray[index], particle.particle):
                glBegin(GL_POINTS)

                # we have to recalculate to get it in view Coordinates
                glVertex3f(drawObjectsArray[index].myCollisionFace[0][0] - world.worldSize,
                           drawObjectsArray[index].myCollisionFace[0][1],
                           drawObjectsArray[index].myCollisionFace[0][2] - world.worldSize)

                glVertex3f(drawObjectsArray[index].myCollisionFace[1][0] - world.worldSize,
                           drawObjectsArray[index].myCollisionFace[1][1],
                           drawObjectsArray[index].myCollisionFace[1][2] - world.worldSize)

                glVertex3f(drawObjectsArray[index].myCollisionFace[2][0] - world.worldSize,
                           drawObjectsArray[index].myCollisionFace[2][1],
                           drawObjectsArray[index].myCollisionFace[2][2] - world.worldSize)
                glEnd()

    if False:
        # Objects in World array in Blue
        glColor3f(0., 0., 1.)
        for indexX, worldGridX in enumerate(world.grid):
            for indexY, worldGridY in enumerate(worldGridX):
                for indexZ, worldGridZ in enumerate(worldGridY):
                    if worldGridZ != -1:
                        glBegin(GL_POINTS)
                        # we have to recalculate to get it in view Coordinates
                        glVertex3f(indexX - world.worldSize,
                                   indexY,
                                   indexZ - world.worldSize)
                        glEnd()

    if False:
        # Objects in World array in Green
        glColor3f(0., 1., 0.)

        glBegin(GL_LINES)
        index = -64
        while index <= 64:
            glVertex3f(index, 0, -64)
            glVertex3f(index, 0, 64)

            glVertex3f(-64, 0, index)
            glVertex3f(64, 0, index)
            index += 1

        glEnd()

        glBegin(GL_LINES)
        indexX = -64
        indexY = -64
        indexZ = -64
        while indexX <= 64:
            while indexY <= 64:
                while indexZ <= 64:
                    glVertex3f(indexY, -64, indexX)
                    glVertex3f(indexY, 64, indexX)

                    glVertex3f(-64, indexX, indexY)
                    glVertex3f(64, indexX, indexY)
                    indexZ+= 4
                indexZ = -64
                indexY += 4
            indexZ = -64
            indexY = -64
            indexX += 4

        glEnd()

        glBegin(GL_LINES)
        index = -64
        while index <= 64:
            glVertex3f(0, index, -64)
            glVertex3f(0, index, 64)

            glVertex3f(0, -64, index)
            glVertex3f(0, 64, index)
            index += 1

        glEnd()


    glColor3f(1., 1., 1.)

def keyFunc(key, x, y):
    global camEyeX, camEyeY, camEyeZ
    global camCenterX, camCenterY, camCenterZ
    global camUpX, camUpY, camUpZ

    CamSpeed = 0.1

    if key == ESCAPE:
        sys.exit()
    elif key == "w":

        pass
    elif key == "a":
        pass
    elif key == "s":
        pass
    elif key == "d":
        pass
    elif key == SPACEBAR:
        camCenterY += CamSpeed
    else:
        print key

    print camCenterY

def mouse(button, state, x, y):
    global buttonState
    global ox, oy
    if (state == GLUT_DOWN):
        buttonState |= 1 << button
    elif (state == GLUT_UP):
        buttonState = 0

    mods = glutGetModifiers()
    if (mods & GLUT_ACTIVE_SHIFT):
        buttonState = 2
    elif (mods & GLUT_ACTIVE_CTRL):
        buttonState = 3

    ox = x
    oy = y

    glutPostRedisplay()

def motion(x, y):
    global buttonState
    global ox, oy
    global camera_trans
    global camera_rot
    dx = x - ox
    dy = y - oy

    if buttonState == 3:
        # left+middle = zoom
        camera_trans[2] += (dy / 100.0) * 0.5 * abs(camera_trans[2])
    elif buttonState & 2:
        # middle = translate
        camera_trans[0] += dx / 100.0
        camera_trans[1] -= dy / 100.0
    elif buttonState & 1:
        # left = rotate
        camera_rot[0] += dy / 5.0
        camera_rot[1] += dx / 5.0

    ox = x
    oy = y
    glutPostRedisplay()

def init():
    global world, drawObjectsArray
    # Init OpenGL Utility Toolkit
    glutInit()
    # Init the Display Mode
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH )
    # and window size
    glutInitWindowSize(width, height)
    # and the Window Title (the b in front, is to give the name in bitwise - opengl needs that)
    glutCreateWindow(b"HS-RM 3D-Animation Avalanche")

    # clear the screen
    glClearColor(0, 0, 0, 0)

    # MatrixMode for setup
    glMatrixMode(GL_PROJECTION)

    # set up a perspective projection matrix
    # void gluPerspective(	GLdouble fovy,	GLdouble aspect, GLdouble zNear, GLdouble zFar);
    gluPerspective(40.0, float(width) / height, 1, 300.0)

    # define a viewing transformation - Camera on Z axis 10 away
    # void gluLookAt(GLdouble eyeX, GLdouble eyeY, GLdouble eyeZ, GLdouble centerX, GLdouble centerY, GLdouble centerZ, GLdouble upX, GLdouble upY, GLdouble upZ);

    # view more far away
    '''gluLookAt(100, 100, 100,
              0, 0, 0,
              0, 1, 0)
    '''

    # view far away
    gluLookAt(0, 35, -60,
              0, 20, 0,
              0, 1, 0)

    # view near to test
    # gluLookAt(100, 100, 0,
    #           0, 0, 0,
    #           0, 1, 0)
    '''
    gluLookAt(20, 25, 10,
              0, 0, 0,
              0, 1, 0)
    '''
    # set MatrixMode for render
    glMatrixMode(GL_MODELVIEW)

    # MatrixMode for setup
    glMatrixMode(GL_PROJECTION)

    # set ShadeModel
    glShadeModel(GL_SMOOTH)

    # enable if front and backface is rendered
    glEnable(GL_CULL_FACE)

    # enable depth Test
    glEnable(GL_DEPTH_TEST)

    # setup light - 2 lights for testing
    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightfv(0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightfv(0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)

    # enable Lighting and Shadows
    glEnable(GL_LIGHTING)

    # enabling colored material
    glEnable(GL_COLOR_MATERIAL)

    # set MatrixMode for render
    glMatrixMode(GL_MODELVIEW)

    # our world model
    world = world.world()

    # load my plane
    drawObjectsArray.append(object.object([0,0,0], 'resources/terrain_smooth_flat.obj', world))

    # setup one particle position, velocity, mass, obj

    # Spawn Flakes
    # for i in xrange(flakeCount):
    #     drawObjectsArray.append(particle.particle([uniform(-5.0, 5.0), uniform(24.0, 30.0),uniform(-5.0, 5.0)],
    #     [0.0, 0.0, 0.0], uniform(.2, 1.0), 'resources/flake.obj', i, world, drawObjectsArray))

    # collision Spawn Flakes
    for i in xrange(emitterCount):
        drawObjectsArray.append(particle.particle([uniform(-10.0, 10.0), uniform(28.0, 45.0), uniform(-10.0, 10.0)],
        [0.0, 0.0, 0.0], uniform(.2, 1.0), 'resources/flake.obj', i, world, drawObjectsArray, flakesPerEmitter))


    # near spawn
    '''for i in xrange(flakeCount):
        drawObjectsArray.append(particle.particle([uniform(-1.0, 1.0), uniform(2.0, 3.0), uniform(-1.0, 1.0)],
                              [0.0, 0.0, 0.0], uniform(.2, 1.0), 'resources/flake.obj', i, world, drawObjectsArray))'''


    # callback for keystroke
    glutKeyboardFunc(keyFunc)

    # callback for mousepress
    glutMouseFunc(mouse)

    # Motion Func
    glutMotionFunc(motion)

    glutDisplayFunc(display)
    # Timer function for the 60 fps draw callback
    glutTimerFunc(1000/60, display, 1000/60)

    # glutMainLoop enters the GLUT event processing loop. This routine should be called at most once in a GLUT program.
    # Once called, this routine will never return. It will call as necessary any callbacks that have been registered.
    glutMainLoop()

if __name__ == '__main__':
    init()
