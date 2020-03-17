import pygame
import time
import copy
from WorldMap import *

class BreadthFirst:
    def __init__(self, StartCoordinates, FogMap):
        self.CurrentList = []
        self.TempList = []
        self.CurrentCoordinates = StartCoordinates
        self.CurrentList.append(self.CurrentCoordinates)
        self.FogMap = copy.deepcopy(FogMap)
        self.FogMap[self.CurrentCoordinates[1]][self.CurrentCoordinates[0]] = "Visited"
        #Tiles[self.CurrentCoordinates[1]][self.CurrentCoordinates[0]][5] = "Visited"


    def CheckTile(self, BaseX, BaseY):
        X = BaseX + self.CurrentCoordinates[0]
        Y = BaseY + self.CurrentCoordinates[1]

        if (self.FogMap[Y][X] == "Unknown"):
            #Tiles[Y][X][4] = self.CurrentCoordinates
            #self.CurrentCoordinates = [X, Y]
            return True

        #elif (Tiles[Y][X][0] != "X" and Tiles[Y][X][5] != "Visited"):
        elif (self.FogMap[Y][X] != "Visited"):
            self.FogMap[Y][X] = "Visited"
            
            if (BaseX != 0 and BaseY != 0):
                #return False
                #if (TheWorld.Tiles[Y][self.CurrentCoordinates[0]][0] == "X" or TheWorld.Tiles[self.CurrentCoordinates[1]][X][0] == "X"):
                if (TheWorld.Tiles[Y][self.CurrentCoordinates[0]][0] in ("V", "B") or TheWorld.Tiles[self.CurrentCoordinates[1]][X][0] in ("V", "B")):
                    return False
                self.TempList.append([X, Y])
            else:
                self.TempList.insert(0, [X, Y])

            #Tiles[Y][X][4] = self.CurrentCoordinates
            #self.FogMap[Y][X] = "Visited"
            #pygame.draw.rect(Window, (200, 0, 255), (int(Displacement[1][0] - DisplacementX + TileSize * X + SmallTile / 2), int(Displacement[1][1] - DisplacementY + TileSize * Y + SmallTile / 2), SmallTile, SmallTile))


            return False

        return False


    def Run(self):
        #while (self.FogMap[self.CurrentCoordinates[1]][self.CurrentCoordinates[0]] != "Unknown"):
        while (len(self.CurrentList) > 0):
            #Breaker = False

            for Tile in self.CurrentList:
                self.CurrentCoordinates = Tile
                X = -1
                Y = -1

                while X < 2:
                    while Y < 2:         
                        if (self.CheckTile(X, Y)):
                            Y = 1
                            X = 1
                            #Breaker = True
                            return CurrentCoordinates
                        Y += 1
                    X += 1
                    Y = -1

                """
                if (Breaker):
                    break
                """
            """
            self.CurrentList = self.TempList
            self.TempList = []
            """
        return CurrentCoordinates                   #This is an actual line of code, not commented out
        """
        while (self.CurrentCoordinates != StartCoordinates):
            pygame.draw.rect(Window, (255, 0, 0), (int(Displacement[1][0] - DisplacementX + TileSize * self.CurrentCoordinates[0] + SmallTile / 2), int(Displacement[1][1] - DisplacementY + TileSize * self.CurrentCoordinates[1] + SmallTile / 2), SmallTile, SmallTile))
            self.CurrentCoordinates = Tiles[self.CurrentCoordinates[1]][self.CurrentCoordinates[0]][4]
        pygame.draw.rect(Window, (255, 0, 0), (int(Displacement[1][0] - DisplacementX + TileSize * self.CurrentCoordinates[0] + SmallTile / 2), int(Displacement[1][1] - DisplacementY + TileSize * self.CurrentCoordinates[1] + SmallTile / 2), SmallTile, SmallTile))
        """
