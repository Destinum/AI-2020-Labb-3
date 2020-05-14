from UnitClass import *

class Player:
    def __init__(self, StartingLocation, Map, DisplaySize):
        self.ExploredTiles = copy.deepcopy(Map)
        self.MapImage = pygame.Surface((DisplaySize[0], DisplaySize[1]))
        self.MapImage.fill((255, 255, 255))
        self.MapImage.convert()
        self.MapImageBaseWidth = self.MapImage.get_width()
        self.MapImageBaseHeight = self.MapImage.get_height()

        self.StartingLocation = (StartingLocation[0], StartingLocation[1])
        self.OreDumpLocation = self.StartingLocation
        self.WoodDumpLocation = (self.StartingLocation[0] + 4, self.StartingLocation[1] - 2)
        X = -1
        Y = -1

        while X < 2:
            while Y < 2:
                self.ExploredTiles[(StartingLocation[1] + Y)][(StartingLocation[0] + X)] = "Explored"
                TheWorld.DrawTile(self.MapImage, StartingLocation[0] + X, StartingLocation[1] + Y)
                Y += 1
            X += 1
            Y = -1

    Zoom = 1.0
    Units = []
    Artisans = 0
    Soldiers = 0
    ReadyToBuild = False
    MoveIronToBuildingLocation = False
    NextBuilding = "Charcoal Stack"
    ProduceSoldiers = False
    Buildings = {}
    Miners = 0
    Woodcutters = 0
    OreLocations = {}
    TreeLocations = []
    TreeListPerfectlySorted = False
    Resources = {"Wood" : 0, "Coal" : 0, "Iron Ore" : 0, "Iron" : 0, "Swords" : 0}

    UpgradingToSoldier = "NULL"

    def AddUnit(self, Unit):
        self.Units.append(Unit)
        Unit.ID = len(self.Units) - 1

    def Update(self):
        UpgradingToArtisan = False
        UpgradeToSoldier = True

        IronToMove = [0, "NULL", "NULL"]
        CoalToMove = [0, "NULL", "NULL"]
        WoodToMove = [0, "NULL", "NULL"]
        OreAvailable = True
        TreeAvailable = True

        if (self.Resources["Swords"] > 15 and self.ProduceSoldiers == False and self.NextBuilding == "NULL"):
            self.ProduceSoldiers = True

        if (self.NextBuilding == "Training Camp" and self.Resources["Swords"] > 10 and self.WoodDumpLocation != (self.StartingLocation[0] - 5, self.StartingLocation[1] - 6)):
            self.WoodDumpLocation = (self.StartingLocation[0] - 5, self.StartingLocation[1] - 6)
            if (self.ExploredTiles[self.WoodDumpLocation[1]][self.WoodDumpLocation[0]] != "Explored" and len(self.TreeLocations) > 0):
                self.WoodDumpLocation = BreadthFirst(self.WoodDumpLocation, self.ExploredTiles, "M").Run()

        if (TheWorld.Tiles[self.WoodDumpLocation[1]][self.WoodDumpLocation[0]][0] not in TheWorld.StructureTypes):
            WoodCount = 0
            IronCount = 0
            for TheResource in TheWorld.Tiles[self.WoodDumpLocation[1]][self.WoodDumpLocation[0]][1]:
                if (TheWorld.Tiles[self.WoodDumpLocation[1]][self.WoodDumpLocation[0]][1][TheResource] == "Wood"):
                    WoodCount += 1
                elif (TheWorld.Tiles[self.WoodDumpLocation[1]][self.WoodDumpLocation[0]][1][TheResource] == "Iron"):
                    IronCount += 1
            if (WoodCount >= 10 and self.Artisans <= len(self.Buildings)):
                if (self.NextBuilding != "Smithy" or (self.NextBuilding == "Smithy" and IronCount >= 3)):
                    UpgradingToArtisan = True
                    self.ReadyToBuild = True


        if (self.UpgradingToSoldier != "NULL" and self.Units[self.UpgradingToSoldier].State.StateName == "Idle"):
            self.UpgradingToSoldier = "NULL"

        ToSmithy = self.Resources["Iron"] + self.Resources["Swords"] >= 20 or self.Resources["Iron Ore"] < 2
        for TheBuilding in self.Buildings:
            if (self.Buildings[TheBuilding][0] == "Smithy"):
                IronToMove[1] = TheBuilding
            elif (self.Buildings[TheBuilding][0] != "Smithy" and TheWorld.Tiles[TheBuilding[1]][TheBuilding[0]][1]["Iron"] > 0):
                IronToMove[0] = TheWorld.Tiles[TheBuilding[1]][TheBuilding[0]][1]["Iron"]
                IronToMove[2] = TheBuilding
         
            if ((self.Buildings[TheBuilding][0] == "Smithy" and ToSmithy) or (self.Buildings[TheBuilding][0] == "Smeltery" and ToSmithy == False)):
                CoalToMove[1] = TheBuilding
            elif (self.Buildings[TheBuilding][0] == "Charcoal Stack" and TheWorld.Tiles[TheBuilding[1]][TheBuilding[0]][1]["Coal"] > 0):  
                CoalToMove[0] = TheWorld.Tiles[TheBuilding[1]][TheBuilding[0]][1]["Coal"]
                CoalToMove[2] = TheBuilding

            if (self.Buildings[TheBuilding][0] == "Charcoal Stack"):
                WoodToMove[1] = TheBuilding
            elif (self.Buildings[TheBuilding][0] != "Charcoal Stack" and TheWorld.Tiles[TheBuilding[1]][TheBuilding[0]][1]["Wood"] > 0):
                WoodToMove[0] = TheWorld.Tiles[TheBuilding[1]][TheBuilding[0]][1]["Wood"]
                WoodToMove[2] = TheBuilding

        for Unit in self.Units:

            if (Unit.Type == "Worker"):
                while (Unit.State.StateName == "Idle"):           
                    if (UpgradingToArtisan):
                        Unit.State = Upgrading("Artisan")
                        self.Artisans += 1
                        UpgradingToArtisan = False
                        break

                    if (UpgradeToSoldier):
                        UpgradeToSoldier = False
                        if (self.ProduceSoldiers and self.Resources["Swords"] > 0 and self.UpgradingToSoldier  == "NULL"):
                            BuildingWithSwords = "NULL"
                            for TheBuilding in self.Buildings:
                                if (self.Buildings[TheBuilding][0] == "Training Camp" and self.Buildings[TheBuilding][1] == "NULL"):
                                    Unit.DumpLocation = TheBuilding
                                if (TheWorld.Tiles[TheBuilding[1]][TheBuilding[0]][1]["Swords"] > 0):
                                    BuildingWithSwords = TheBuilding
                                if ("NULL" not in (Unit.DumpLocation, BuildingWithSwords)):
                                    self.Buildings[Unit.DumpLocation][1] = Unit.ID
                                    Unit.SetDestination(BuildingWithSwords, True)
                                    Unit.State = Moving(TakeFromBuilding("Swords", BuildingWithSwords), False)
                                    break
                            if (Unit.State.StateName != "Idle"):
                                self.UpgradingToSoldier = Unit.ID
                                break

                    if (IronToMove[0] > 0):
                        if (IronToMove[1] != "NULL"):
                            Unit.DumpLocation = IronToMove[1]
                        else:
                            Unit.DumpLocation = self.WoodDumpLocation              
                        Unit.SetDestination(IronToMove[2], True)
                        Unit.State = Moving(TakeFromBuilding("Iron", IronToMove[2]), False)
                        IronToMove[0] -= 1
                        break

                    elif (CoalToMove[0] > 0 and CoalToMove[1] != "NULL"):
                        Unit.DumpLocation = CoalToMove[1]
                        Unit.SetDestination(CoalToMove[2], True)
                        Unit.State = Moving(TakeFromBuilding("Coal", CoalToMove[2]), False)
                        CoalToMove[0] -= 1
                        break

                    elif (WoodToMove[0] > 0 and WoodToMove[1] != "NULL"):
                        Unit.DumpLocation = WoodToMove[1]
                        Unit.SetDestination(WoodToMove[2], True)
                        Unit.State = Moving(TakeFromBuilding("Wood", WoodToMove[2]), False)
                        WoodToMove[0] -= 1
                        break

                    if (OreAvailable):
                        FoundOre = False
                        for PotentialOre in self.OreLocations:
                            if (self.OreLocations[PotentialOre] == "Available"):
                                Unit.SetDestination((PotentialOre[0], PotentialOre[1]), False)
                                self.OreLocations[PotentialOre] = "Occupied"
                                Unit.DumpLocation = self.OreDumpLocation
                                Unit.State = Moving(Mining((PotentialOre[2], PotentialOre[3])), False)
                                FoundOre = True
                                break
                        OreAvailable = FoundOre   
                        if (Unit.State.StateName != "Idle"):
                            break
                    
                    if (TreeAvailable):
                        FoundTree = False
                        for TreeTile in self.TreeLocations:
                            for PotentialTree in TreeTile[2]:
                                if (TreeTile[2][PotentialTree] == "Available"):
                                    Unit.SetDestination(TreeTile[0], False)
                                    TreeTile[2][PotentialTree] = "Occupied"
                                    Unit.DumpLocation = self.WoodDumpLocation
                                    Unit.State = Moving(Woodcutting(PotentialTree), False)
                                    FoundTree = True
                                    break
                            if (FoundTree):
                                break
                        TreeAvailable = FoundTree
                    
                    break

            elif (Unit.Type == "Artisan" and Unit.State.StateName == "Idle"):
                if (self.ReadyToBuild):
                    Unit.SetDestination(self.WoodDumpLocation, True)
                    self.ReadyToBuild = False
                    if (self.NextBuilding == "Charcoal Stack"):
                        Unit.State = Moving(Building("Charcoal Stack", self.WoodDumpLocation, 60), False)
                        self.WoodDumpLocation = self.OreDumpLocation
                        self.NextBuilding = "Smeltery"
                    elif (self.NextBuilding == "Smeltery"):
                        Unit.State = Moving(Building("Smeltery", self.WoodDumpLocation, 120), False)
                        self.WoodDumpLocation = (self.StartingLocation[0], self.StartingLocation[1] - 4)
                        if (self.ExploredTiles[self.WoodDumpLocation[1]][self.WoodDumpLocation[0]] != "Explored" and len(self.TreeLocations) > 0):
                            self.WoodDumpLocation = BreadthFirst(self.WoodDumpLocation, self.ExploredTiles, "M").Run()
                        self.NextBuilding = "Smithy"
                        MoveIronToBuildingLocation = True
                    elif (self.NextBuilding == "Smithy"):
                        Unit.State = Moving(Building("Smithy", self.WoodDumpLocation, 180), False)
                        self.NextBuilding = "Training Camp"
                        for TheBuilding in self.Buildings:
                            if(self.Buildings[TheBuilding][0] == "Charcoal Stack"):
                                self.WoodDumpLocation = TheBuilding
                                break
                    elif (self.NextBuilding == "Training Camp"):
                        Unit.State = Moving(Building("Training Camp", self.WoodDumpLocation, 120), False)
                        self.NextBuilding = "NULL"
                        for TheBuilding in self.Buildings:
                            if(self.Buildings[TheBuilding][0] == "Charcoal Stack"):
                                self.WoodDumpLocation = TheBuilding
                                break
                else:
                    for TheBuilding in self.Buildings:
                        if (self.Buildings[TheBuilding][1] == "NULL" and self.Buildings[TheBuilding][0] != "Training Camp"):
                            if (self.Buildings[TheBuilding][0] == "Charcoal Stack"):
                                Unit.State = Moving(Coalmaking(TheBuilding), True)
                            elif (self.Buildings[TheBuilding][0] == "Smeltery"):
                                Unit.State = Moving(Smelting(TheBuilding), True)
                            elif (self.Buildings[TheBuilding][0] == "Smithy"):
                                 Unit.State = Moving(Smithing(TheBuilding), True)
                            Unit.SetDestination(TheBuilding, False)
                            self.Buildings[TheBuilding][1] = Unit.ID
                            break


            if (Unit.Type == "Explorer" and Unit.Pathfinding == False):
                Unit.State.Update(Unit)
            elif (Unit.Type != "Explorer"):
                Unit.State.Update(Unit)


    def InitialUpgrade(self):
        for i, Unit in enumerate(self.Units):
            if (i > 3):
                break
            Unit.State = Upgrading("Explorer")

    def SortTrees(self):
        self.TreeListPerfectlySorted = True
        TempList = []

        for TreeTile in self.TreeLocations:
            Distance = len(AStar(TreeTile[0], self.StartingLocation, self.ExploredTiles, False).Run()[0])

            Minimum = 0
            Maximum = len(TempList) - 1
            Index = int(len(TempList) / 2)
            if (Maximum > 0):
                while True:
                    if Distance < TempList[Index][1]:
                        Maximum = Index
                        Index = int(Index - (Index - Minimum) / 2)
                    elif Distance > TempList[Index][1]:
                        Minimum = Index
                        Index = int(Index + (Maximum - Index) / 2)
                    else:
                        break
                    if (Index in (Minimum, Maximum)):
                        Index = Maximum
                        break

            TempList.insert(Index, [TreeTile[0], Distance, TreeTile[2]])

        self.TreeLocations = TempList

        Index = 0
        while Index < len(self.TreeLocations):
            if (len(self.TreeLocations[Index][2]) == 0):
                self.TreeLocations.pop(Index)
            else:
                Index += 1