"""
N-dimensional snake.
"""

from collections import deque
from typing import Optional

import numpy as np

from level import Level


class Game:
    """
    Game object.
    """

    def __init__(self, level: Optional[Level] = None, start_position: Optional[tuple] = None,
                 start_direction: Optional[np.ndarray] = None) -> None:
        """
        Snake player initialization. Randomly initialized with length 1 by default. Provided
        level should only contain empty cells, walls, and extra fruit. All fruit are replaced 
        upon being eaten. One fruit will be generated on initialization regardless of provided level.
        """
        if level is None:
            level = Level()
        if start_position is None:
            # start_position = tuple(np.random.randint(dim) for dim in level.shape)
            # TODO: make this avoid walls using choose_random_empty_position
            start_position = level.choose_random_empty_position()
        if start_direction is None:
            start_direction = np.zeros(level.ndim, dtype=int)
            rand_dim = np.random.randint(level.ndim)
            start_direction[rand_dim] = np.random.choice([-1, 1])

        self.level = level
        self.moves = 0
        self.length = 1
        self.finished = False

        self.head = start_position
        self.direction = start_direction
        self.body = deque()
        self.add_to_head(self.head, None)
        self.spawn_fruit()

    def add_to_head(self, new_pos: tuple, old_pos: Optional[tuple]) -> None:
        """
        Add to the snake's body from the head.
        """
        self.head = new_pos
        self.body.append(new_pos)
        self.level[new_pos] = Level.HEAD
        if old_pos is not None:
            self.level[old_pos] = Level.BODY

    def remove_from_tail(self) -> None:
        """
        Remove the end of the snake's tail.
        """
        tail_pos = self.body.popleft()
        self.level[tail_pos] = Level.EMPTY
    
    def spawn_fruit(self) -> None:
        fruit_pos = self.level.choose_random_empty_position()
        self.level[fruit_pos] = Level.FRUIT

    def move(self) -> None:
        """
        Move the snake by one timestep.
        """
        self.moves += 1
        old_head_pos = self.head
        new_head_pos = tuple(self.head + self.direction)

        if (not self.level.position_in_bounds(new_head_pos) 
                or self.level[new_head_pos] == Level.WALL
                or self.level[new_head_pos] == Level.BODY):
            self.finished = True
            return

        if self.level[new_head_pos] == Level.FRUIT:
            self.add_to_head(new_head_pos, old_head_pos)
            self.spawn_fruit()
        else:
            self.add_to_head(new_head_pos, old_head_pos)
            self.remove_from_tail()

    def change_direction(self, direction: np.ndarray) -> None:
        """
        Change the direction of the snake. Does nothing when trying to go directly backwards.
        """
        self.direction = direction
    
    def won(self):
        """
        Returns True if game has been won.
        """
        return len(self.level.empty_cell_positions) == 0
