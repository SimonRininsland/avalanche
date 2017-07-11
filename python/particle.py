# Class for a single Particle
# a Particle always has a position, speed and a mass
# a Particle checks in every step which grid is his position
import math

import pywavefront
import object
import numpy as np
from math import atan2, sqrt, atan, pi, degrees

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

        # and an own elasticity 1:perfect bounce 0: zero bounce 0.7
        self.elasticity = 1

        # and an own mass
        self.mass = mass

        # and an air drag 0.8
        self.airDrag = 0

        # my obj
        self.obj = pywavefront.Wavefront(obj)

        # my VoxelIndex
        self.voxelIndex = (int(round(self.position[0])) + world.worldSize,
                           int(round(self.position[1])) + world.worldSize,
                           int(round(self.position[2])) + world.worldSize)

        # my voxel
        self.voxel = [self.voxelIndex]

        self.drawObjectsArray = drawObjectsArray

    def applyGravityAndAirDrag(self, dt):
        # apply the Force
        global gravitation

        # old speed added by the force given in dependence to Time gone and the mass
        self.speed[0] += gravitation[0] * (1 - self.airDrag) * (dt / self.mass)
        self.speed[1] += gravitation[1] * (1 - self.airDrag) * (dt / self.mass)
        self.speed[2] += gravitation[2] * (1 - self.airDrag) * (dt / self.mass)

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
                    pass
                    # @todo: Next step Collide with other Particles
                    #self.collisionDetection(self.drawObjectsArray[collObjIndex])

                # and append myself
                np.append(world.grid[self.voxel], self.index)

        # i'm in a new voxel
        if preVoxel != self.voxel:

            # to avoid having an empty non existing array in grid
            if len(world.grid[preVoxel]) <= 1:
                world.grid[preVoxel] = -1
            else:
                np.delete(world.grid[preVoxel], self.index)

    def calcForceCollisionWithParticle(self, world, x, z):

        pass

    def calcForceCollisionWithTerrain(self, world, x, z):
        # returns angle and direction mapped to 1

        # RealPositin is my position in world
        xReal = self.position[0] + world.worldSize - 1
        zReal = self.position[2] + world.worldSize - 1

        # x, Z Coeffizeint, 0,5 = Full = 1
        xCoe = (xReal - x) / (abs(xReal - x) + abs(zReal - z))
        zCoe = (zReal - z) / (abs(xReal - x) + abs(zReal - z))
        print "x", xCoe, "z", zCoe

        # local Terrain Height (absolut Height - position[1])
        localHeight = abs(world.terrainHeightMap[x][z] - self.position[1])

        print "mySpeed:", self.speed
        # calculate angle from Particles with ground(not terrain)
        ax = atan2(sqrt(self.speed[1] ** 2 + self.speed[2] ** 2), self.speed[0])
        ay = atan2(sqrt(self.speed[2] ** 2 + self.speed[0] ** 2), self.speed[1])
        az = atan2(sqrt(self.speed[0] ** 2 + self.speed[1] ** 2), self.speed[2])
        print "Particle angle on ground: ", degrees(ax), degrees(ay), degrees(az)

        # angle on Terrain x = asin(a/b) a = localHeight, c = length between x,z and self.position[0], self.position[2]:
        # angle of the Particle on the Terain(- pi/2 to get the next to calc X)
        print "Terrain angle: ", degrees(atan(localHeight / (sqrt((xReal - x) ** 2 + (zReal - z) ** 2))))

        pOnTx = (ax - atan(localHeight / (sqrt((xReal - x) ** 2 + (zReal - z) ** 2)))) * xCoe
        pOnTy = ay - atan(localHeight / (sqrt((xReal - x) ** 2 + (zReal - z) ** 2)))
        pOnTz = (az - atan(localHeight / (sqrt((xReal - x) ** 2 + (zReal - z) ** 2)))) * zCoe

        print "angles of Particle with Terrain", degrees(pOnTx), degrees(pOnTy), degrees(pOnTz)

        outAngles = [pi - pOnTx, pi - pOnTy, pi - pOnTz]
        normOutAngles = [outAngles[0] / (abs(outAngles[0]) + abs(outAngles[1]) + abs(outAngles[2])),
                         outAngles[1] / (abs(outAngles[0]) + abs(outAngles[1]) + abs(outAngles[2])),
                         outAngles[2] / (abs(outAngles[0]) + abs(outAngles[1]) + abs(outAngles[2]))]
        print "out angles of Particle with Terrain", (
        degrees(outAngles[0]), degrees(outAngles[1]), degrees(outAngles[2]))
        print "normed", normOutAngles

        # if the angle is 0 it's it's fully up. if it's near to 1 it's in collisionDirection.
        fullSpeed = abs(self.speed[0]) + abs(self.speed[1]) + abs(self.speed[2])

        # CollisionAngles mapped to one
        collisionForce = [normOutAngles[0] * fullSpeed,
                          normOutAngles[1] * fullSpeed,
                          normOutAngles[2] * fullSpeed]

        print "collisionForce ", collisionForce
        return (collisionForce)

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
            collisionForce = self.calcForceCollisionWithTerrain(world, x, z)

            # react on Collision
            self.collisionResponse(collisionForce)
        else:
            self.applyGravityAndAirDrag(passed)

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

        r = ((max(xs) - min(xs)) * self.mass / 2)

        x = (max(xs) - r)
        y = (max(xs) - r)
        z = (max(xs) - r)

        return (x, y, z, r)

    def collisionResponse(self, collisionForce):
        # fullSpeed has to be hold by
        print collisionForce
        # the collisionForce impacts the different Axis
        self.speed[0] = collisionForce[0] * self.elasticity
        self.speed[1] = collisionForce[1] * self.elasticity
        self.speed[2] = collisionForce[2] * self.elasticity

    def collisionResponseParticle(self, obj):

        self.speed = [self.speed[0] * -1, self.speed[1] * -1, self.speed[2] * -1]

        tmpS = self.getBound()
        tmpO = obj.getBound()

        # midpoint in world
        xs, ys, zs = (tmpS[0] + self.position[0], tmpS[1] + self.position[1], tmpS[2] + self.position[2])
        xo, yo, zo = (tmpO[0] + obj.position[0], tmpO[1] + obj.position[1], tmpO[2] + obj.position[2])

        # distance between two points
        xr, yr, zr = (xs - xo, ys - yo, zs - zo)

        # collision point
        xc, yc, zc = (xo - xr / 2, yo - yr / 2, zo - zr / 2)

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

        if isColliding:
            # @todo false yet
            self.collisionResponseParticle(obj)
            obj.collisionResponseParticle(self)
