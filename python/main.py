#!/usr/bin/env python
# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def display():
    # display all the stuff
    # which colors will be cleared (all here- without alpha) - every frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # draw solid Sphere
    glutSolidSphere(2,20,20)

    # swap the Buffers on Projection Matrix
    glutSwapBuffers()
    return

def init():
    # Init OpenGL Utility Toolkit
    glutInit()
    # Init the Display Mode
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
    # and window size
    glutInitWindowSize(1280, 720)
    # and the Window Title (the b in front, is to give the name in bitwise - opengl needs that)
    glutCreateWindow(b"HS-RM 3D-Animation Avalanche")

    # enable if front and backface is rendered
    glEnable(GL_CULL_FACE)

    # enable depth Test
    glEnable(GL_DEPTH_TEST)

    # enable Lighting and Shadows
    glEnable(GL_LIGHTING)

    # clear the screen
    glClearColor(1, 1, 1, 0)

    # to have a callback function we need to add a display function
    glutDisplayFunc(display)

    # create Projection Matrix
    glMatrixMode(GL_PROJECTION)

    # set up a perspective projection matrix
    # void gluPerspective(	GLdouble fovy,	GLdouble aspect, GLdouble zNear, GLdouble zFar);
    gluPerspective(40., 1., 1., 40.)

    # define a viewing transformation - Camera on Z axis 10 away
    # void gluLookAt(GLdouble eyeX, GLdouble eyeY, GLdouble eyeZ, GLdouble centerX, GLdouble centerY, GLdouble centerZ, GLdouble upX, GLdouble upY, GLdouble upZ);
    gluLookAt(0, 0, 10,
              0, 0, 0,
              0, 1, 0)

    # glutMainLoop enters the GLUT event processing loop. This routine should be called at most once in a GLUT program.
    # Once called, this routine will never return. It will call as necessary any callbacks that have been registered.
    glutMainLoop()

if __name__ == '__main__':
    init()
    print ("start of Code")
