"""
N-dimensional snake.
"""

from collections import deque
from typing import Optional

import numpy as np

from level import (Cell, choose_random_empty_position)


class Game():
    """
    Game object.
    """

    def __init__(self, level: np.ndarray, start_position: Optional[tuple] = None,
                 start_direction: Optional[np.ndarray] = None) -> None:
        """
        Snake player initialization. Randomly initialized with length 1 by default.
        """
        if start_position is None:
            start_position = tuple(np.random.randint(dim) for dim in level.shape)
            # TODO: make this avoid walls using choose_random_empty_position
        if start_direction is None:
            start_direction = np.zeros(level.ndim, dtype=int)
            rand_dim = np.random.randint(level.ndim)
            start_direction[rand_dim] = np.random.choice([-1, 1])

        self.level = level
        self.finished = False

        self.head = start_position
        self.direction = start_direction
        self.body = deque()
        self.add_to_head(self.head)

    def add_to_head(self, pos):
        """
        Add to the snake's body from the head.
        """
        self.head = pos
        self.body.append(pos)
        self.level[pos] = Cell.BODY

    def remove_from_tail(self):
        """
        Remove the end of the snake's tail.
        """
        tail_pos = self.body.popleft()
        self.level[tail_pos] = Cell.EMPTY

    def position_in_bounds(self, pos: tuple):
        """
        Check if a position is within the bounds of the map.
        """
        for i, dim_size in enumerate(self.level.shape):
            if pos[i] < 0 or pos[i] >= dim_size:
                return False
        return True

    def move(self):
        """
        Move the snake by one timestep.
        """
        new_pos = tuple(self.head + self.direction)
        if not self.position_in_bounds(new_pos) or self.level[new_pos] == Cell.WALL:
            self.finished = True
            return

        self.add_to_head(new_pos)
        if self.level[new_pos] != Cell.FRUIT:
            self.remove_from_tail()

    def change_direction(self, direction: np.ndarray):
        """
        Change the direction of the snake.
        """
        curr_dim = np.argmax(abs(self.direction))
        target_dim = np.argmax(abs(direction))
        if curr_dim != target_dim:
            self.direction = direction
