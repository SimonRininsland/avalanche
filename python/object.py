# Class for an Object
# One Object is a collideable Obstacle

from OpenGL.GL import *
# used: https://github.com/greenmoss/PyWavefront
import pywavefront
import particle


class object():
    def __init__(self, position, obj):
        # every Object has an own position
        self.position = position

        self.mass = 1

        # The obj
        self.obj = pywavefront.Wavefront(obj)

    def increment(self, dt):
        pass

    def draw(self, deltaT):
        self.increment(deltaT)
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glScalef(self.mass,self.mass,self.mass)
        self.obj.draw()
        ##### WIRED FRAME #####
        # tmp = self.getBound()
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
        # glBegin(GL_POLYGON)
        # glVertex3f(tmp[0], tmp[2], tmp[4])
        # glVertex3f(tmp[1], tmp[2], tmp[4])
        # glVertex3f(tmp[1], tmp[3], tmp[4])
        # glVertex3f(tmp[0], tmp[3], tmp[4])
        #
        # glVertex3f(tmp[0], tmp[2], tmp[5])
        # glVertex3f(tmp[1], tmp[2], tmp[5])
        # glVertex3f(tmp[1], tmp[3], tmp[5])
        # glVertex3f(tmp[0], tmp[3], tmp[5])
        #
        # glVertex3f(tmp[0], tmp[2], tmp[4])
        # glVertex3f(tmp[0], tmp[3], tmp[4])
        # glVertex3f(tmp[0], tmp[3], tmp[5])
        # glVertex3f(tmp[0], tmp[2], tmp[5])
        #
        # glVertex3f(tmp[1], tmp[2], tmp[4])
        # glVertex3f(tmp[1], tmp[3], tmp[4])
        # glVertex3f(tmp[1], tmp[3], tmp[5])
        # glVertex3f(tmp[1], tmp[2], tmp[5])
        #
        # glEnd()
        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glTranslatef(-self.position[0], -self.position[1], -self.position[2])


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

    def collisionDetection(self, obj):
        if isinstance(obj, particle.particle):
            obj.collisionDetection(self)


    def collisionResponse(self):
        pass