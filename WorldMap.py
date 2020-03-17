class WorldMap:
    def __init__(self, Map, TileSize):
        self.MapData = Map
        self.Tiles = []
        self.ExploredTiles = []
        self.TileSize = TileSize
        self.UnitSize = self.TileSize / 20

        for index, line in enumerate(self.MapData):
            self.ExploredTiles.append([])
            self.Tiles.append([])

            for i, letter in enumerate(line):
                self.ExploredTiles[index].append("Unknown")
                self.Tiles[index].append([letter, float('inf'), float('inf'), float('inf'), "NULL", "Unknown"])
                #DrawTile(i, index)
                """
                #if (letter == "M"):
                    #pygame.draw.rect(Window, (0, 255, 0), (int(TileSize * i - DisplacementX), int(TileSize * index - DisplacementY), TileSize, TileSize))
                if (letter == "T"):
                    pygame.draw.rect(Window, (0, 100, 0), (int(TileSize * i - DisplacementX), int(TileSize * index - DisplacementY), TileSize, TileSize))
                elif (letter == "V"):
                    pygame.draw.rect(Window, (0, 0, 255), (int(TileSize * i - DisplacementX), int(TileSize * index - DisplacementY), TileSize, TileSize))
                elif (letter == "G"):
                    pygame.draw.rect(Window, (150, 0, 150), (int(TileSize * i - DisplacementX), int(TileSize * index - DisplacementY), TileSize, TileSize))
                elif (letter == "B"):
                    pygame.draw.rect(Window, (100, 100, 100), (int(TileSize * i - DisplacementX), int(TileSize * index - DisplacementY), TileSize, TileSize))
                """



Map = open("KartaLaboration3.txt", "r")
lines = Map.readlines()
Map.close()

TheWorld = WorldMap(lines, 10)