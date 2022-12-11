import pygame
from pygame import font
from Node import Terrain
import sys

BLACK = (0, 0, 0)
R, G, B = 255, 255, 255
WHITE = (250, 250, 250)
BLUE = (0, 0, 255)
WINDOW_HEIGHT = 2000
WINDOW_WIDTH = 1000

def renderGrid(grid: list):
    '''
    for i in range(len(grid)): 
        for j in range(len(grid[i])): 
            print(str(grid[i][j]), end = " ")
        print()
    '''
    pygame.init()
    global SCREEN
    global font
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(WHITE)
    font = pygame.freetype.Font(None, 12)

    hasUpdated = False 
    while True:
        drawGrid(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if hasUpdated is False: 
            pygame.display.update()
        hasUpdated = True 



def drawGrid(grid: list):
    blockSize = 20 #Set the size of the grid block
    gridX = 1
    for x in range(0, WINDOW_WIDTH, blockSize):
        gridY = 1
        for y in range(0, WINDOW_HEIGHT, blockSize):
            node = grid[gridY][gridX]
            terrain = node.terrain
            prob = node.prob
            rect = pygame.Rect(x, y, blockSize, blockSize)

            if terrain != Terrain.B:
                pygame.draw.rect(SCREEN, (R, G - G * prob, B - B * prob), rect, 0)
            else: 
                pygame.draw.rect(SCREEN, (120, 120, 120), rect, 0)
            
            pygame.draw.rect(SCREEN, BLACK, rect, 1)

            gridY = gridY + 1 
            addText(terrain, x, y)
        gridX = gridX+1

def addText(text: str, x: int, y: int):
    font.render_to(SCREEN, (x+5, y+5), str(text.value) )
