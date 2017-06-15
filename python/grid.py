import numpy as np


class Grid:
    def __init__(self, gridSize):
        self.vol = np.full((2,3),gridSize)

    def check(self):
