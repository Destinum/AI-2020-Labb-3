import pygame
import time
from WorldMap import *

class AStar:
    def __init__(self, StartCoordinates, GoalCoordinates, Tiles):
        self.OpenList = []
        self.ClosedList = []
        self.CurrentCoordinates = StartCoordinates
        self.Destination = GoalCoordinates
        self.TheTileSystem = Tiles

        TotalDistance = self.DistanceToGoal(StartCoordinates[0], StartCoordinates[1])
        self.TheTileSystem[StartCoordinates[1]][StartCoordinates[0]] = ["S", 0, TotalDistance, TotalDistance, "NULL", "Unknown"]
        self.ClosedList.append([StartCoordinates[0], StartCoordinates[1]])

    def DistanceToGoal(self, X, Y):
        xDistance = abs(self.Destination[0] - X)
        yDistance = abs(self.Destination[1] - Y)
        TotalDistance = abs(xDistance - yDistance) * 10
        if (xDistance > yDistance):
            TotalDistance += (xDistance - abs(xDistance - yDistance)) * 14
        else:
            TotalDistance += (yDistance - abs(xDistance - yDistance)) * 14
        return TotalDistance


    def CheckTile(self, BaseX, BaseY):
        X = BaseX + self.CurrentCoordinates[0]
        Y = BaseY + self.CurrentCoordinates[1]

        for Closed in self.ClosedList:
            if (Closed == [X, Y]):
                return False

        if (Tiles[Y][X][0] != "X"):
            DistanceToStart = Tiles[self.CurrentCoordinates[1]][self.CurrentCoordinates[0]][1] + 10

            if (BaseX != 0 and BaseY != 0):
                if (Tiles[Y][self.CurrentCoordinates[0]][0] != "X" and Tiles[self.CurrentCoordinates[1]][X][0] != "X"):
                    DistanceToStart += 4
                else:
                    return False

            for Open in self.OpenList:
                if (Open == [X, Y]):
                    if (DistanceToStart < Tiles[Y][X][1]):
                        Tiles[Y][X][1] = DistanceToStart
                        Tiles[Y][X][3] = Tiles[Y][X][1] + Tiles[Y][X][2]
                        Tiles[Y][X][4] = self.CurrentCoordinates
                    return True

            Tiles[Y][X][1] = DistanceToStart
            Tiles[Y][X][2] = self.DistanceToGoal(X, Y)
            Tiles[Y][X][3] = Tiles[Y][X][1] + Tiles[Y][X][2]
            Tiles[Y][X][4] = self.CurrentCoordinates
            self.OpenList.append([X, Y])
            return True

        return False

    def Run(self):
        while (Tiles[self.CurrentCoordinates[1]][self.CurrentCoordinates[0]][0] != "G"):
            X = -1
            Y = -1

            while X < 2:
                while Y < 2:         
                    self.CheckTile(X, Y)
                    Y += 1
                X += 1
                Y = -1

            ShortestTotal = float('inf')
            for Open in self.OpenList:
                if (Tiles[Open[1]][Open[0]][3] < ShortestTotal or (Tiles[Open[1]][Open[0]][3] == ShortestTotal and Tiles[Open[1]][Open[0]][2] < Tiles[self.CurrentCoordinates[1]][self.CurrentCoordinates[0]][2])):
                    self.CurrentCoordinates = Open
                    ShortestTotal = Tiles[Open[1]][Open[0]][3]

            pygame.draw.rect(Window, (200, 0, 255), (int(Displacement[0][0] - DisplacementX + TileSize * self.CurrentCoordinates[0] + SmallTile / 2), int(Displacement[0][1] - DisplacementY + TileSize * self.CurrentCoordinates[1] + SmallTile / 2), SmallTile, SmallTile))
            self.OpenList.remove(self.CurrentCoordinates)
            self.ClosedList.append(self.CurrentCoordinates)

            
            #pygame.draw.rect(Window, (255, 255, 255), ((Location[0] - DisplacementX + TileSize * i), (Location[1] - DisplacementY + TileSize * index), TileSize - 1, TileSize - 1))
            #DisplacementX = (len(lines[0]) - 1) * TileSize / 2
            #DisplacementY = len(lines) * TileSize / 2



        while (self.CurrentCoordinates != StartCoordinates):
            pygame.draw.rect(Window, (255, 0, 0), (int(Displacement[0][0] - DisplacementX + TileSize * self.CurrentCoordinates[0] + SmallTile / 2), int(Displacement[0][1] - DisplacementY + TileSize * self.CurrentCoordinates[1] + SmallTile / 2), SmallTile, SmallTile))
            self.CurrentCoordinates = Tiles[self.CurrentCoordinates[1]][self.CurrentCoordinates[0]][4]
        pygame.draw.rect(Window, (255, 0, 0), (int(Displacement[0][0] - DisplacementX + TileSize * self.CurrentCoordinates[0] + SmallTile / 2), int(Displacement[0][1] - DisplacementY + TileSize * self.CurrentCoordinates[1] + SmallTile / 2), SmallTile, SmallTile))
