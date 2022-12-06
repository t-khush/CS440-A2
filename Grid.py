from Node import Node, Terrain
import random
import sys
import os

ROWS = 100
COLS = 50

def main(): 
    if len(sys.argv) == 2: 
        nodesList, actionString, terrainString = readFile(sys.argv[1])   
    mapGeneration()

def mapGeneration():
    if os.path.exists("maps"):
        print("Maps already generated")
        return
    os.mkdir("maps")
    # 10 maps
    for i in range(10):
        grid = gen_grid()
        subdir = os.path.join(os.getcwd(), "maps")
        path = os.path.join(subdir, f"map_{i+1}")
        os.mkdir(path)

        # 10 files per map
        for j in range(10):
            with open(os.path.join(path, f"testcase_{j+1}.txt"), "w+") as f:
                startX, startY = randomStartVertex(grid)
                randomActionString = gen_action_sequence(grid, startX, startY)
                simulatedPath, terrain_readings = simulateAgent(grid, randomActionString, startX, startY)

                for node in simulatedPath:
                    f.write(f"{node.x} {node.y}\n")
                for action in randomActionString:
                    f.write(f"{action}")
                f.write("\n")
                for terrain in terrain_readings:
                    f.write(f"{terrain.name}")

def gen_grid(): 
    grid = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(Node(i, j, gen_terrain()))
        grid.append(row)
    return grid 

def gen_terrain() -> Terrain:
    terrains = [Terrain.N, Terrain.H, Terrain.T, Terrain.B]
    probabilities = [0.5, 0.2, 0.2, 0.1]
    return random.choices(terrains, probabilities)[0]

def gen_action() -> str:
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
    
    def sensor_reading(actual: Terrain):
        terrains = [Terrain.N, Terrain.H, Terrain.T]
        if actual == Terrain.N:
            probabilities = [0.9, 0.05, 0.05]
        elif actual == Terrain.H:
            probabilities = [0.05, 0.9, 0.05]
        else:
            probabilities = [0.05, 0.05, 0.9]
        return random.choices(terrains, probabilities)[0]

    nodePath = []
    nodePath.append(grid[x][y])
    terrain_readings = []
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
        terrain_readings.append(sensor_reading(grid[x][y].terrain))
        nodePath.append(grid[x][y])

    return nodePath, terrain_readings
def readFile(fileName: str): 
    nodesList = []
    with open(fileName, 'r') as f: 
        for i in range(101): 
            x,y = next(f).strip().split(" ")
            nodesList.append(Node(int(x), int(y)))
        actionString = next(f).strip()
        terrainString = next(f).strip()
    return nodesList, actionString, terrainString


if __name__ == "__main__": 
    main()
