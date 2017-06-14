# Our world modell

import numpy as np

class World(object):

    def __init__(self, ):

        self.gridresolution = 32

        self.grid = np.full((32, 32, 32), 0)
