# Class for a single Particle
# a Particle always has a position, speed and a mass
# a Particle checks in every step which grid is his position
import math

import pywavefront
import object
import numpy as np

# The Gravitation
gravitation = [0, -9.81, 0]

# check if the distace to plane is less than Threshold
collisionDistanceThreshold = 0.01


class particle(object.object):
    def __init__(self, position, speed, mass, obj, index, world, drawObjectsArray):
        # an own index
        self.index = index

        # every Particle has an new own positionget_vert
        self.position = position

        # and an own speed
        self.speed = speed

        # and an own elasticity 1:perfect bounce 0: zero bounce 0.7
        self.elasticity = 0.9

        # and an own mass
        self.mass = mass

        # and an air drag 0.9
        self.airDrag = 0.8

        # my obj
        self.obj = pywavefront.Wavefront(obj)

        # my voxel
        self.voxel = [[int(round(self.position[0])) + world.worldSize],
                      [int(round(self.position[1])) + world.worldSize],
                      [int(round(self.position[2])) + world.worldSize]]

        # allObjects
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
                      [int(round(self.position[1]))],
                      [int(round(self.position[2])) + world.worldSize]]

        # if voxel is empty
        if world.grid[self.voxel] == -1:
            world.grid[self.voxel] = self.index
        else:
            if world.grid[self.voxel] != self.index:
                # check a collision
                for collObjIndex in world.grid[self.voxel]:
                    if isinstance(self.drawObjectsArray[collObjIndex], particle):
                        if self.index != self.drawObjectsArray[collObjIndex].index:
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

    def calcForceCollisionWithParticle(self, obj):


        tmpS = self.getBound()
        tmpO = obj.getBound()

        # midpoint in world
        xs, ys, zs = (tmpS[0] + self.position[0], tmpS[1] + self.position[1], tmpS[2] + self.position[2])
        xo, yo, zo = (tmpO[0] + obj.position[0], tmpO[1] + obj.position[1], tmpO[2] + obj.position[2])

        # distance between two points
        xr, yr, zr = (xo - xs, yo - ys, zo - zs)

        # collision point
        xc, yc, zc = (xo - xr / 2, yo - yr / 2, zo - zr / 2)

        collisionPoint = (xc, yc, zc)

        vn1 = collisionPoint / np.linalg.norm(collisionPoint) * np.dot(self.speed, collisionPoint) / np.linalg.norm(
            collisionPoint)

        vt1 = collisionPoint - vn1

        vn2 = collisionPoint / np.linalg.norm(collisionPoint) * np.dot(obj.speed, collisionPoint) / np.linalg.norm(
            collisionPoint)

        vt2 = collisionPoint - vn1

        self.collisionResponse((vn2 + vt1))
        obj.collisionResponse((vn1 + vt2))


    def calcForceCollisionWithTerrain(self, normalizedPNormale):
        # map NormalVector on myVector
        mapedVector = np.dot(self.speed, normalizedPNormale)/np.linalg.norm(normalizedPNormale)

        # calculate my output Vector
        outputVector = np.add(np.subtract((2 * mapedVector * normalizedPNormale), self.speed), self.position)

        return outputVector

    def checkCollisonWithterrain(self, passed, world):
        # collision with heightmap
        x = int(round(self.position[0])) + world.worldSize
        z = int(round(self.position[2])) + world.worldSize

        # realposition
        xReal = self.position[0] + world.worldSize
        zReal = self.position[2] + world.worldSize
        realPosition = [xReal, self.position[1], zReal]

        xDifToCenter = xReal - x
        zDifToCenter = zReal - z

        # identify Face collided
        myCollisionFace = [[x, world.terrainHeightMap[x][z], z]]

        # in right
        if xDifToCenter >= 0:
            if zDifToCenter >= 0:
                # in upper Right
                myCollisionFace.append([x + 1, world.terrainHeightMap[x + 1][z + 1], z + 1])
                # to exlude 0/0
                if (xDifToCenter == zDifToCenter or xDifToCenter / zDifToCenter <= 1) and zDifToCenter != 0:
                    myCollisionFace.append([x, world.terrainHeightMap[x][z + 1], z + 1])
                # Right
                else:
                    myCollisionFace.append([x + 1, world.terrainHeightMap[x + 1][z], z])
            else:
                #down
                myCollisionFace.append([x, world.terrainHeightMap[x][z - 1], z - 1])
                myCollisionFace.append([x + 1, world.terrainHeightMap[x + 1][z], z])
        else:
            if zDifToCenter < 0:
                # in upper Right
                myCollisionFace.append([x - 1, world.terrainHeightMap[x - 1][z - 1], z - 1])
                # down down
                if (xDifToCenter == zDifToCenter or xDifToCenter / zDifToCenter <= 1) and zDifToCenter != 0:
                    myCollisionFace.append([x, world.terrainHeightMap[x][z-1], z-1])
                # Left
                else:
                    myCollisionFace.append([x-1, world.terrainHeightMap[x -1][z], z])
            else:
                #left top
                myCollisionFace.append([x, world.terrainHeightMap[x][z + 1], z + 1])
                myCollisionFace.append([x - 1, world.terrainHeightMap[x - 1][z], z])

        # there could be a collision
        # i have found collisionFace and speed is stable
        if self.position[1] + self.getBound()[1] <= max([myCollisionFace[0][1], myCollisionFace[1][1], myCollisionFace[2][1]]):
            # what i do:
            # i calculate the normal of the collisionFace
            # i calculate a normal from a second Face with 2 points from CollisionFace and one is my point
            # i normalize both and calc a dot Product. DotProduct of two normalized vectors is 1 if they are parralel
            # (means here the same). Because position is changes per Frame we hae to add a Threshold

            # calculate normal of Face
            normal = np.cross(np.subtract(myCollisionFace[1], myCollisionFace[0]),
                              np.subtract(myCollisionFace[2], myCollisionFace[0]))

            normalizedNormale = normal / np.linalg.norm(normal)

            # calculate Face from my Point to 2 points of collisonFace
            pointFace = [realPosition, myCollisionFace[1], myCollisionFace[2]]

            # normal of pointFace
            pNormal = np.cross(np.subtract(pointFace[1], pointFace[0]),
                              np.subtract(pointFace[2], pointFace[0]))
            normalizedPNormale = pNormal / np.linalg.norm(pNormal)

            # check if the distace to plane is less than Threshold
            # @todo: make distance related to speed
            if (1-np.dot(normalizedNormale, normalizedPNormale)) < collisionDistanceThreshold:
                # calc CollisionForce
                collisionForce = self.calcForceCollisionWithTerrain(normalizedPNormale)
                # react on Collision
                self.collisionResponse(collisionForce)

            if (np.dot(normalizedNormale, normalizedPNormale)) <0:
                exit("Particle is under the plate! Fix it")

        else:
            self.applyGravityAndAirDrag(passed)

        return realPosition

    def increment(self, dt, world):

        # save voxel before
        preVoxel = self.voxel

        # we want time passed in seconds
        passed = float(dt) / 1000

        # check and react on Terrain Collision
        self.checkCollisonWithterrain(passed, world)

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

        r = (max(xs) - min(xs))

        x = (max(xs) - r)
        y = (max(xs) - r)
        z = (max(xs) - r)

        return (x, y, z, r)

    def collisionResponse(self, collisionForce):
        # fullSpeed has to be hold by
        # the collisionForce impacts the different Axis
        self.speed[0] += collisionForce[0] * self.elasticity
        self.speed[1] += collisionForce[1] * self.elasticity
        self.speed[2] += collisionForce[2] * self.elasticity

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
            self.calcForceCollisionWithParticle(obj)
