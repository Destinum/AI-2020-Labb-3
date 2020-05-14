from WorldMap import *
from AStar import *
from BreadthFirst import *
import threading

class State:
    StateName = "Idle"

    def Update(self, TheUnit):
        #Does nothing
        return


class Upgrading(State):
    def  __init__(self, Type):
        self.UpgradingTo = Type
        if (Type == "Explorer" or Type == "Soldier"):
            self.Time = 60
        elif (Type == "Artisan"):
            self.Time = 120

    StateName = "Upgrading"

    def Update(self, TheUnit):
        self.Time -= 1
        if (self.Time <= 0):
            if (self.UpgradingTo == "Soldier"):
                if (TheUnit.Carrying == "Swords" and TheWorld.Tiles[TheUnit.CurrentNode[1]][TheUnit.CurrentNode[0]][0] == "Training Camp"):
                    for XY in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        if (TheWorld.Tiles[TheUnit.CurrentNode[1] + XY[1]][TheUnit.CurrentNode[0] + XY[0]][0] in ("M", "T", "G")):
                            TheUnit.Player.Buildings[(TheUnit.CurrentNode[0], TheUnit.CurrentNode[1])][1] = "NULL"
                            TheUnit.CurrentNode[0] = TheUnit.CurrentNode[0] + XY[0]
                            TheUnit.CurrentNode[1] = TheUnit.CurrentNode[1] + XY[1]
                            X = random.randrange(0, 10, 1)
                            Y = random.randrange(0, 10, 1)
                            TheUnit.NodeCoordinates = [X, Y]
                            break
                    TheUnit.ChangeType(self.UpgradingTo)
                    TheUnit.Player.Soldiers += 1
                else:
                    TheUnit.State = State()

            else:
                TheUnit.ChangeType(self.UpgradingTo)


class Exploring(State):
    def __init__(self, TheUnit):
        self.Explore(TheUnit)

    StateName = "Exploring"

    def Update(self, TheUnit):
        if (TheUnit.Move()):
            TheUnit.Pathfinding = True
            TheThread = threading.Thread(target=self.Explore, args=(TheUnit,))
            TheThread.start()
            #self.Explore(TheUnit)

    def Explore(self, TheUnit):
        for X in (-1, 0, 1):
            for Y in (-1, 0, 1):
                TheNode = (TheUnit.CurrentNode[0] + X, TheUnit.CurrentNode[1] + Y)
                TheUnit.Player.ExploredTiles[TheNode[1]][TheNode[0]] = "Explored"
                TheWorld.DrawTile(TheUnit.Player.MapImage, TheNode[0], TheNode[1])
                
                AddTreeTile = True
                TileInTreeList = "NULL"
                if (TheWorld.Tiles[TheNode[1]][TheNode[0]][0] == "T"):
                    for TreeTile in TheUnit.Player.TreeLocations:
                        if TreeTile[0] == TheNode:
                            AddTreeTile = False
                            TileInTreeList = TreeTile
                            break

                for SpecialTile in TheWorld.Tiles[TheNode[1]][TheNode[0]][1]:
                    TheTile = (TheUnit.CurrentNode[0] + X, TheUnit.CurrentNode[1] + Y, SpecialTile[0], SpecialTile[1])
                    if (TheWorld.Tiles[TheNode[1]][TheNode[0]][1][SpecialTile] == "Iron Ore" and (TheTile not in TheUnit.Player.OreLocations)):
                        TheUnit.Player.OreLocations[TheTile] = "Available"
                    elif (TheWorld.Tiles[TheNode[1]][TheNode[0]][1][SpecialTile] == "Tree" and AddTreeTile):
                        if (TileInTreeList == "NULL"):
                            Distance = abs(TheUnit.Player.WoodDumpLocation[0] - TheNode[0]) + abs(TheUnit.Player.WoodDumpLocation[1] - TheNode[1])
                            #Distance = len(AStar(TheTile, TheUnit.Player.WoodDumpLocation, TheUnit.Player.ExploredTiles, False).Run()[0])

                            Minimum = 0
                            Maximum = len(TheUnit.Player.TreeLocations) - 1
                            Index = int(len(TheUnit.Player.TreeLocations) / 2)
                            if (Maximum > 0):
                                while True:
                                    if Distance < TheUnit.Player.TreeLocations[Index][1]:
                                        Maximum = Index
                                        Index = int(Index - (Index - Minimum) / 2)
                                    elif Distance > TheUnit.Player.TreeLocations[Index][1]:
                                        Minimum = Index
                                        Index = int(Index + (Maximum - Index) / 2)
                                    else:
                                        break
                                    if (Index in (Minimum, Maximum)):
                                        Index = Maximum
                                        break

                            if (TheUnit.Player.ExploredTiles[TheUnit.Player.WoodDumpLocation[1]][TheUnit.Player.WoodDumpLocation[0]] != "Explored"):
                                TheUnit.Player.WoodDumpLocation = BreadthFirst(TheUnit.Player.WoodDumpLocation, TheUnit.Player.ExploredTiles, "M").Run()
                            TheUnit.Player.TreeLocations.insert(Index, [TheNode, Distance, {}])
                            TileInTreeList = TheUnit.Player.TreeLocations[Index]
                        TileInTreeList[2][SpecialTile] = "Available"

        TheUnit.SetDestination()
        TheUnit.Pathfinding = False



class Moving(State):
    def  __init__(self, NextState, MovingToBuilding):
        self.NextState = NextState
        self.MovingToBuilding =  MovingToBuilding

    StateName = "Moving"

    def Update(self, TheUnit):
        if (len(TheUnit.WalkPath[0]) == 0):
            TheUnit.State = self.NextState
            if (self.MovingToBuilding):
                if (TheUnit.State.StateName == "Upgrading"):
                    TheUnit.CurrentNode[0] = TheUnit.DumpLocation[0]
                    TheUnit.CurrentNode[1] = TheUnit.DumpLocation[1]
                else:
                    TheUnit.CurrentNode[0] = TheUnit.State.Building[0]
                    TheUnit.CurrentNode[1] = TheUnit.State.Building[1]
                TheUnit.NodeCoordinates = [5, 5]
        else:
            TheUnit.Move()


class Transporting(State):

    StateName = "Transporting"

    def Update(self, TheUnit):
        if (TheWorld.Tiles[TheUnit.DumpLocation[1]][TheUnit.DumpLocation[0]][0] in TheWorld.StructureTypes):
            TheWorld.Tiles[TheUnit.DumpLocation[1]][TheUnit.DumpLocation[0]][1][TheUnit.Carrying] += 1
            TheUnit.Player.Resources[TheUnit.Carrying] += 1
            TheUnit.Carrying = "NULL"

        else:
            DumpLocation = (random.randrange(0, 10, 1), random.randrange(0, 10, 1))
            while (DumpLocation in TheWorld.Tiles[TheUnit.CurrentNode[1]][TheUnit.CurrentNode[0]][1]):
                DumpLocation = (random.randrange(0, 10, 1), random.randrange(0, 10, 1))
            TheUnit.PutDown(DumpLocation)

        TheUnit.State = State()
        TheUnit.DumpLocation = "NULL"

class TakeFromBuilding(State):
    def  __init__(self, ResourceType, TargetBuilding):
        self.ResourceType = ResourceType
        self.TargetBuilding = TargetBuilding

    StateName = "Taking from Building"

    def Update(self, TheUnit):
        if (TheWorld.Tiles[self.TargetBuilding[1]][self.TargetBuilding[0]][1][self.ResourceType] > 0):
            TheWorld.Tiles[self.TargetBuilding[1]][self.TargetBuilding[0]][1][self.ResourceType] -= 1
            TheUnit.Carrying = self.ResourceType
            TheUnit.Player.Resources[self.ResourceType] -= 1
            TheUnit.SetDestination(TheUnit.DumpLocation, False)
            if (TheWorld.Tiles[TheUnit.DumpLocation[1]][TheUnit.DumpLocation[0]][0] == "Training Camp"):
                TheUnit.State = Moving(Upgrading("Soldier"), True)
            else:
                TheUnit.State = Moving(Transporting(), False)
        else:
            TheUnit.State = State()
            TheUnit.DumpLocation = "NULL"

class Mining(State):
    def  __init__(self, OreCoordinate):
        self.OreCoordinate = OreCoordinate

    StateName = "Mining"

    def Update(self, TheUnit):
        if (TheUnit.NodeCoordinates[0] + 1 < self.OreCoordinate[0]):
            TheUnit.NodeCoordinates[0] += 1
        elif (TheUnit.NodeCoordinates[0] - 1 > self.OreCoordinate[0]):
            TheUnit.NodeCoordinates[0] -= 1
        elif (TheUnit.NodeCoordinates[1] + 1 < self.OreCoordinate[1]):
            TheUnit.NodeCoordinates[1] += 1
        elif (TheUnit.NodeCoordinates[1] - 1 > self.OreCoordinate[1]):
            TheUnit.NodeCoordinates[1] -= 1

        else:
            TheUnit.Pickup(self.OreCoordinate)
            del TheUnit.Player.OreLocations[(TheUnit.CurrentNode[0], TheUnit.CurrentNode[1], self.OreCoordinate[0], self.OreCoordinate[1])]
            TheUnit.SetDestination(TheUnit.DumpLocation, False)
            TheUnit.State = Moving(Transporting(), False)


class Woodcutting(State):
    def  __init__(self, TreeCoordinate):
        self.TreeCoordinate = TreeCoordinate

    StateName = "Woodcutting"
    ChoppingTime = 30

    def Update(self, TheUnit):
        if (TheUnit.NodeCoordinates[0] + 1 < self.TreeCoordinate[0]):
            TheUnit.NodeCoordinates[0] += 1
        elif (TheUnit.NodeCoordinates[0] - 1 > self.TreeCoordinate[0]):
            TheUnit.NodeCoordinates[0] -= 1
        elif (TheUnit.NodeCoordinates[1] + 1 < self.TreeCoordinate[1]):
            TheUnit.NodeCoordinates[1] += 1
        elif (TheUnit.NodeCoordinates[1] - 1 > self.TreeCoordinate[1]):
            TheUnit.NodeCoordinates[1] -= 1

        else:
            self.ChoppingTime -= 1

            if (self.ChoppingTime <= 0):
                TheWorld.Tiles[TheUnit.CurrentNode[1]][TheUnit.CurrentNode[0]][1][self.TreeCoordinate] = "Wood"
                TheUnit.Pickup(self.TreeCoordinate)
                for TreeTile in TheUnit.Player.TreeLocations:
                    if TreeTile[0] == (TheUnit.CurrentNode[0], TheUnit.CurrentNode[1]):
                        del TreeTile[2][self.TreeCoordinate]
                        if (len(TreeTile[2]) == 0):
                            TheUnit.Player.TreeLocations.remove(TreeTile)
                        break

                TheUnit.SetDestination(TheUnit.DumpLocation, False)
                TheUnit.State = Moving(Transporting(), False)


class Building(State):
    def  __init__(self, Building, BuildLocation, BuildingTime):
        self.Building = Building
        self.BuildLocation = BuildLocation
        self.BuildingTime = BuildingTime

    StateName = "Building"

    def Update(self, TheUnit):
        self.BuildingTime -= 1

        if (self.BuildingTime <= 0):
            TheWorld.Tiles[self.BuildLocation[1]][self.BuildLocation[0]][0] = self.Building
            TempList = {"Wood" : -10, "Coal" : 0, "Iron Ore" : 0, "Iron" : 0, "Swords" : 0}
            TheUnit.Player.Resources["Wood"] -= 10
            if (self.Building == "Smithy"):
                TempList["Iron"] = -3
                TheUnit.Player.Resources["Iron"] -= 3

            for Resource in TheWorld.Tiles[self.BuildLocation[1]][self.BuildLocation[0]][1]:
                ResourceType = TheWorld.Tiles[self.BuildLocation[1]][self.BuildLocation[0]][1][Resource]
                TempList[ResourceType] += 1
                TheUnit.Player.Resources[ResourceType] += 1

            TheWorld.Tiles[self.BuildLocation[1]][self.BuildLocation[0]][1] = TempList

            UnitsWithThisAsDumpLocation = 0
            for Unit in TheUnit.Player.Units:
                if Unit.Type == "Worker" and Unit.DumpLocation == self.BuildLocation:
                    UnitsWithThisAsDumpLocation += 1
            TheUnit.Player.Buildings[self.BuildLocation] = [self.Building, "NULL"]
            TheWorld.DrawTile(TheUnit.Player.MapImage, self.BuildLocation[0], self.BuildLocation[1])
            TheUnit.State = State()


class Coalmaking(State):
    def  __init__(self, Building):
        self.Building = Building

    StateName = "Coalmaking"
    ProductionTime = 0

    def Update(self, TheUnit):

        if (self.ProductionTime > 0):
            self.ProductionTime -= 1
            if (self.ProductionTime == 0 and TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Wood"] >= 2):
                TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Wood"] -= 2
                TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Coal"] += 1
                TheUnit.Player.Resources["Wood"] -= 2
                TheUnit.Player.Resources["Coal"] += 1

        elif (TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Wood"] >= 2):
            self.ProductionTime = 30


class Smelting(State):
    def  __init__(self, Building):
        self.Building = Building

    StateName = "Smelting"
    ProductionTime = 0

    def Update(self, TheUnit):

        if (self.ProductionTime > 0):
            self.ProductionTime -= 1
            if (self.ProductionTime == 0 and TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Coal"] >= 3 and TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Iron Ore"] >= 2):
                TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Coal"] -= 3
                TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Iron Ore"] -= 2
                TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Iron"] += 1
                TheUnit.Player.Resources["Coal"] -= 3
                TheUnit.Player.Resources["Iron Ore"] -= 2
                TheUnit.Player.Resources["Iron"] += 1

        elif (TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Coal"] >= 3 and TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Iron Ore"] >= 2):
            self.ProductionTime = 30

class Smithing(State):
    def  __init__(self, Building):
        self.Building = Building

    StateName = "Smithing"
    ProductionTime = 0

    def Update(self, TheUnit):

        if (self.ProductionTime > 0):
            self.ProductionTime -= 1
            if (self.ProductionTime == 0 and TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Coal"] >= 2 and TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Iron"] >= 1):
                TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Coal"] -= 2
                TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Iron"] -= 1
                TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Swords"] += 1
                TheUnit.Player.Resources["Coal"] -= 2
                TheUnit.Player.Resources["Iron"] -= 1
                TheUnit.Player.Resources["Swords"] += 1

        elif (TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Coal"] >= 2 and TheWorld.Tiles[self.Building[1]][self.Building[0]][1]["Iron"] >= 1):
            self.ProductionTime = 60