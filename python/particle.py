# Class for a single Particle
# a Particle always has a position, velocity and a mass
import math

import pywavefront
import object

# The Gravitation
gravitation = [0, -9.81, 0]


class particle(object.object):
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
        # we want time passed in seconds
        passed = float(dt) / 1000
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

    def getBound(self):
        xs = [v[0] for v in self.obj.vertx]

        r = (max(xs) - min(xs)) / 2

        x = max(xs) - r
        y = max(xs) - r
        z = max(xs) - r

        return (x, y, z, r)

    def collisionResponse(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = -self.velocity[1]
        self.velocity[2] = -self.velocity[2]


    def collisionDetection(self, obj):
        tmpP = self.getBound()
        tmpO = obj.getBound()
        isColliding = False
        if isinstance(obj, particle):
            distance = math.sqrt(
                math.pow((tmpP[0] - self.position[0]) - (tmpO[0] - obj.position[0]), 2) +
                math.pow((tmpP[1] - self.position[1]) - (tmpO[1] - obj.position[1]), 2) +
                math.pow((tmpP[2] - self.position[2]) - (tmpO[2] - obj.position[2]), 2)
            )
            isColliding = distance < (tmpP[3] + tmpO[3])

        # @todo still has an error calculation with the position has to be fixed
        elif isinstance(obj, object.object):
            x = max((tmpO[0] - obj.position[0]), min((tmpP[0] - self.position[0]), (tmpO[1] - obj.position[0])))
            y = max((tmpO[2] - obj.position[1]), min((tmpP[1] - self.position[1]), (tmpO[3] - obj.position[1])))
            z = max((tmpO[4] - obj.position[2]), min((tmpP[2] - self.position[2]), (tmpO[5] - obj.position[2])))
            distance = math.sqrt(
                math.pow(((x - obj.position[0]) - (tmpP[0] - self.position[0])), 2) +
                math.pow(((y - obj.position[1]) - (tmpP[1] - self.position[1])), 2) +
                math.pow(((z - obj.position[2]) - (tmpP[2] - self.position[2])), 2)
            )
            isColliding = distance < tmpP[3]

        # very not correct collision handling at the moment @todo everything
        if isColliding:
            self.collisionResponse()
            obj.collisionResponse()

