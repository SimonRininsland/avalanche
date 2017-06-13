# Class for a single Particle
# a Particle always has a position, velocity and a mass

from OpenGL.GL import *
# used: https://github.com/greenmoss/PyWavefront
import pywavefront, time

# The Gravitation
gravitation = -9.81

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

        for x in self.obj.materials:
            for y in x.vertices:
                print y

    # apply the Force
    def applyForce(self, dt):
        global gravitation

        # old velocity added by the force given in dependence to Time gone and the mass
        self.velocity = self.velocity + gravitation * (dt / self.mass)

    # new position has to be calculated
    def increment(self, dt):
        t = time.clock()
        passed = t - dt
        # we want time passed in seconds
        passed = passed/1000
        self.applyForce(passed)

        # new position is old position + velocity in dependence to the time gone
        # @todo do for x and z too
        #self.position[0] = self.position[0] + self.velocity * passed
        # only Y for now
        self.position[1] = self.position[1] + self.velocity * passed
        #self.position[1] = self.position[2] + self.velocity * passed

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