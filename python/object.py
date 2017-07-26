# Class for an Object
# One Object is a collideable Obstacle

from OpenGL.GL import *
# used: https://github.com/greenmoss/PyWavefront
import pywavefront
import particle

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
        if isinstance(self, particle.particle):
            self.increment(deltaT, world)
            glTranslatef(self.position[0], self.position[1], self.position[2])
            #glScalef(self.mass,self.mass,self.mass)
            self.obj.draw()
            glTranslatef(-self.position[0], -self.position[1], -self.position[2])

            for self.emitterFlake in self.emitterFlakes:
                glTranslatef(self.position[0] + self.emitterFlake[0],
                             self.position[1] + self.emitterFlake[1],
                             self.position[2] + self.emitterFlake[2])
                self.obj.draw()
                glTranslatef(-(self.position[0] + self.emitterFlake[0]),
                             -(self.position[1] + self.emitterFlake[1]),
                             -(self.position[2] + self.emitterFlake[2]))
        else:
            self.obj.draw()


    def getHeightMap(self, world):
        # map heigth of vertice in array
        for vertice in self.obj.vertx:
            x = int(round(vertice[0])) + world.worldSize
            y = vertice[1]
            z = int(round(vertice[2])) + world.worldSize

            world.terrainHeightMap[x][z] = y

        # to not have false zeros in height array:
        for x, heights in enumerate(world.terrainHeightMap):
            for z, height in enumerate(heights):
                # go through Heighmap
                if height <= 0:
                    # search for Zeros (comes in the EndPoints of the Terrain ) and correct them
                    if z == 0:
                        # if i'm at the endpoints set heigth to hight to react
                        world.terrainHeightMap[x][z] = 9999
                    elif z >= (len(world.terrainHeightMap)-1):
                        # if i'm at the endpoints set heigth to hight to react
                        world.terrainHeightMap[x][z] = 9999
                    else:
                        world.terrainHeightMap[x][z] = ((heights[z - 1] + heights[z + 1]) / 2)

    def getBound(self):
        xs = [v[0] for v in self.obj.vertx]
        ys = [v[1] for v in self.obj.vertx]
        zs = [v[2] for v in self.obj.vertx]
        return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

    def collisionDetection(self, obj):
        if isinstance(obj, particle.particle):
            obj.collisionDetection(self)


    def collisionResponse(self):
        pass