# Our world model
# our world space is from 2 to 2 and is squared in 4 parts 4*4*4
# always take gridResolutions x * 4

import numpy as np

class world(object):
    def __init__(self):
        # all Axis +2 to -2
        self.worldSize = 2

        # 10*10*10 in worldSize above
        self.gridResolution = 4

        self.grid = np.empty([self.gridResolution])

    def getGridResolution(self):
        return self.gridResolution