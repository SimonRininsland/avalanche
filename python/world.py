# Our world model
# out Terrain has a Radius of 64. It's 128 big

import numpy as np

class world(object):
    def __init__(self):
        # our Plane has a radius of
        self.worldSize = 64

        # 10*10*10 in worldSize above
        self.gridResolution = 128

        self.grid = np.empty((self.gridResolution, self.gridResolution, self.gridResolution), dtype=int)

    def getGridResolution(self):
        return self.gridResolution