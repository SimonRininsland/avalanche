# Our world modell

import numpy as np
# import grid

class World(object):

    def __init__(self, ):

        self.gridResolution = 32

        # self.grid = np.full((self.gridResolution, self.gridResolution,self.gridResolution, 6), 0)
        self.grid = np.mgrid[0:32*32:32,0:32*32:32,0:32*32:32]





Test = World()

print Test.grid
