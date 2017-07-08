# Class for a single Particle
# a Particle always has a position, speed and a mass
# a Particle checks in every step which grid is his position
import math

import pywavefront
import object
import numpy as np
from math import atan

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
        self.elasticity = 1

        # and an own mass
        self.mass = mass

        # my obj
        self.obj = pywavefront.Wavefront(obj)

        # my VoxelIndex
        self.voxelIndex = (int(round(self.position[0])) + world.worldSize,
                           int(round(self.position[1])) + world.worldSize,
                           int(round(self.position[2])) + world.worldSize)

        # my voxel
        self.voxel = [self.voxelIndex]

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

    def calcAngleCollision(self, world, x, z):
        # returns angle and direction in the Form:
        # angle 1 means up, angle 0 meanse straight to left or rigth
        # angle, (right, rightDown, down, leftdown, left, leftTop, top, topRight )
        xReal = self.position[0] + world.worldSize - 1
        zReal = self.position[2] + world.worldSize - 1

        xDiff = x - xReal
        zDiff = z - zReal

        # defaulValue are to the Top and directly
        angle = (-1, -1, -1, -1, -1, -1, 90, -1)

        if abs(xDiff) > abs(zDiff) * 2:
            # our lean is only to X axis
            if xDiff >= 0:
                # to the right
                angle = (atan(abs(world.terrainHeightMap[x + 1][z] - self.position[1])), -1, -1, -1, -1, -1, -1, -1)
            else:
                # to the left
                angle = (-1, -1, -1, -1, atan(abs(world.terrainHeightMap[x - 1][z] - self.position[1])), -1, -1, -1)
        elif abs(zDiff) > abs(xDiff) * 2:
            # our lean is only to Z axis
            if zDiff >= 0:
                # to the Top
                angle = (-1, -1, -1, -1, -1, -1, atan(abs(world.terrainHeightMap[x][z + 1] - self.position[1])), -1)
            else:
                # to the Bottom
                angle = (-1, -1, atan(abs(world.terrainHeightMap[x][z - 1] - self.position[1])), -1, -1, -1, -1, -1)
        elif xDiff >= 0:
            if zDiff >= 0:
                # to the Top-Right
                angle = (-1, -1, -1, -1, -1, -1, -1, atan(abs(world.terrainHeightMap[x + 1][z + 1] - self.position[1])))
            elif zDiff < 0:
                # to the Down-Right
                angle = (-1, atan(abs(world.terrainHeightMap[x + 1][z - 1] - self.position[1])), -1, -1, -1, -1, -1, -1)
        elif xDiff < 0:
            if zDiff >= 0:
                # to the Top-Left
                angle = (-1, -1, -1, -1, -1, atan(abs(world.terrainHeightMap[x - 1][z + 1] - self.position[1])), -1, -1)
            if zDiff < 0:
                # to the Down-Left
                angle = (-1, -1, -1, atan(abs(world.terrainHeightMap[x - 1][z - 1] - self.position[1])), -1, -1, -1, -1)
        else:
            print("can't bee!")

        return (angle)

    def increment(self, dt, world):

        # save voxel before
        preVoxel = self.voxel

        # we want time passed in seconds
        passed = float(dt) / 1000

        # collision with heightmap
        x = int(round(self.position[0])) + world.worldSize - 1
        z = int(round(self.position[2])) + world.worldSize - 1

        # if there is a Collision with Terrain
        if self.position[1] <= world.terrainHeightMap[x][z]:
            # calculate the Angle and direction
            angle = self.calcAngleCollision(world, x, z)

            # react on Collision
            self.collisionResponse(angle)
        else:
            self.applyGravity(passed)

        # calc new Posititon
        # new position is old position + speed in dependence to the time gone
        self.position[0] += self.speed[0] * passed
        self.position[1] += self.speed[1] * passed
        self.position[2] += self.speed[2] * passed

        # check Grid
        self.checkGrid(preVoxel, world)

    # @todo: some function to combine two particles to one
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

    def collisionResponse(self, angle):
        # @todo add angle and force
        #if angle == (0, 0, 0, 0, 1, 0, 0, 0):
            # to the left
        print angle[0]
        fullSpeed = self.speed[0] + self.speed[1] + self.speed[2]

        if angle[0] > -1:
            # it goes to the right
            self.speed[0] = abs((fullSpeed*(1-angle[0])*self.elasticity))
            self.speed[1] = abs((fullSpeed*(angle[0])*self.elasticity))
            self.speed[2] = 0
        elif angle[1] > -1:
            # it goes to the rightDown
            self.speed[0] = abs((fullSpeed * (1 - angle[1])/2 * self.elasticity))
            self.speed[1] = abs((fullSpeed * (angle[1]) * self.elasticity))
            self.speed[2] = -abs((fullSpeed * (1 - angle[1])/2 * self.elasticity))
        elif angle[2] > -1:
            # it goes down
            self.speed[0] = 0
            self.speed[1] = abs((fullSpeed * (angle[2]) * self.elasticity))
            self.speed[2] = -abs((fullSpeed * (1 - angle[2]) * self.elasticity))
        elif angle[3] > -1:
            # it goes to the leftdown
            self.speed[0] = -abs((fullSpeed * (1 - angle[3])/2 * self.elasticity))
            self.speed[1] = abs((fullSpeed * (angle[3]) * self.elasticity))
            self.speed[2] = -abs((fullSpeed * (1 - angle[3])/2 * self.elasticity))
        elif angle[4] > -1:
            # it goes to the left
            self.speed[0] = -abs((fullSpeed * (1 - angle[4]) * self.elasticity))
            self.speed[1] = abs((fullSpeed * (angle[4]) * self.elasticity))
            self.speed[2] = 0
        elif angle[5] > -1:
            # it goes to the leftTop
            self.speed[0] = -abs((fullSpeed * (1 - angle[5])/2 * self.elasticity))
            self.speed[1] = abs((fullSpeed * (angle[5]) * self.elasticity))
            self.speed[2] = abs((fullSpeed * (1 - angle[5])/2 * self.elasticity))
        elif angle[6] > -1:
            # it goes to the top
            self.speed[0] = 0
            self.speed[1] = abs((fullSpeed * (angle[6]) * self.elasticity))
            self.speed[2] = abs((fullSpeed * (1 - angle[6]) * self.elasticity))
        elif angle[7] > -1:
            # it goes to the topRight
            self.speed[0] = abs((fullSpeed * (1 - angle[7])/2 * self.elasticity))
            self.speed[1] = abs((fullSpeed * (angle[7]) * self.elasticity))
            self.speed[2] = abs((fullSpeed * (1 - angle[7])/2 * self.elasticity))
        else:
            print("can't be")


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

