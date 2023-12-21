"""
Functions and declarations for levels.
"""

from enum import Enum
from typing import Optional
import random

import numpy as np


class Level:
    """
    Level object. Contains helper functions and enumerations for different types of cells.
    """
    
    EMPTY = 0
    HEAD = 1
    BODY = 2
    FRUIT = 3
    WALL = 4

    NUM_STATES = 5
     
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
        
        # Gathering initial empty cells. __setitem__ keeps track of them afterwards.
        self.empty_cell_positions = set()
        flat_length = np.prod(self.arr.shape)
        for flat_i in range(flat_length):
            pos = np.unravel_index(flat_i, shape=self.arr.shape)
            if self.arr[pos] == Level.EMPTY:
                self.empty_cell_positions.add(pos)


    def __getitem__(self, key):
        """
        Get an item from self.arr.
        """
        return self.arr.__getitem__(key)

    def __setitem__(self, key, value) -> None:
        """
        Set an item in self.arr. Keeps track of empty cells.
        """
        if self.arr[key] == Level.EMPTY and value != Level.EMPTY:
            self.empty_cell_positions.remove(key)
        if self.arr[key] != Level.EMPTY and value == Level.EMPTY:
            self.empty_cell_positions.add(key)
        return self.arr.__setitem__(key, value)

    def position_out_of_bounds(self, pos: tuple):
        """
        Check if a position is within the bounds of the map.
        """
        for i, dim_size in enumerate(self.arr.shape):
            if pos[i] < 0 or pos[i] >= dim_size:
                return True
        return False

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
    
    def _choose_random_empty_position_rand(self) -> tuple:
        """
        Choose a random empty cell in a level. Returns a tuple representing an index.
        Only optimal when the level is mostly empty cells. Runs forever when no empty 
        cells are remaining in the level.
        """
        flat_length = np.prod(self.arr.shape)
        while True:
            random_flat_idx = np.random.randint(flat_length)
            random_pos = np.unravel_index(random_flat_idx, shape=self.arr.shape)
            if self.arr[random_pos] == Level.EMPTY:
                return random_pos
    
    def choose_random_empty_position(self) -> Optional[tuple]:
        """
        Choose a random empty cell in a level. Returns a tuple representing an index or
        None when no empty cells are left.
        """
        empty_cell_positions_list = list(self.empty_cell_positions)
        if len(empty_cell_positions_list) == 0:
            return None
        random_pos_idx = np.random.randint(len(empty_cell_positions_list))
        random_pos = empty_cell_positions_list[random_pos_idx]

        return random_pos

