from enum import Enum

class Terrain(Enum): 
    N = 1
    H = 2
    T = 3
    B = 4
    NOT_DEFINED = -1

class Node:
    def __init__(self, x: int, y: int, terrain: Terrain = Terrain.NOT_DEFINED, prob: float = 0.0):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.prob = prob

    def __str__(self) -> str:
        return (f"({self.x + 1}, {self.y+ 1}, terrain: {self.terrain})")