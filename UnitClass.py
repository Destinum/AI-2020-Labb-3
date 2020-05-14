import random
from WorldMap import *
from AStar import *
from BreadthFirst import *
from States import *

class Unit:
    def __init__(self, Location, ThePlayer):
        self.CurrentNode = copy.deepcopy(Location)
        self.Player = ThePlayer
        self.ID = "NULL"
        ThePlayer.AddUnit(self)
        self.Direction = [0, 0]
        self.WalkPath = [[]]
        X = random.randrange(0, 10, 1)
        Y = random.randrange(0, 10, 1)
        self.NodeCoordinates = [int(X * TheWorld.TileSize / 10), int(Y * TheWorld.TileSize / 10)]
        self.DumpLocation = ThePlayer.WoodDumpLocation

    Type = "NULL"
    MovementSpeed = 1.0
    MoveThisFrame = True
    Color = [0, 0, 0]
    State = State()

    def SetDestination(self, Destination, WalkToAdjacentOfGoal):
        self.WalkPath = AStar(self.CurrentNode, Destination, self.Player.ExploredTiles, WalkToAdjacentOfGoal).Run()
        self.SetDirection()

    def SetDirection(self):
        if (len(self.WalkPath[0]) > 0):
            self.Direction[0] = self.WalkPath[0][0][0] - self.CurrentNode[0]
            self.Direction[1] = self.WalkPath[0][0][1] - self.CurrentNode[1]

    def Move(self):
        if (TheWorld.Tiles[self.CurrentNode[1]][self.CurrentNode[0]][0] == "G"):
            self.MoveThisFrame = not self.MoveThisFrame

        if (self.MoveThisFrame == False or len(self.WalkPath[0]) == 0):
            return False

        Movement = int(self.MovementSpeed)

        self.NodeCoordinates[0] += self.Direction[0] * Movement
        self.NodeCoordinates[1] += self.Direction[1] * Movement

        MoveToNewTile = False

        if (self.NodeCoordinates[0] >= TheWorld.TileSize or self.NodeCoordinates[0] < 0 or self.NodeCoordinates[1] >= TheWorld.TileSize or self.NodeCoordinates[1] < 0):
            if (len(self.WalkPath) == 1 or self.WalkPath[1] != "Next To" or len(self.WalkPath[0]) > 1):
                self.NodeCoordinates[0] -= self.Direction[0] * TheWorld.TileSize
                self.CurrentNode[0] += self.Direction[0]
                self.NodeCoordinates[1] -= self.Direction[1] * TheWorld.TileSize
                self.CurrentNode[1] += self.Direction[1]
            else:
                self.NodeCoordinates[0] -= self.Direction[0] * Movement
                self.NodeCoordinates[1] -= self.Direction[1] * Movement
            MoveToNewTile = True

        if (MoveToNewTile):
            self.WalkPath[0].pop(0)
            self.SetDirection()

        return MoveToNewTile


class Worker(Unit):
    Type = "Worker"
    Carrying = "NULL"

    def ChangeType(self, Type):
        if (Type == "Explorer"):
            self.Player.Units[self.ID] = Explorer(self.CurrentNode, self.NodeCoordinates, self.Player, self.ID)
        elif (Type == "Artisan"):
            self.Player.Units[self.ID] = Artisan(self.CurrentNode, self.NodeCoordinates, self.Player, self.ID)
        elif (Type == "Soldier"):
            self.Player.Units[self.ID] = Soldier(self.CurrentNode, self.NodeCoordinates, self.Player, self.ID)

    def Pickup(self, Coordinate):
        if (self.Carrying == "NULL"):
            self.Carrying = TheWorld.Tiles[self.CurrentNode[1]][self.CurrentNode[0]][1][Coordinate]
            del TheWorld.Tiles[self.CurrentNode[1]][self.CurrentNode[0]][1][Coordinate]
        else:
            CarriedObject = self.Carrying
            self.Carrying = TheWorld.Tiles[self.CurrentNode[1]][self.CurrentNode[0]][1][Coordinate]
            TheWorld.Tiles[self.CurrentNode[1]][self.CurrentNode[0]][1][Coordinate] = CarriedObject
        TheWorld.DrawTile(self.Player.MapImage, self.CurrentNode[0], self.CurrentNode[1])

    def PutDown(self, Coordinate):
        if (self.Carrying != "NULL"):
            TheWorld.Tiles[self.CurrentNode[1]][self.CurrentNode[0]][1][Coordinate] = self.Carrying
            TheWorld.DrawTile(self.Player.MapImage, self.CurrentNode[0], self.CurrentNode[1])
            self.Carrying = "NULL"

class Explorer(Unit):
    def __init__(self, Location, NodeCoordinates, ThePlayer, ID):
        self.CurrentNode = copy.deepcopy(Location)
        self.NodeCoordinates = copy.deepcopy(NodeCoordinates)
        self.Player = ThePlayer
        self.ID = ID
        self.Direction = [0, 0]
        self.WalkPath = [[]]
        self.State = Exploring(self)

    Type = "Explorer"
    Pathfinding = False

    def SetDestination(self):
        if (len(self.WalkPath[0]) == 0):
            NewDestination = BreadthFirst(self.CurrentNode, self.Player.ExploredTiles, "Exploring").Run()
            if (NewDestination[0] == self.CurrentNode[0] and NewDestination[1] == self.CurrentNode[1]):
                self.State = State()
                if (self.Player.TreeListPerfectlySorted == False):
                    self.Player.SortTrees()
                return
            self.WalkPath = AStar(self.CurrentNode, NewDestination, self.Player.ExploredTiles, False).Run()
            self.SetDirection()


class Soldier(Unit):
    def __init__(self, Location, NodeCoordinates, ThePlayer, ID):
        self.CurrentNode = copy.deepcopy(Location)
        self.Player = ThePlayer
        self.ID = ID
        self.Direction = [0, 0]
        self.WalkPath = [[]]
        self.NodeCoordinates = copy.deepcopy(NodeCoordinates)
    
    Type = "Soldier"

class Artisan(Unit):
    def __init__(self, Location, NodeCoordinates, ThePlayer, ID):
        self.CurrentNode = copy.deepcopy(Location)
        self.Player = ThePlayer
        self.ID = ID
        self.Direction = [0, 0]
        self.WalkPath = [[]]
        self.NodeCoordinates = copy.deepcopy(NodeCoordinates)

    Type = "Artisan"