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

    def draw(self, detaT):
        glTranslatef(self.position[0], self.position[1], self.position[2])
        # An Object needs only a function to get drawn
        # print(self.obj.__getattribute__('width'))
        return (self.obj.draw())

    def getBound(self):
        xs = [v[0] for v in self.obj.vertx]
        ys = [v[1] for v in self.obj.vertx]
        zs = [v[2] for v in self.obj.vertx]
        return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

    # BoundingBox in Relation to the Position
    def getCollisionBox(self):
        bound = self.getBound()
        # min(xs), max(xs), min(ys), max(ys), min(zs), max(zs) + position on axis
        # X - Axis min / max
        # Y - Axis min / max
        # Z - Axis min / max
        return (bound[0] + self.position[0], bound[1] + self.position[0],
                bound[2] + self.position[1], bound[3] + self.position[1],
                bound[4] + self.position[2], bound[5] + self.position[2])

    def collision(self):
        print("WAAAAAAAAAAAAAAAH COLLISION in Object!!!")
