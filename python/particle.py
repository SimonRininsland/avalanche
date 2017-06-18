# Class for a single Particle
# a Particle always has a position, velocity and a mass

from OpenGL.GL import *
# used: https://github.com/greenmoss/PyWavefront
import pywavefront, time

# The Gravitation
gravitation = [0, -9.81, 0]

class particle(object):
    def __init__(self, position, velocity, mass, obj):
        # every Particle has an own positionget_vert
        self.position = position

        # and an own velocity
        self.velocity = velocity

        # and an own mass
        self.mass = mass

        # my obj
        self.obj = pywavefront.Wavefront(obj)

    # apply the Force
    def applyForce(self, dt):
        global gravitation

        # old velocity added by the force given in dependence to Time gone and the mass
        self.velocity[0] = self.velocity[0] + gravitation[0] * (dt / self.mass)
        self.velocity[1] = self.velocity[1] + gravitation[1] * (dt / self.mass)
        self.velocity[2] = self.velocity[2] + gravitation[2] * (dt / self.mass)

    # new position has to be calculated
    def increment(self, dt):
        t = time.clock()
        passed = t - dt
        # we want time passed in seconds
        passed = passed/1000
        self.applyForce(passed)

        # new position is old position + velocity in dependence to the time gone
        self.position[0] = self.position[0] + self.velocity[0] * passed
        self.position[1] = self.position[1] + self.velocity[1] * passed
        self.position[2] = self.position[2] + self.velocity[2] * passed

    # some function to combine two particles to one @todo
    def combine(self, other):
        '''
        newPos = (self.position + other.position) * 0.5
        newMass = self.mass + other.mass
        newVel = (self.velocity * self.mass + other.velocity * other.mass) * (1 / newMass)
        self.position = newPos
        self.mass = newMass
        self.velocity = newVel
        '''

    def draw(self, deltaT):
        self.increment(deltaT)
        glTranslatef(self.position[0], self.position[1], self.position[2])
        self.obj.draw()

    def getBound(self):
        xs = [v[0] for v in self.obj.vertx]
        ys = [v[1] for v in self.obj.vertx]
        zs = [v[2] for v in self.obj.vertx]
        return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))