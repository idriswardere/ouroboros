"""
Main method for demonstrating the game Ouroboros.
"""

from ouroboros.game import Game
from ouroboros.level import Level
from ouroboros.controller import PlayerController2D

LEVEL_SIZE = 9
N_DIMS = 2

def main():
    """
    Creates a PlayerController for Ouroboros that is usable by humans.
    """    
    level = Level(level_size=LEVEL_SIZE, n_dims=N_DIMS)
    game = Game(level=level)

    player = PlayerController2D(game)
    player.start()


if __name__ == "__main__":
    main()
