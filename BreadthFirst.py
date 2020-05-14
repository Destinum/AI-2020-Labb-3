import pygame
import time
import random
from WorldMap import *

class BreadthFirst:
    def __init__(self, StartCoordinates, FogMap, SearchingFor):
        self.CurrentList = []
        self.TempList = []
        self.Visited = []
        self.StartCoordinates = (StartCoordinates[0], StartCoordinates[1])
        self.CurrentCoordinates = (StartCoordinates[0], StartCoordinates[1])
        self.CurrentList.append(self.CurrentCoordinates)
        self.Visited.append(self.CurrentCoordinates)
        self.FogMap = FogMap
        self.SearchingFor = SearchingFor

##############################################################################

    def CheckTile(self, BaseX, BaseY):

        X = BaseX + self.CurrentCoordinates[0]
        Y = BaseY + self.CurrentCoordinates[1]

        if (self.FogMap[Y][X] == "Unknown" and self.SearchingFor == "Exploring"):
            for XY in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                if (self.FogMap[self.CurrentCoordinates[1] + XY[1]][self.CurrentCoordinates[0] + XY[0]] == "Unknown"):
                    self.FogMap[self.CurrentCoordinates[1] + XY[1]][self.CurrentCoordinates[0] + XY[0]] = "Being Explored"
            return True

        elif (TheWorld.Tiles[Y][X][0] == self.SearchingFor and self.FogMap[Y][X] == "Explored"):
            return True

        elif ((X, Y) not in self.Visited):
            self.Visited.append((X, Y))
            
            if (TheWorld.Tiles[Y][X][0] in ("V", "B")):
                return False

            self.TempList.append((X, Y))
            return False

        return False

##############################################################################

    def Run(self):
        PossibleDirections = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(PossibleDirections)
        while (len(self.CurrentList) > 0):
            for Tile in self.CurrentList:
                self.CurrentCoordinates = Tile
                for XY in PossibleDirections:
                    if (self.CheckTile(XY[0], XY[1])):
                        if (self.SearchingFor == "Exploring"):
                            return (self.CurrentCoordinates[0], self.CurrentCoordinates[1])
                        else:
                            return (self.CurrentCoordinates[0] + XY[0], self.CurrentCoordinates[1] + XY[1])
            
            self.CurrentList = self.TempList
            self.TempList = []
            
        return self.StartCoordinates