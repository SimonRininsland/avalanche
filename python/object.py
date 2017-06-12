# Class for an Object
# One Object is a collideable Obstacle

from OpenGL.GL import *
# used: https://github.com/greenmoss/PyWavefront
import pywavefront

class object():
    def __init__(self, position, obj):
        # every Object has an own position
        self.position = position

        # The obj
        self.obj = pywavefront.Wavefront(obj)

    def draw(self):
        glTranslatef(self.position[0], self.position[1], self.position[2])
        # An Object needs only a function to get drawn
        #print(self.obj.__getattribute__('width'))
        return(self.obj.draw())

