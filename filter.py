from Node import Node, Terrain
import random
import sys
import os
from UserInterface import renderGrid

ROWS = 100
COLS = 50

def compute_prob(grid, num_actions, blocked_count, nodesList, actionString, terrainString, track_prob):
    nodesList.pop(0) # first vertex is the starting vertex, next 100 are the result of 100 actions
    # we first set the initial probability of all cells (only possible after getting blocked_count)
    for i in range(1, ROWS + 1):
        for j in range(1, COLS + 1):
            if grid[i][j].terrain.name != "B":
                grid[i][j].prob = 1 / ((ROWS*COLS) - blocked_count)
                track_prob[i][j] = 1 / ((ROWS*COLS) - blocked_count)

    # we excecute upto the input number of actions
    for i in range(num_actions):
        action = actionString[i]
        sensor_reading = terrainString[i]
        for i in range(1, ROWS + 1):
            for j in range(1, COLS + 1):
                if grid[i][j].terrain.name != "B":
                    # this flag helps us to determine if the agent gave a correct sensor reading or not
                    sensorFlag = True if (grid[i][j].terrain.name == sensor_reading) else False

                    # based on the current action, we set the prev and action flags to find probability
                    prevBlocked = False
                    actionBlocked = False
                    
                    if action == "U":
                        if i == ROWS or grid[i+1][j].terrain.name == "B":
                            prevBlocked = True
                        if i == 1 or grid[i-1][j].terrain.name == "B":
                            actionBlocked = True
                    
                    elif action == "D":
                        if i == 1 or grid[i-1][j].terrain.name == "B":
                            prevBlocked = True
                        if i == ROWS or grid[i+1][j].terrain.name == "B":
                            actionBlocked = True

                    elif action == "L":
                        if j == COLS or grid[i][j+1].terrain.name == "B":
                            prevBlocked = True
                        if j == 1 or grid[i][j-1].terrain.name == "B":
                            actionBlocked = True
                    
                    elif action == "R":
                        if j == 1 or grid[i][j-1].terrain.name == "B":
                            prevBlocked = True
                        if j == COLS or grid[i][j+1].terrain.name == "B":
                            actionBlocked = True
                    
                    grid[i][j].prob = updateProb(i, j, grid, action, actionBlocked, prevBlocked, sensorFlag, track_prob)
                    
        # once we are done with updating the probabilities, we normalize the grid and update track_prob
        normalize(grid, track_prob)
    x,y,prob = find_largest(grid)
    # coordinates of the actual last point
    print(f"Coordinates of actual position: {grid[nodesList[num_actions-1][0]][nodesList[num_actions-1][1]].x} {grid[nodesList[num_actions-1][0]][nodesList[num_actions-1][1]].y}")
    
    # prob that our agent is actually on the cell at the end of actions
    print(f"Probability of being at actual position: {grid[nodesList[num_actions-1][0]][nodesList[num_actions-1][1]].prob}")
    
    # coordinates of the most probable location of the agent according to the filtering algorithm
    print(f"Coordinates of the predicted location by filtering algorithms: {x} {y}")

    # prob of being at predicted location
    print(f"Probability of agent being at predicted location: {prob}")

    # Once we have the probabilities we can render the heatmap
    renderGrid(grid)


def updateProb(i, j, grid, action, actionBlocked, prevBlocked, sensorFlag, track_prob) -> float:
    new_prob = 0.0
    # current probability of the cell the agent is currently on 
    old_prob = grid[i][j].prob

    # probability of the agent being on the previous cell, i.e, if the agent arrived on the current cell after actually moving
    # this var stores the prob of the agent being at the 'previous' cell at state X(t-1)
    prev_prob = 0.0

    # observation model
    o_model = 0.9 if sensorFlag else 0.05

    # if the cell before the current one (based on direction of action) is not blocked, our agent could have moved to the current cell with
    # a probability of 0.9
    if not prevBlocked:
        if action == "U":
            prev_prob = track_prob[i+1][j]
        elif action == "D":
            prev_prob = track_prob[i-1][j]
        elif action == "L":
            prev_prob = track_prob[i][j+1]
        elif action == "R":
            prev_prob = track_prob[i][j-1]

    # if its not possible for the agent to execute the action, it is guaranteed to stay at it's place
    # we have 4 cases of how the agent could have been at its current cell, and the probabilities change based on the 2 flags

    # prevBlocked = False implies that we are certain the agent was already on the current cell before the action was executed
    if prevBlocked and actionBlocked:
        new_prob = old_prob*1.0*o_model
    elif prevBlocked and not actionBlocked:
        new_prob = old_prob*0.1*o_model

    # otherwise, it is possible the agent arrived at the current cell after executing the given action
    elif not prevBlocked and actionBlocked:
        new_prob = prev_prob*0.9*o_model + old_prob*1.0*o_model
    elif not prevBlocked and not actionBlocked:
        new_prob = prev_prob*0.9*o_model + old_prob*0.1*o_model

    return new_prob

def find_largest(grid):
    res = 0.0
    x = 0
    y = 0
    for i in range(1, ROWS + 1):
        for j in range(1, COLS + 1):
            if grid[i][j].prob > res:
                res = grid[i][j].prob
                x = i
                y = j
    return x,y,res

def normalize(grid, track_prob):
    total = 0.0
    alpha = 0.0
    for i in range(1, ROWS + 1):
        for j in range(1, COLS + 1):
            total += grid[i][j].prob
    alpha = 1/total
    for i in range(1, ROWS + 1):
        for j in range(1, COLS + 1):
            grid[i][j].prob = grid[i][j].prob*alpha
            # track_prob is updated to keep track of the probabilities
            track_prob[i][j] = grid[i][j].prob

