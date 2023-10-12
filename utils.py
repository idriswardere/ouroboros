from enum import Enum

import numpy as np


class Tile(Enum):
    """
    Enumerations for different types of tiles in a map.
    """
    EMPTY = 0
    BODY = 1
    FRUIT = 2
    WALL = 3


def create_empty_arr(arr_size: int, n_dims: int) -> np.ndarray:
    """
    Create a map with only empty tiles.
    """
    arr_shape = (arr_size,)*n_dims
    arr = np.full(shape=arr_shape, fill_value=Tile.EMPTY)
    return arr

def print_arr(arr: np.ndarray):
    """
    Prints a map to the console.
    """
    print(np.vectorize(lambda e: e.value)(arr))
