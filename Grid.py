from Node import Node, Terrain
import random

ROWS = 100
COLS = 50 
def main():
    grid = gen_grid()
    startX, startY = randomStartVertex(grid)

    randomActionString = gen_action_sequence(grid, startX, startY)
    simulatedPath = simulateAgent(grid, randomActionString, startX, startY)
    print(len(simulatedPath))

'''   
    # checking if generation worked
    for i in range(ROWS):
        for j in range(COLS):
            print(str(grid[i][j]))
'''
def gen_grid(): 
    grid = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(Node(i, j, Terrain.NOT_DEFINED))
        grid.append(row)

    addTerrain(grid, Terrain.N, int(0.5 * ROWS * COLS))
    addTerrain(grid, Terrain.H, int(0.2 * ROWS * COLS))
    addTerrain(grid, Terrain.T, int(0.2 * ROWS * COLS))
    addTerrain(grid, Terrain.B, int(0.1 * ROWS * COLS))

    return grid 

def gen_action():
    actions = ["Up", "Left", "Down", "Right"]
    probabilities = [0.25, 0.25, 0.25, 0.25]
    return random.choices(actions, probabilities)[0]

def gen_action_sequence(grid, x, y):
    sequence = ""
    for i in range(100): 
        flag = True
        while flag: 
            action = gen_action()
            if action == "Up":
                if x == 0 or grid[x-1][y].terrain != Terrain.B:
                    x = max(0, x-1)
                    flag = False 
                    sequence = sequence + "U"
            if action == "Down": 
                if x == ROWS - 1 or grid[x+1][y].terrain != Terrain.B: 
                    x = min(ROWS-1, x + 1)
                    flag = False 
                    sequence = sequence + "D"
            if action == "Right": 
                if y == COLS -1 or grid[x][y+1]!= Terrain.B: 
                    y = min(COLS - 1, y + 1)
                    flag = False 
                    sequence = sequence + "R"
            if action == "Left": 
                if y == 0 or grid[x][y-1] != Terrain.B: 
                    y = max(0, y-1)
                    flag = False
                    sequence = sequence + "L"

    return sequence
                
# Takes grid, a terrain type, and the count of the terrain that should exist and adds them to the grid
def addTerrain(grid: list, terrainType: Terrain, terrainCount: int):
    for i in range(terrainCount): 
        randX, randY = randomVertex()
        while grid[randX][randY].terrain != Terrain.NOT_DEFINED: 
            randX, randY = randomVertex()
        grid[randX][randY].terrain = terrainType

def randomStartVertex(grid: list): 
    randX, randY = randomVertex()
    while(grid[randX][randY].terrain == Terrain.B): 
        randX, randY = randomVertex()
    return (randX, randY)

def randomVertex(): 
    randX = random.randrange(0, ROWS)
    randY = random.randrange(0, COLS)
    return (randX, randY)

def simulateAgent(grid: list, randomActionString: str, x: int, y: int): 
    def willFollowDirection():
        actions = ["Yes", "No"]
        probabilities = [0.9, 0.1]
        return random.choices(actions, probabilities)[0]
    nodePath = []
    nodePath.append(grid[x][y])
    for direction in randomActionString: 
        if(willFollowDirection() == "Yes"):
            if direction == "U": 
                if x == 0 or grid[x-1][y].terrain != Terrain.B:
                    x = max(0, x-1)
            if direction == "D": 
                if x == ROWS - 1 or grid[x+1][y].terrain != Terrain.B: 
                    x = min(ROWS-1, x + 1)
            if direction == "L": 
                if y == 0 or grid[x][y-1] != Terrain.B: 
                    y = max(0, y-1)
            if direction == "R": 
                if y == COLS -1 or grid[x][y+1]!= Terrain.B: 
                    y = min(COLS - 1, y + 1)
        nodePath.append(grid[x][y])

    return nodePath
if __name__ == "__main__":
    main()