#!/usr/bin/env python
# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *


def display():
    # display all the stuff
    print("display")

def init():
    # Init OpenGL Utility Toolkit
    glutInit()
    # Init the Display Mode
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
    # and window size
    glutInitWindowSize(1280, 720)
    # and the Window Title (the b in front, is to give the name in bitwise - opengl needs that)
    glutCreateWindow(b"HS-RM 3D-Animation Avalanche")

    # to have a callback function we need to add a display function
    glutDisplayFunc(display)

    # If activated the depth will be compared and the depthbuffer refreshed (don't calc things which are not visible)
    #glEnable(GL_DEPTH_TEST)
    # which colors will be cleared (all here- without alpha)
    glClearColor(1, 1, 1, 0)

    # glutMainLoop enters the GLUT event processing loop. This routine should be called at most once in a GLUT program.
    # Once called, this routine will never return. It will call as necessary any callbacks that have been registered.
    glutMainLoop()

if __name__ == '__main__':
    init()
    print ("start of Code")
