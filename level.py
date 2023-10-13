"""
Functions and declarations for levels.
"""

from enum import Enum
from typing import Optional

import numpy as np


class Level:
    """
    Level object. Contains helper functions and enumerations for different types of cells.
    """

    HEAD = -1
    EMPTY = 0
    BODY = 1
    FRUIT = 2
    WALL = 3
     
    def __init__(self, level_size: Optional[int] = 9, n_dims: Optional[int] = 2,
                 arr: Optional[np.ndarray] = None) -> None:
        """
        Level initialization. Full of empty cells by default. When arr is provided, it
        overrides other arguments defining the level.
        """
        if arr is None:
            level_shape = (level_size,)*n_dims
            self.arr = np.full(shape=level_shape, fill_value=Level.EMPTY)
        else:
            self.arr = arr

        self.shape = self.arr.shape
        self.ndim = self.arr.ndim

    def __getitem__(self, key):
        return self.arr.__getitem__(key)

    def __setitem__(self, key, value) -> None:
        return self.arr.__setitem__(key, value)

    def position_in_bounds(self, pos: tuple):
        """
        Check if a position is within the bounds of the map.
        """
        for i, dim_size in enumerate(self.arr.shape):
            if pos[i] < 0 or pos[i] >= dim_size:
                return False
        return True

    def _choose_random_empty_position_iter(self) -> Optional[tuple]:
        """
        Choose a random empty cell in a level. Returns a tuple representing an index or none when.
        no empty cells are remaining. Implemented using iterative method. Should be used if level 
        doesn't have many empty cells remaining.
        """
        flat_length = np.prod(self.arr.shape)
        empty_cell_positions = []

        for flat_i in range(flat_length):
            pos = np.unravel_index(flat_i, shape=self.arr.shape)
            if self.arr[pos] == Level.EMPTY:
                empty_cell_positions.append(pos)

        if len(empty_cell_positions) == 0:
            return None
        random_pos_idx = np.random.randint(len(empty_cell_positions))
        random_pos = empty_cell_positions[random_pos_idx]

        return random_pos
    
    def choose_random_empty_position(self, iter=True) -> tuple:
        """
        Choose a random empty cell in a level. Returns a tuple representing an index.
        Set iter=True if level has many empty cells for performance. Runs forever when
        no empty cells are remaining in the level.
        """
        if iter:
            return self._choose_random_empty_position_iter()

        flat_length = np.prod(self.arr.shape)
        while True:
            random_flat_idx = np.random.randint(flat_length)
            random_pos = np.unravel_index(random_flat_idx, shape=self.arr.shape)
            if self.arr[random_pos] == Level.EMPTY:
                return random_pos

