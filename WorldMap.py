import pygame
import copy
import random

class WorldMap:
    def __init__(self, Map, TileSize):
        self.MapData = Map
        self.Tiles = []
        self.ExploredTiles = []
        self.TileSize = TileSize
        self.UnitSize = self.TileSize / 20
        self.StructureTypes = ("Charcoal Stack", "Smithy", "Smeltery", "Training Camp")

        for index, line in enumerate(self.MapData):
            self.ExploredTiles.append([])
            self.Tiles.append([])

            for i, letter in enumerate(line):
                self.ExploredTiles[index].append("Unknown")                #The Map is initially unknown by the player
                #self.ExploredTiles[index].append("Explored")                #The Map is known from the start by the player
                self.Tiles[index].append([letter, {}])

                if (letter == "T"):
                    Count = 0
                    while (Count < 5):
                        TreeLocation = (random.randrange(0, 10, 1), random.randrange(0, 10, 1))
                        while (TreeLocation in self.Tiles[index][i][1]):
                            TreeLocation = (random.randrange(0, 10, 1), random.randrange(0, 10, 1))
                        self.Tiles[index][i][1][TreeLocation] = "Tree"
                        Count += 1

        MapDimensions = (len(self.Tiles[0]) - 1, len(self.Tiles) - 1)

        Count = 0
        while Count < 60:
            IronTile = (random.randrange(0, MapDimensions[0], 1), random.randrange(0, MapDimensions[1], 1))
            while (self.Tiles[IronTile[1]][IronTile[0]][0] in ("V", "B")):
                IronTile = (random.randrange(0, MapDimensions[0], 1), random.randrange(0, MapDimensions[1], 1))

            IronLocation = (random.randrange(0, 10, 1), random.randrange(0, 10, 1))
            while (IronLocation in self.Tiles[IronTile[1]][IronTile[0]][1]):
                IronLocation = (random.randrange(0, 10, 1), random.randrange(0, 10, 1))

            self.Tiles[IronTile[1]][IronTile[0]][1][IronLocation] = "Iron Ore"

            Count += 1


    def DrawTile(self, DrawSurface, xValue, yValue):

        letter = self.Tiles[yValue][xValue][0]
        Color = [255, 255, 255]

        if (letter in ("M", "T")):
            Color = [255, 200, 100]
        elif (letter == "V"):
            Color = [0, 0, 255]
        elif (letter == "G"):
            Color = [150, 0, 150]
        elif (letter == "B"):
            Color = [100, 100, 100]
        elif (letter in self.StructureTypes):
            Color = [200, 200, 200]

        X = DrawSurface.get_width() / 100
        Y = DrawSurface.get_height() / 100
        
        #Plain image
        pygame.draw.rect(DrawSurface, (Color[0], Color[1], Color[2]), (xValue * X, yValue * Y, X, Y))
        
        #With visible grid
        #pygame.draw.rect(DrawSurface, (200, 200, 200), (xValue * X, yValue * Y, X, Y))
        #pygame.draw.rect(DrawSurface, (Color[0], Color[1], Color[2]), (xValue * X + 0.5, yValue * Y + 0.5, X - 1, Y - 1))

        if (letter not in self.StructureTypes):
            for ResourceLocation in self.Tiles[yValue][xValue][1]:
                if (self.Tiles[yValue][xValue][1][ResourceLocation] == "Tree"):
                    Color = [0, 200, 0]
                elif (self.Tiles[yValue][xValue][1][ResourceLocation] == "Wood"):
                    Color = [0, 100, 0]
                elif (self.Tiles[yValue][xValue][1][ResourceLocation] == "Iron Ore"):
                    Color = [200, 0, 0]
                elif (self.Tiles[yValue][xValue][1][ResourceLocation] == "Iron"):
                    Color = [100, 0, 0] 
                pygame.draw.rect(DrawSurface, (Color[0], Color[1], Color[2]), (xValue * X + ResourceLocation[0], yValue * Y + ResourceLocation[1], X / 10, Y / 10))




Map = open("KartaLaboration3.txt", "r")
lines = Map.readlines()
Map.close()

TheWorld = WorldMap(lines, 10)