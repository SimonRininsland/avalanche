#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

width, height = (1280, 720)

pos = []

# ASCII OCTAL for ESCAPE
ESCAPE = '\033'


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

def drawLoop(deltaT):
    # display all the stuff
    # which colors will be cleared (all here- without alpha) - every frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # ttransle on x axis
    glTranslate(0, -.025, 0)

    # draw everything red
    glColor3f(1, 0, 0)

    # draw solid Sphere
    # void glutSolidSphere(GLdouble radius, GLint slices, GLint stacks);

    global pos

    for index, i in enumerate(pos):
        drawLine(i[0], i[1], i[2])
        if i[1] < -1:
            pos[index] = (i[0], 1, i[2])
        else:
            pos[index] = (i[0], i[1]-0.01, i[2])


    # swap the Buffers on Projection Matrix
    glutSwapBuffers()

    # LoopCallback Recursive
    glutTimerFunc(1000/60, drawLoop, 0)


def keyFunc(key, x, y):
    if key == ESCAPE:
        sys.exit()


def mouseFunc(key, mode, x, y):
    if mode == 0 and key == 0:
        randPos(1)
    if mode == 0 and key == 2:
        randPos(10)
    if mode == 0 and key == 1:
        randPos(100)
    print len(pos)
    pass


def drawLine(x, y, z):
    glLineWidth(10);
    glColor3f(1.0, 0.0, 0.0);
    glBegin(GL_LINES);
    # dont use fixed function functionality!!!
    # use shader based OpenGL!!!
    glVertex3f(x, y, z);
    glVertex3f(x + .002, y + .002, z + .002);
    glEnd();

def randPos(i):
    global pos
    for j in xrange(i):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        z = random.uniform(-1,1)
        pos.append((x,y,z))


def init():
    # Init OpenGL Utility Toolkit
    glutInit()
    # Init the Display Mode
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
    # and window size
    glutInitWindowSize(width, height)
    # and the Window Title (the b in front, is to give the name in bitwise - opengl needs that)
    glutCreateWindow(b"HS-RM 3D-Animation Avalanche")

    # enable if front and backface is rendered
    glEnable(GL_CULL_FACE)

    # enable depth Test
    glEnable(GL_DEPTH_TEST)

    # enable Lighting and Shadows @todo we need to add a ligth afterwards
    # glEnable(GL_LIGHTING)

    # enabling colored material
    glEnable(GL_COLOR_MATERIAL)

    # clear the screen
    glClearColor(1, 1, 1, 0)

    # to have a callback function we need to add a display function
    glutDisplayFunc(display)

    # callback for keystroke
    glutKeyboardFunc(keyFunc)

    # callback for mousepress
    glutMouseFunc(mouseFunc)

    # Timer function for the 60 fps draw callback
    glutTimerFunc(1000/60, drawLoop, 0)

    # create Projection Matrix
    glMatrixMode(GL_PROJECTION)

    # set up a perspective projection matrix
    # void gluPerspective(	GLdouble fovy,	GLdouble aspect, GLdouble zNear, GLdouble zFar);
    gluPerspective(40., (width / height), 1., 40.)

    # define a viewing transformation - Camera on Z axis 10 away
    # void gluLookAt(GLdouble eyeX, GLdouble eyeY, GLdouble eyeZ, GLdouble centerX, GLdouble centerY, GLdouble centerZ, GLdouble upX, GLdouble upY, GLdouble upZ);
    gluLookAt(0, 0, 10,
              0, 0, 0,
              0, 1, 0)

    # glutMainLoop enters the GLUT event processing loop. This routine should be called at most once in a GLUT program.
    # Once called, this routine will never return. It will call as necessary any callbacks that have been registered.
    glutMainLoop()

if __name__ == '__main__':
    randPos(123)
    init()