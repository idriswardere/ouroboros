"""
Functions and declarations for levels.
"""

from enum import Enum

import numpy as np


class Cell(Enum):
    """
    Enumerations for different types of cells in a level.
    """
    EMPTY = 0
    BODY = 1
    FRUIT = 2
    WALL = 3


def create_empty_level(level_size: int, n_dims: int) -> np.ndarray:
    """
    Create a level with only empty cells.
    """
    level_shape = (level_size,)*n_dims
    level = np.full(shape=level_shape, fill_value=Cell.EMPTY)
    return level

def print_level(level: np.ndarray):
    """
    Print a map to the console.
    """
    print(np.vectorize(lambda e: e.value)(level))


def choose_random_empty_position(level: np.ndarray) -> tuple:
    """
    Choose a random empty cell in a level. Returns a tuple of indices.
    """
    return None
