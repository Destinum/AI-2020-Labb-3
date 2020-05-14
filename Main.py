import pygame
import time
from WorldMap import *
from PlayerClass import *

DisplaySize = (1000, 1000)

pygame.init()
Window = pygame.display.set_mode((DisplaySize[0], DisplaySize[1]))
pygame.display.set_caption("AI Labb 3")

def text_object(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()
TextSize = 3
TextFont = pygame.font.Font('freesansbold.ttf', TextSize)

LargeTextSize = 20
LargeTextFont = pygame.font.Font('freesansbold.ttf', LargeTextSize)
DisplayUnitInfo = False
DisplayBuildingInfo = False

CameraSpeed = 5

CenterPoint = [int(DisplaySize[0] / 2), int(DisplaySize[1] / 2)]
StartNode = [50, 48]

ThePlayer = Player(StartNode, TheWorld.ExploredTiles, DisplaySize)

def DrawUnit(Unit):

    X = int(DisplaySize[0] / 2 + (CenterPoint[0] - DisplaySize[0] + TheWorld.TileSize * Unit.CurrentNode[0] + Unit.NodeCoordinates[0]) * ThePlayer.Zoom)
    Y = int(DisplaySize[1] / 2 + (CenterPoint[1] - DisplaySize[1] + TheWorld.TileSize * Unit.CurrentNode[1] + Unit.NodeCoordinates[1]) * ThePlayer.Zoom)

    OnScreenSize = int(TheWorld.UnitSize * ThePlayer.Zoom)
    pygame.draw.circle(Window, (Unit.Color[0], Unit.Color[1], Unit.Color[2]), (X, Y), OnScreenSize)

    if DisplayUnitInfo:
        TextSurf, TextRect = text_object(str(Unit.ID) + ": " + Unit.Type + ", " + Unit.State.StateName, TextFont)
        TextRect.midtop = (X, Y + OnScreenSize)
        Window.blit(TextSurf, TextRect)
        if (Unit.Type == "Worker" and Unit.Carrying != "NULL"):
            TextSurf, TextRect = text_object("Carrying: " + Unit.Carrying, TextFont)
            TextRect.midtop = (X, Y + OnScreenSize + int(TextSize * ThePlayer.Zoom))
            Window.blit(TextSurf, TextRect)


Count = 0
while Count < 50:
    Worker(StartNode, ThePlayer)
    Count += 1

#Remove fog of war
"""
for Y, line in enumerate(TheWorld.Tiles):
    for X, letter in enumerate(line):
        TheWorld.DrawTile(ThePlayer.MapImage, X, Y)
"""

LastTime = time.process_time()
CurrentTime = time.process_time()
Paused = False
UpdateRate = 0.01
Running = True

ThePlayer.InitialUpgrade()
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
                    UpdateRate = 1.0 / val
                except ValueError:
                    print("Couldn't convert input to usable value.")
            if (event.key == pygame.K_ESCAPE):
                Running = False
                break
            if (event.key == pygame.K_e):
                DisplayUnitInfo = not DisplayUnitInfo
            if (event.key == pygame.K_q):
                DisplayBuildingInfo = not DisplayBuildingInfo

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 4):
                ThePlayer.Zoom *= 1.1
                if (ThePlayer.Zoom > 15.0):
                    ThePlayer.Zoom = 15.0
            elif (event.button == 5):
                ThePlayer.Zoom /= 1.1
                if (ThePlayer.Zoom < 0.5):
                    ThePlayer.Zoom = 0.5
            if (ThePlayer.Zoom > 0.95 and ThePlayer.Zoom < 1.05):
                ThePlayer.Zoom = 1.0
            TextFont = pygame.font.Font('freesansbold.ttf', int(TextSize * ThePlayer.Zoom))

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

    if (Paused == False and (CurrentTime - LastTime) >= UpdateRate):
        ThePlayer.Update()
        LastTime = CurrentTime

    TempSurface = pygame.transform.scale(ThePlayer.MapImage, (int(ThePlayer.MapImageBaseWidth * ThePlayer.Zoom), int(ThePlayer.MapImageBaseHeight * ThePlayer.Zoom)))

    X = int((DisplaySize[0] / 2 - (DisplaySize[0] - CenterPoint[0]) * ThePlayer.Zoom))
    Y = int((DisplaySize[1] / 2 - (DisplaySize[1] - CenterPoint[1]) * ThePlayer.Zoom))
    DrawArea = TempSurface.get_rect().move(X, Y)
    Window.blit(TempSurface, DrawArea)

    for Unit in ThePlayer.Units:
        DrawUnit(Unit)

    if DisplayBuildingInfo:
        for Structure in ThePlayer.Buildings:
            X = int(DisplaySize[0] / 2 + (CenterPoint[0] - DisplaySize[0] + TheWorld.TileSize * (Structure[0] + 0.5)) * ThePlayer.Zoom)
            Y = int(DisplaySize[1] / 2 + (CenterPoint[1] - DisplaySize[1] + TheWorld.TileSize * (Structure[1] + 1) + 1) * ThePlayer.Zoom)

            TheText = ThePlayer.Buildings[Structure][0]
            TextSurf, TextRect = text_object(TheText, TextFont)
            TextRect.midtop = (X, Y)
            Window.blit(TextSurf, TextRect)
            TheText = str(TheWorld.Tiles[Structure[1]][Structure[0]][1])
            TextSurf, TextRect = text_object(TheText, TextFont)
            TextRect.midtop = (X, Y + int((TextSize + 1) * ThePlayer.Zoom))
            Window.blit(TextSurf, TextRect)

        #Displaying Node Coordinates for testing purposes
        """
        for Y2, line in enumerate(ThePlayer.ExploredTiles):
            for X2, letter in enumerate(line):
                if (letter == "Explored"):
                    X = int(DisplaySize[0] / 2 + (CenterPoint[0] - DisplaySize[0] + TheWorld.TileSize * X2) * ThePlayer.Zoom)
                    Y = int(DisplaySize[1] / 2 + (CenterPoint[1] - DisplaySize[1] + TheWorld.TileSize * Y2) * ThePlayer.Zoom)

                    TheText = str(X2) + ", " + str(Y2)
                    TextSurf, TextRect = text_object(TheText, TextFont)
                    TextRect.topleft = (X, Y)
                    Window.blit(TextSurf, TextRect)
        """


    LineSpace = 10
    for Resource in ThePlayer.Resources:
        Text = Resource + ": " + str(ThePlayer.Resources[Resource])
        TextSurf, TextRect = text_object(Text, LargeTextFont)
        TextRect.topleft = (10, LineSpace)
        Window.blit(TextSurf, TextRect)
        LineSpace += LargeTextSize
    Text = "Soldiers: " + str(ThePlayer.Soldiers)
    TextSurf, TextRect = text_object(Text, LargeTextFont)
    TextRect.topleft = (10, LineSpace)
    Window.blit(TextSurf, TextRect)
    LineSpace += LargeTextSize


    pygame.display.update()


pygame.quit()
#print("Session ended at " + TheTime)