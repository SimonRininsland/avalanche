# Our world model
# out Terrain has a Radius of 64. It's 128 big

import numpy as np

class world(object):
    def __init__(self):
        # our Plane radius
        self.worldSize = 64

        # We have 128 Terrain und 1 at each site to add a invisible wall
        # Means 128 + 2
        self.gridResolution = 130

        # The Heightmap has the same Resolution as the World
        self.terrainHeightMap = np.zeros((self.gridResolution, self.gridResolution), dtype=float)

        # fill with Zeros
        self.grid = np.zeros((self.gridResolution, self.gridResolution, self.gridResolution), dtype=int)

        # -1 means is empty
        self.grid.fill(-1)

        i = 0
        while i < self.gridResolution:
            self.grid[i][i][0] = 99999
            self.grid[0][i][i] = 99999
            self.grid[i][i][i] = 99999
            self.grid[i][0][0] = 99999
            self.grid[0][i][0] = 99999
            self.grid[0][0][i] = 99999
            self.grid[i][i][self.gridResolution-1] = 99999
            self.grid[self.gridResolution-1][i][i] = 99999
            self.grid[i][i][i] = 99999
            self.grid[i][self.gridResolution-1][self.gridResolution-1] = 99999
            self.grid[self.gridResolution-1][i][self.gridResolution-1] = 99999
            self.grid[self.gridResolution-1][self.gridResolution-1][i] = 99999
            i += 1


    def getGridResolution(self):
        return self.gridResolution