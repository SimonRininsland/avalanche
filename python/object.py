# Class for an Object
# One Object is a collideable Obstacle

from OpenGL.GL import *
# used: https://github.com/greenmoss/PyWavefront
import pywavefront
import particle
import numpy as np

class object():
    def __init__(self, position, obj, world):
        # every Object has an own position
        self.position = position

        # The obj
        self.obj = pywavefront.Wavefront(obj)

        # init Terrain HeightMap
        self.getHeightMap(world)


    def increment(self, dt, world):
        pass

    def draw(self, deltaT, world):
        self.increment(deltaT, world)
        glTranslatef(self.position[0], self.position[1], self.position[2])
        #glScalef(self.mass,self.mass,self.mass)
        self.obj.draw()
        glTranslatef(-self.position[0], -self.position[1], -self.position[2])


    def getHeightMap(self, world):
        # map heigth of vertice in array
        for vertice in self.obj.vertx:
            x = int(round(vertice[0])) + world.worldSize - 1
            y = int(round(vertice[1]))
            z = int(round(vertice[2])) + world.worldSize - 1

            world.terrainHeightMap[x][z] = y

        # to not have false zeros in height array:
        for x, heights in enumerate(world.terrainHeightMap):
            for z, height in enumerate(heights):
                # go through Heighmap
                if height <= 0:
                    # search for Zeros (comes in the EndPoints of the Terrain ) and correct them
                    if z == 0:
                        world.terrainHeightMap[x][z] = ((heights[z + 1] + heights[z + 2]) / 2)
                    elif z >= (len(world.terrainHeightMap)-1):
                        world.terrainHeightMap[x][z] = ((heights[z - 1] + heights[z - 2]) / 2)
                    else:
                        world.terrainHeightMap[x][z] = ((heights[z - 1] + heights[z + 1]) / 2)


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