# Class for a single Particle
# a Particle always has a position, speed and a mass
# a Particle checks in every step which grid is his position
import math

import pywavefront
import object
import numpy as np

# The Gravitation
gravitation = [0, -9.81, 0]

class particle(object.object):
    def __init__(self, position, speed, mass, obj, index, world, drawObjectsArray):
        # an own index
        self.index = index

        # every Particle has an new own positionget_vert
        self.position = position

        # and an own speed
        self.speed = speed

        # and an own elasticity 1:perfect bounce 0: zero bounce
        self.elasticity = 0.8

        # and an own mass
        self.mass = mass

        # my obj
        self.obj = pywavefront.Wavefront(obj)

        # my voxel
        self.voxel = [[int(round(self.position[0])) + world.worldSize],
                   [int(round(self.position[1])) + world.worldSize],
                   [int(round(self.position[2])) + world.worldSize]]

        self.drawObjectsArray = drawObjectsArray

    def applyGravity(self, dt):
        # apply the Force
        global gravitation

        # old speed added by the force given in dependence to Time gone and the mass
        self.speed[0] += gravitation[0] * (dt / self.mass)
        self.speed[1] += gravitation[1] * (dt / self.mass)
        self.speed[2] += gravitation[2] * (dt / self.mass)

    def checkGrid(self, preVoxel, world):
        # check new Position Voxel
        # new Voxel
        self.voxel = [[int(round(self.position[0])) + world.worldSize],
                      [int(round(self.position[1])) + world.worldSize],
                      [int(round(self.position[2])) + world.worldSize]]

        # if voxel is empty
        if world.grid[self.voxel] == -1:
            world.grid[self.voxel] = self.index
        else:
            if world.grid[self.voxel] != self.index:
                # check a collision
                # print("Collision detected ")
                # print(world.grid[self.voxel])
                for collObjIndex in world.grid[self.voxel]:
                    self.collisionDetection(self.drawObjectsArray[collObjIndex])

                # and append myself
                np.append(world.grid[self.voxel], self.index)

        # i'm in a new voxel
        if preVoxel != self.voxel:

            # to avoid having an empty non existing array in grid
            if len(world.grid[preVoxel]) <= 1:
                world.grid[preVoxel] = -1
            else:
                np.delete(world.grid[preVoxel], self.index)

    # new position has to be calculated
    def increment(self, dt, world):

        # save voxel before
        preVoxel = self.voxel

        # we want time passed in seconds
        passed = float(dt) / 1000
        # @todo When Tiras has his Terrain Highmap, remove this:
        if self.position[1] < 0.0:
            self.collisionResponse()
        else:
            self.applyGravity(passed)



        # calc new Posititon
        # new position is old position + speed in dependence to the time gone
        self.position[0] += self.speed[0] * passed
        self.position[1] += self.speed[1] * passed
        self.position[2] += self.speed[2] * passed

        # check Grid
        self.checkGrid(preVoxel, world)

    # some function to combine two particles to one @todo
    def combine(self, other):
        '''
        newPos = (self.position + other.position) * 0.5
        newMass = self.mass + other.mass
        newVel = (self.speed * self.mass + other.speed * other.mass) * (1 / newMass)
        self.position = newPos
        self.mass = newMass
        self.speed = newVel
        '''

    def getBound(self):
        xs = [v[0] for v in self.obj.vertx]

        r = ((max(xs) - min(xs))* self.mass / 2)

        x = (max(xs) - r)
        y = (max(xs) - r)
        z = (max(xs) - r)

        return (x, y, z, r)

    def collisionResponse(self):
        # very not correct collision handling at the moment @todo everything

        self.speed[0] = abs(self.speed[0]*self.elasticity)
        self.speed[1] = abs(self.speed[1]*self.elasticity)
        self.speed[2] = abs(self.speed[2]*self.elasticity)


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

        elif isinstance(obj, object.object):
            x = max((tmpO[0] - obj.position[0]), min((tmpP[0] - self.position[0]), (tmpO[1] - obj.position[0])))
            y = max((tmpO[2] - obj.position[1]), min((tmpP[1] - self.position[1]), (tmpO[3] - obj.position[1])))
            z = max((tmpO[4] - obj.position[2]), min((tmpP[2] - self.position[2]), (tmpO[5] - obj.position[2])))
            distance = math.sqrt(
                math.pow((x - (tmpP[0] - self.position[0])), 2) +
                math.pow((y - (tmpP[1] - self.position[1])), 2) +
                math.pow((z - (tmpP[2] - self.position[2])), 2)
            )
            isColliding = distance < tmpP[3]

        if isColliding:
            self.collisionResponse()
            obj.collisionResponse()

