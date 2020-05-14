import pygame
import time
from WorldMap import *

class AStar:
    def __init__(self, StartCoordinates, Destination, ExploredMap, WalkToAdjacentOfGoal):
        self.OpenList = {}
        self.ClosedList = {}
        self.ExploredMap = ExploredMap
        self.WalkToAdjacentOfGoal = WalkToAdjacentOfGoal

        self.CurrentCoordinates = (StartCoordinates[0], StartCoordinates[1])
        self.StartCoordinates = (StartCoordinates[0], StartCoordinates[1])
        self.Destination = Destination

        TotalDistance = self.DistanceToGoal(StartCoordinates[0], StartCoordinates[1])
        self.ClosedList[self.StartCoordinates] = [0, TotalDistance, TotalDistance, "NULL"]

##############################################################################

    def DistanceToGoal(self, X, Y):
        xDistance = abs(self.Destination[0] - X)
        yDistance = abs(self.Destination[1] - Y)
        return (xDistance + yDistance)

##############################################################################

    def CheckTile(self, BaseX, BaseY):

        X = BaseX + self.CurrentCoordinates[0]
        Y = BaseY + self.CurrentCoordinates[1]

        if ((X, Y) in self.ClosedList):
            return False

        UnwalkableTile = TheWorld.Tiles[Y][X][0] not in ("M", "T", "G") or self.ExploredMap[Y][X] == "Unknown"

        if ((X, Y) == self.Destination and UnwalkableTile):
            self.WalkToAdjacentOfGoal = True

        if (UnwalkableTile == False or (self.WalkToAdjacentOfGoal and (X, Y) == self.Destination)):

            DistanceToStart = self.ClosedList[self.CurrentCoordinates][0] + 1

            if(TheWorld.Tiles[Y][X][0] == "G"):
                DistanceToStart += 1

            if ((X, Y) in self.OpenList):
                if (DistanceToStart < self.OpenList[(X, Y)][1]):
                    self.OpenList[(X, Y)][0] = DistanceToStart
                    self.OpenList[(X, Y)][2] = self.OpenList[(X, Y)][1] + self.OpenList[(X, Y)][2]
                    self.OpenList[(X, Y)][3] = self.CurrentCoordinates
                return True

            self.OpenList[(X, Y)] = [DistanceToStart, self.DistanceToGoal(X, Y), (DistanceToStart + self.DistanceToGoal(X, Y)), self.CurrentCoordinates]
            return True

        return False

##############################################################################

    def Run(self):
        Path = [[]]

        while (self.CurrentCoordinates != self.Destination):
            
            for XY in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                self.CheckTile(XY[0], XY[1])

            ShortestTotal = float('inf')
            for Open in self.OpenList:
                if (self.OpenList[Open][2] < ShortestTotal or (self.OpenList[Open][2] == ShortestTotal and self.OpenList[Open][1] < self.OpenList[self.CurrentCoordinates][1])):
                    self.CurrentCoordinates = Open
                    ShortestTotal = self.OpenList[Open][2]

            self.ClosedList[self.CurrentCoordinates] = self.OpenList[self.CurrentCoordinates]
            del self.OpenList[self.CurrentCoordinates]

        if (self.WalkToAdjacentOfGoal):
            Path.append("Next To")

        while (self.CurrentCoordinates != self.StartCoordinates):
            Path[0].insert(0, self.CurrentCoordinates)
            self.CurrentCoordinates = self.ClosedList[self.CurrentCoordinates][3]

        if (len(Path[0]) == 0):
            if (self.WalkToAdjacentOfGoal):
                for XY in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    self.CheckTile(XY[0], XY[1])
                    X = XY[0] + self.CurrentCoordinates[0]
                    Y = XY[1] + self.CurrentCoordinates[1]
                    UnwalkableTile = TheWorld.Tiles[Y][X][0] not in ("M", "T", "G") or self.ExploredMap[Y][X] == "Unknown"
                    if (UnwalkableTile == False):
                        Path[0].append((X, Y))
                        break

            Path[0].append(self.CurrentCoordinates)

        return Path
