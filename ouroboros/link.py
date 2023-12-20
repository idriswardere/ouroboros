"""
Functions that facilitate the link between Ouroboros and the Hydra frontend.
"""
import numpy as np
from ouroboros.level import Level
from ouroboros.game import Game

game = None


def init_game(level_size: int, n_dims: int) -> None:
    """
    Initializes an Ouroboros game from frontend input.
    """
    global game
    level = Level(level_size=level_size, n_dims=n_dims)
    game = Game(level=level)


def progress_game(direction: np.ndarray) -> "tuple[list, int]":
    """
    Progresses an Ouroboros game given an input direction.
    Returns state matrix as nested lists and game status. 
    Status map: 0: Playing, 1: Lost, 2: Won
    """
    global game
    game.change_direction(direction)
    game.move()
    
    state = game.level.arr.tolist()

    if game.won():
        status = 2
    elif game.finished:
        status = 1
    else:
        status = 0

    return state, status