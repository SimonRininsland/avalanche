# Our world modell

import numpy as np


# import grid

class World(object):
    def __init__(self, collisionGrid):
        self.collisionGrid = collisionGrid
        '''self.gridResolution = 32

        # self.grid = np.full((self.gridResolution, self.gridResolution,self.gridResolution, 6), 0)
        self.grid = np.mgrid[0:32*32:32,0:32*32:32,0:32*32:32]'''

    def checkCollision(self, drawObjectsArray):
        objectArray = drawObjectsArray

        for cOid, collisionObject in enumerate(self.collisionGrid):
            for oOid, obstacleObject in enumerate(self.collisionGrid):
                if cOid != oOid:

                    # Bounds from obejct:
                    # (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)) '''
                    collision = ((collisionObject[1] >= obstacleObject[0] and collisionObject[1] <= obstacleObject[1])
                                   or (
                                   collisionObject[0] <= obstacleObject[1] and collisionObject[0] >= obstacleObject[0]))\
                                  and (
                                  (collisionObject[3] >= obstacleObject[2] and collisionObject[3] <= obstacleObject[3])
                                  or (
                                  collisionObject[2] <= obstacleObject[3] and collisionObject[2] >= obstacleObject[2]))\
                                  and (
                                  (collisionObject[5] >= obstacleObject[4] and collisionObject[5] <= obstacleObject[5])
                                  or (
                                  collisionObject[4] <= obstacleObject[5] and collisionObject[4] >= obstacleObject[4]))
                    # if there is a collision call the collsion function from the objects
                    if (collision):
                        objectArray[cOid].collision()
                        objectArray[oOid].collision()
