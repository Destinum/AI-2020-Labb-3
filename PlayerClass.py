import copy
from UnitClass import *

class Player:
    def __init__(self, StartingLocation, Map):
        self.ExploredTiles = copy.deepcopy(Map)

        X = -1
        Y = -1

        while X < 2:
            while Y < 2:
                #print(ExploredTiles[yValue + Y][xValue + X])
                self.ExploredTiles[(StartingLocation[1] + Y)][(StartingLocation[0] + X)] = "Explored"
                Y += 1
            X += 1
            Y = -1

    Units = []

    def AddUnit(self, Unit):
        self.Units.append(Unit)
