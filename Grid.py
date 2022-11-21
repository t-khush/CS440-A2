from Node import Node
import random


def main():
    grid = []
    for i in range(100):
        row = []
        for j in range(50):
            row.append(Node(i, j, gen_terrain()))
        grid.append(row)
    
    # checking if generation works
    for i in range(5):
        print(f"({grid[0][i].x}, {grid[0][i].y}, terrain: {grid[0][i].terrain})")

    # for row in grid:
    #     print(row)

    random_terrain = gen_terrain()
    actions = gen_actions()


def gen_actions():
    actions = ["Up", "Left", "Down", "Right"]
    probabilities = [0.25, 0.25, 0.25, 0.25]
    return random.choices(actions, probabilities, k = 100)

# returns randomly chosen terrain as a string
def gen_terrain():
    states = ["N", "H", "T", "B"]
    probabilities = [0.5, 0.2, 0.2, 0.1]
    return random.choices(states, probabilities)[0] # just want to return as string not list



if __name__ == "__main__":
    main()