import pygame
import time
from WorldMap import *
from PlayerClass import *

DisplayWidth = 1000
DisplayHeight = 1000

pygame.init()
Window = pygame.display.set_mode((DisplayWidth, DisplayHeight))
pygame.display.set_caption("AI Labb 3")

"""
Map = open("KartaLaboration3.txt", "r")
lines = Map.readlines()
Map.close()

TheWorld = WorldMap(lines)
"""

#Fisk = int(4.2)
#Fisk2 = int(4.6)

#Tiles = []
#ExploredTiles = []
#ExploredTiles = [["Unknown"] * len(lines[0])] * len(lines)

CameraSpeed = 5
Zoom = 1.0
#TileSize = 100
#UnitSize = TileSize / 20

DisplacementX = (len(TheWorld.MapData[0]) - 1) * TheWorld.TileSize / 2
DisplacementY = (len(TheWorld.MapData) - 1) * TheWorld.TileSize / 2
#CenterPoint = [DisplacementX, DisplacementY]

CenterPoint = [int(DisplayWidth / 2), int(DisplayHeight / 2)]
StartNode = [50, 48]

#DisplacementX = - (DisplayWidth / 2)
#DisplacementY = - (DisplayHeight / 2)

#print(len(lines))

#Window.fill((255, 255, 255))
#Window.fill((0, 255, 0))

def DrawTile(xValue, yValue):
    
    letter = TheWorld.Tiles[yValue][xValue][0]
    Color = [255, 255, 255]

    if (letter == "M"):
        Color = [0, 255, 0]
    elif (letter == "T"):
        Color = [0, 100, 0]
    elif (letter == "V"):
        Color = [0, 0, 255]
    elif (letter == "G"):
        Color = [150, 0, 150]
    elif (letter == "B"):
        Color = [100, 100, 100]

    X = int(CenterPoint[0] + (TheWorld.TileSize * xValue - DisplacementX) * Zoom)
    Y = int(CenterPoint[1] + (TheWorld.TileSize * yValue - DisplacementY) * Zoom)
    pygame.draw.rect(Window, (Color[0], Color[1], Color[2]), (X, Y, int(TheWorld.TileSize * Zoom) + 1, int(TheWorld.TileSize * Zoom) + 1))

def DrawUnit(Unit):
    X = int(CenterPoint[0] + (TheWorld.TileSize * Unit.CurrentNode[0] + Unit.NodeCoordinates[0] - DisplacementX) * Zoom)
    Y = int(CenterPoint[1] + (TheWorld.TileSize * Unit.CurrentNode[1] + Unit.NodeCoordinates[1] - DisplacementY) * Zoom)
    pygame.draw.circle(Window, (Unit.Color[0], Unit.Color[1], Unit.Color[2]), (X, Y), int(TheWorld.UnitSize * Zoom))          


"""
for index, Row in enumerate(Tiles):
    if (index > 10 and index < 60):
        ExploredTiles[index] = ["Explored"] * len(lines[0])
"""


ThePlayer = Player([StartNode[0], StartNode[1]], TheWorld.ExploredTiles)
AbsoluteUnit = Explorer("Explorer", [StartNode[0], StartNode[1]], ThePlayer)


"""
Count = 0
while (Count < 5):
    Units.append(Explorer("Explorer", [StartNode[0], StartNode[1]]))
    Count += 1
"""

LastTime = time.process_time()
CurrentTime = time.process_time()
#TheTime = ""
Paused = False
UpdateRate = 0.01
Running = True

while Running:

    CurrentTime = time.process_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
            break
        
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE):
                Paused = not Paused
            if (event.key == pygame.K_KP_ENTER):
                try:
                    val = float(input("Enter new update rate per second: "))
                    #UpdateRate = 1.0 / val
                    Zoom = val
                except ValueError:
                    print("Couldn't convert input to usable value.")
            if (event.key == pygame.K_ESCAPE):
                Running = False
                break

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 4):
                Zoom *= 1.1
            elif (event.button == 5):
                Zoom /= 1.1

    if (Paused == False and (CurrentTime - LastTime) >= UpdateRate):

        Window.fill((255, 255, 255))

        Keys = pygame.key.get_pressed()
        if Keys[pygame.K_a]:
            CenterPoint[0] += CameraSpeed
        if Keys[pygame.K_d]:
            CenterPoint[0] -= CameraSpeed
        if Keys[pygame.K_w]:
            CenterPoint[1] += CameraSpeed
        if Keys[pygame.K_s]:
            CenterPoint[1] -= CameraSpeed


        for index, Row in enumerate(TheWorld.Tiles):
            for i, Tile in enumerate(Row):
                if (ThePlayer.ExploredTiles[index][i] == "Explored"):
                    DrawTile(i, index)
        """

        for index, line in enumerate(TheWorld.MapData):
            for i, letter in enumerate(line):
                DrawTile(i, index)
        
        """

        for Unit in ThePlayer.Units:
            Unit.Update()
            DrawUnit(Unit)

        LastTime = CurrentTime

    pygame.display.update()

pygame.quit()
#print("Session ended at " + TheTime)