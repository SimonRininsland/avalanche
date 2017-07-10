# Class for a single Particle
# a Particle always has a position, speed and a mass
# a Particle checks in every step which grid is his position
import math

import pywavefront
import object
import numpy as np
from math import atan2, sqrt, asin, pi

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
        self.elasticity = 0.7

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
        self.speed[0] += gravitation[0] * (1- self.airDrag) * (dt / self.mass)
        self.speed[1] += gravitation[1] * (1- self.airDrag) * (dt / self.mass)
        self.speed[2] += gravitation[2] * (1- self.airDrag) * (dt / self.mass)

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
                    #@todo: Next step Collide with other Particles
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

    def calcForceCollisionWithTerrain(self, world, x, z):
        # returns angle and direction in the Form:

        # RealPositin is my position in world
        xReal = self.position[0] + world.worldSize - 1
        zReal = self.position[2] + world.worldSize - 1

        # calc the x and z direction
        collisionDirection = [x - xReal, z - zReal]

        # local Terrain Height (absolut Height - position[1])
        localHeight = abs(world.terrainHeightMap[x][z] - self.position[1])


        print "mySpeed:", self.speed
        print "collisionDirection ", collisionDirection
        ax = atan2(sqrt(self.speed[1] ** 2 + self.speed[2] ** 2), self.speed[0])
        ay = atan2(sqrt(self.speed[2] ** 2 + self.speed[0] ** 2), self.speed[1])
        az = atan2(sqrt(self.speed[0] ** 2 + self.speed[1] ** 2), self.speed[2])
        print "angles of Particles", ax, ay, az

        # angle on Terrain x = asin(a/b) a = localHeight, c = length between x,z and self.position[0], self.position[2]:
        angleT = asin(localHeight/(sqrt((self.position[0]-x)**2 + (self.position[2]-z)**2)))
        print "angle of hit Terrain", angleT

        # angle of the Particle on the Terain(- pi/2 to get the next to calc X)
        px = (pi - ax - angleT) - pi/2
        py = (pi - ay - angleT) - pi/2
        pz = (pi - az - angleT) - pi/2

        fx = pi - px * 2 + ax
        fy = pi - py * 2 + ay
        fz = pi - pz * 2 + az
        # outgoing angle:


        print "angles of Particle", fx, fy, fz

        # if the angle is 0 it's it's fully up. if it's near to 1 it's in collisionDirection.

        collisionForce = [fx, fy, fz]
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

        r = ((max(xs) - min(xs))* self.mass / 2)

        x = (max(xs) - r)
        y = (max(xs) - r)
        z = (max(xs) - r)

        return (x, y, z, r)

    def collisionResponse(self, collisionForce):
        # fullSpeed has to be hold by
        fullSpeed = self.speed[0] + self.speed[1] + self.speed[2]

        # the collisionForce impacts the different Axis
        self.speed[0] = abs(fullSpeed * collisionForce[0]*self.elasticity)
        self.speed[1] = abs(fullSpeed * collisionForce[1]*self.elasticity)
        self.speed[2] = abs(fullSpeed * collisionForce[2]*self.elasticity)

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

        '''elif isinstance(obj, object.object):
            x = max((tmpO[0] - obj.position[0]), min((tmpP[0] - self.position[0]), (tmpO[1] - obj.position[0])))
            y = max((tmpO[2] - obj.position[1]), min((tmpP[1] - self.position[1]), (tmpO[3] - obj.position[1])))
            z = max((tmpO[4] - obj.position[2]), min((tmpP[2] - self.position[2]), (tmpO[5] - obj.position[2])))
            distance = math.sqrt(
                math.pow((x - (tmpP[0] - self.position[0])), 2) +
                math.pow((y - (tmpP[1] - self.position[1])), 2) +
                math.pow((z - (tmpP[2] - self.position[2])), 2)
            )
            isColliding = distance < tmpP[3]'''

        elif False:
            distance = math.sqrt(
                math.pow((tmpO[0] - obj.position[0]) - (tmpP[0] - self.position[0]), 2) +
                math.pow((tmpO[1] - obj.position[1]) - (tmpP[1] - self.position[1]), 2) +
                math.pow((tmpO[2] - obj.position[2]) - (tmpP[2] - self.position[2]), 2)
            )
            isColliding = distance < tmpP[3]

        if isColliding:
            # @todo false yet
            self.collisionResponse(obj.speed)
            obj.collisionResponse(self.speed)

