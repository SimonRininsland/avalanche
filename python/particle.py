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
        xReal = self.position[0] + world.worldSize - 1
        zReal = self.position[2] + world.worldSize - 1

        # identify Face collided
        myCollisionFace = [[x, world.terrainHeightMap[x][z], z]]
        
        if xReal-x >= 0:
            myCollisionFace.append([x + 1, world.terrainHeightMap[x + 1][z], z])
        else:
            myCollisionFace.append([x - 1, world.terrainHeightMap[x - 1][z], z])
        if (zReal - z) >= 0:
            myCollisionFace.append([x, world.terrainHeightMap[x][z + 1], z + 1])
        if (zReal - z) < 0:
            myCollisionFace.append([x, world.terrainHeightMap[x][z - 1], z - 1])

        # calculate normal of Face
        normal = np.cross(np.subtract(myCollisionFace[1], myCollisionFace[0]),
                            np.subtract(myCollisionFace[2], myCollisionFace[0]))
        normalizedNormale = normal/np.linalg.norm(normal)

        # map NormalVector on myVector
        mapedVector = np.dot(self.speed, normalizedNormale)
        normalizeMapedVector = mapedVector/np.linalg.norm(mapedVector)

        # calculate my output Vector
        outputVector = np.subtract(np.add(2 * normalizeMapedVector * normalizedNormale, self.position), self.speed)

        return outputVector

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
        self.speed[0] = self.speed[0] * self.elasticity + collisionForce[0]
        self.speed[1] = self.speed[1] * self.elasticity + collisionForce[1]
        self.speed[2] = self.speed[2] * self.elasticity + collisionForce[2]

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
