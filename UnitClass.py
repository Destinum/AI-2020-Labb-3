import random
from WorldMap import *

class Unit:
    def __init__(self, TheType):
        self.Type = TheType

    MovementSpeed = 1.0

    def Update(self):
        print("Nothing to Update")


class Explorer(Unit):
    def __init__(self, TheType, Location, ThePlayer):
        self.Type = TheType
        self.CurrentNode = Location
        self.Player = ThePlayer
        ThePlayer.AddUnit(self)

        #self.Direction = [random.randrange(-1, 2, 1), random.randrange(-1, 2, 1)]
        self.Direction = [random.randrange(-1, 2, 2), 0]
        X = random.randrange(0, 10, 1)
        Y = random.randrange(0, 10, 1)
        self.NodeCoordinates = [int(X * TheWorld.TileSize / 10), int(Y * TheWorld.TileSize / 10)]

    Color = [255, 0, 0]
    #NodeCoordinates = [5, 5]

    def Update(self):
        #self.RandomMove()
        self.Move()
        #self.Explore(self.CurrentNode[0], self.CurrentNode[1])

    def Move(self):
        Movement = int(TheWorld.TileSize / 10 * self.MovementSpeed)

        self.NodeCoordinates[0] += self.Direction[0] * Movement
        self.NodeCoordinates[1] += self.Direction[1] * Movement

        Exploring = False

        if (self.NodeCoordinates[0] >= TheWorld.TileSize):
            self.NodeCoordinates[0] = self.NodeCoordinates[0] - TheWorld.TileSize
            self.CurrentNode[0] += 1
            Exploring = True
        elif (self.NodeCoordinates[0] < 0):
            self.NodeCoordinates[0] = TheWorld.TileSize + self.NodeCoordinates[0]
            self.CurrentNode[0] -= 1
            Exploring = True
        if (self.NodeCoordinates[1] >= TheWorld.TileSize):
            self.NodeCoordinates[1] = self.NodeCoordinates[1] - TheWorld.TileSize
            self.CurrentNode[1] += 1
            Exploring = True
        elif (self.NodeCoordinates[1] < 0):
            self.NodeCoordinates[1] = TheWorld.TileSize + self.NodeCoordinates[1]
            self.CurrentNode[1] -= 1
            Exploring = True

        if (Exploring):
            self.Explore(self.CurrentNode[0], self.CurrentNode[1])

        self.CheckNextTile()

    def CheckNextTile(self):
        NextTile = TheWorld.Tiles[self.CurrentNode[1] + self.Direction[1]][self.CurrentNode[0] + self.Direction[0]]
        if (NextTile[0] == "V" or NextTile[0] == "B" or (self.Direction[0] == 0 and self.Direction[1] == 0) or (self.Direction[0] != 0 and self.Direction[1] != 0)):
            self.Direction = [random.randrange(-1, 2, 1), random.randrange(-1, 2, 1)]
            #self.Direction = [random.randrange(-1, 2, 2), 0]
            """
            if (self.Direction[0] == 1):
                self.Direction = [0, 1]
            elif (self.Direction[1] == 1):
                self.Direction = [-1, 0]
            elif (self.Direction[0] == -1):
                self.Direction = [0, -1]
            elif (self.Direction[1] == -1):
                self.Direction = [1, 0]
            """
            self.CheckNextTile()

    def RandomMove(self):
        X = random.randrange(-1, 2, 1)
        Y = random.randrange(-1, 2, 1)

        Movement = int(TheWorld.TileSize / 10 * self.MovementSpeed)

        self.NodeCoordinates[0] += X * Movement
        self.NodeCoordinates[1] += Y * Movement

        Exploring = False

        if (self.NodeCoordinates[0] >= TheWorld.TileSize):
            self.NodeCoordinates[0] = self.NodeCoordinates[0] - TheWorld.TileSize
            self.CurrentNode[0] += 1
            Exploring = True
        elif (self.NodeCoordinates[0] < 0):
            self.NodeCoordinates[0] = TheWorld.TileSize + self.NodeCoordinates[0]
            self.CurrentNode[0] -= 1
            Exploring = True
        if (self.NodeCoordinates[1] >= TheWorld.TileSize):
            self.NodeCoordinates[1] = self.NodeCoordinates[1] - TheWorld.TileSize
            self.CurrentNode[1] += 1
            Exploring = True
        elif (self.NodeCoordinates[1] < 0):
            self.NodeCoordinates[1] = TheWorld.TileSize + self.NodeCoordinates[1]
            self.CurrentNode[1] -= 1
            Exploring = True

        if (Exploring):
            self.Explore(self.CurrentNode[0], self.CurrentNode[1])

    def Explore(self, xValue, yValue):
        #"""
        X = -1
        Y = -1

        while X < 2:
            while Y < 2:
                #print(ExploredTiles[yValue + Y][xValue + X])
                self.Player.ExploredTiles[(yValue + Y)][(xValue + X)] = "Explored"
                Y += 1
            X += 1
            Y = -1
        #"""
        #ExploredTiles[(yValue)][(xValue)] = "Explored"