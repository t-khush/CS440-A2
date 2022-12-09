from Node import Node, Terrain
from filter import compute_prob
import random
import sys
import os

ROWS = 100
COLS = 50

def main():
    if len(sys.argv) == 4:
    
        map_path = os.path.join(os.getcwd(), "maps", f"map_{sys.argv[1]}", "map.txt")
        testcase_path = os.path.join(os.getcwd(), "maps", f"map_{sys.argv[1]}", f"testcase_{sys.argv[2]}.txt")
        num_actions = int(sys.argv[3])
        grid, blocked_count = readMap(map_path)
        nodesList, actionString, terrainString = readFile(testcase_path)
        # track_prob is a 2d array that stores the probabilities of all cells before the current action is executed, this is req when computing new probabilites
        track_prob = []
        for i in range(ROWS+1):
            filler = [0.0]*(COLS+1)
            track_prob.append(filler)

        # run filtering algorithm
        compute_prob(grid, num_actions, blocked_count, nodesList, actionString, terrainString, track_prob)
    else:
        mapGeneration()
        print("Run grid.py again with map number and test case number as arguments. Example command: 'python grid.py 1 3' for running testcase 3 on map 1")
    
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
        with open(os.path.join(path, "map.txt"), "w+") as f:
            for i in range(1, ROWS+1):
                for j in range(1, COLS+1):
                    f.write(f"{grid[i][j].x} {grid[i][j].y} {grid[i][j].terrain.name}\n")

        # 10 files per map
        for j in range(10):
            with open(os.path.join(path, f"testcase_{j+1}.txt"), "w+") as f:
                startX, startY = randomStartVertex(grid)
                randomActionSeq = gen_action_sequence()
                simulatedPath, terrain_readings = simulateAgent(grid, randomActionSeq, startX, startY)

                for node in simulatedPath:
                    f.write(f"{node.x} {node.y}\n")
                for action in randomActionSeq:
                    f.write(f"{action}")
                f.write("\n")
                for terrain in terrain_readings:
                    f.write(f"{terrain.name}")
    print("Maps generated successfully")

def gen_grid(): 
    grid = []
    # the first row and the first column of each row is a blocked cell so that the first cell is grid[1][1]
    filler = []
    for i in range(COLS+1):
        filler.append(Node(0, i, Terrain.B))
    grid.append(filler)
    for i in range(1, ROWS+1):
        row = [Node(i, 0, Terrain.B)]
        for j in range(1, COLS+1):
            row.append(Node(x = i, y = j, terrain = gen_terrain()))
        grid.append(row)
    return grid 

def gen_terrain() -> Terrain:
    terrains = [Terrain.N, Terrain.H, Terrain.T, Terrain.B]
    probabilities = [0.5, 0.2, 0.2, 0.1]
    return random.choices(terrains, probabilities)[0]

def gen_action_sequence() -> list:
    actions = ["U", "L", "D", "R"]
    probabilities = [0.25, 0.25, 0.25, 0.25]
    return random.choices(actions, probabilities, k = 100)

def randomStartVertex(grid: list): 
    randX, randY = randomVertex()
    while(grid[randX][randY].terrain == Terrain.B): 
        randX, randY = randomVertex()
    return (randX, randY)

def randomVertex(): 
    randX = random.randrange(1, ROWS+1)
    randY = random.randrange(1, COLS+1)
    return (randX, randY)

def simulateAgent(grid: list, randomActionSeq: str, x: int, y: int): 
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
    for direction in randomActionSeq: 
        if(willFollowDirection() == "Yes"):
            if direction == "U": 
                if x != 1 and grid[x-1][y].terrain.name != "B":
                    x -= 1
            if direction == "D": 
                if x != ROWS and grid[x+1][y].terrain.name != "B": 
                    x += 1
            if direction == "L": 
                if y != 1 and grid[x][y-1].terrain.name != "B": 
                    y -= 1
            if direction == "R": 
                if y != COLS and grid[x][y+1].terrain.name != "B": 
                    y += 1
        terrain_readings.append(sensor_reading(grid[x][y].terrain))
        nodePath.append(grid[x][y])

    return nodePath, terrain_readings

def readMap(fileName: str):
    grid = []
    blocked_count = 0
    filler = []
    # the first row and the first column of each row is a blocked cell so that the first cell is = grid[1][1]
    for i in range(COLS+1):
        filler.append(Node(0, i, Terrain.B))
    grid.append(filler)
    with open(fileName, "r") as f:
        for i in range(1, ROWS+1):
            row = [Node(i, 0, Terrain.B)]
            for j in range(1, COLS+1):
                line = f.readline().strip()
                x, y, t = line.split(" ")
                if t == "N":
                    terrain = Terrain.N
                elif t == "H":
                    terrain = Terrain.H
                elif t == "T":
                    terrain = Terrain.T
                else:
                    blocked_count += 1
                    terrain = Terrain.B
                row.append(Node(int(x), int(y), terrain))
            
            grid.append(row)
    return grid, blocked_count 

def readFile(fileName: str): 
    nodesList = []
    with open(fileName, 'r') as f: 
        for i in range(101): 
            x,y = next(f).strip().split(" ")
            # we need only the coordinates of the actual path followed by the agent so no need to store a list of nodes, tuples of coordinates is fine
            nodesList.append((int(x), int(y)))
        actionString = next(f).strip()
        terrainString = next(f).strip()
    return nodesList, actionString, terrainString


if __name__ == "__main__": 
    main()
