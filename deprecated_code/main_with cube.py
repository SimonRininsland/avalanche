#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# used: https://github.com/greenmoss/PyWavefront
import pywavefront

width, height = (1280, 720)

# gloabl var for later cam rotation on click
camRotation = 0

# lightfv for our light
lightfv = ctypes.c_float * 4

#my dummy cube
cube = ''

# ASCII OCTAL for ESCAPE
ESCAPE = '\033'

def display():
    # gets called if glut thinks the window has to be redrawed (by click, resize...)
    # init displaying
    glLoadIdentity()

    # enable depth  Test
    glEnable(GL_DEPTH_TEST)

    # setup light - 2 lights for testing
    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightfv(0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightfv(0.7, 0.7, 0.7, 1.0))

    glEnable(GL_LIGHT0)

    # enable Lighting and Shadows
    glEnable(GL_LIGHTING)

    # GLOBAL light settings
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.1, 0.1, 0.1, 1))

    # set ShadeModel
    glShadeModel(GL_SMOOTH)

    # set MatrixMode for render
    glMatrixMode(GL_MODELVIEW)

def drawLoop(deltaT):
    global pos, camRotation, cube
    # display all the stuff
    # which colors will be cleared (all here- without alpha) - every frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    #rotate around camRotation
    glRotatef(camRotation, 1, 1, 0)

    # print my cube
    cube.draw()

    # swap the Buffers on Projection Matrix
    glutSwapBuffers()

    # increment camRotation
    camRotation += 1

    # LoopCallback Recursive
    glutTimerFunc(1000/60, drawLoop, 0)


def keyFunc(key, x, y):
    if key == ESCAPE:
        sys.exit()


def mouseFunc(key, mode, x, y):
    global camRotation
    if mode == 0 and key == 0:
        print("click")
        camRotation = 0
    pass

def init():
    global cube
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

    # set up a perspective projection matrix @todo it does not do anything right now
    # void gluPerspective(	GLdouble fovy,	GLdouble aspect, GLdouble zNear, GLdouble zFar);
    gluPerspective(40.0, float(width) / height, 1, 100.0)

    # define a viewing transformation - Camera on Z axis 10 away @todo it does not do anything
    # void gluLookAt(GLdouble eyeX, GLdouble eyeY, GLdouble eyeZ, GLdouble centerX, GLdouble centerY, GLdouble centerZ, GLdouble upX, GLdouble upY, GLdouble upZ);
    gluLookAt(0, 0, 10,
              0, 0, 0,
              0, 1, 0)

    # set MatrixMode for render
    glMatrixMode(GL_MODELVIEW)

    # to have a callback function we need to add a display function
    glutDisplayFunc(display)

    #load my cube
    cube = pywavefront.Wavefront('resources/cube.obj')

    # callback for keystroke
    glutKeyboardFunc(keyFunc)

    # callback for mousepress
    glutMouseFunc(mouseFunc)

    # Timer function for the 60 fps draw callback
    glutTimerFunc(1000/60, drawLoop, 0)

    # glutMainLoop enters the GLUT event processing loop. This routine should be called at most once in a GLUT program.
    # Once called, this routine will never return. It will call as necessary any callbacks that have been registered.
    glutMainLoop()

if __name__ == '__main__':
    init()