"""
Main method for demonstration purposes.
"""

from ouroboros.game import Game
from ouroboros.level import Level
from ouroboros.controller import PlayerController2D, PlayerController3D

def main():
    """
    Testing method.
    """
    level_size = 3
    n_dims = 3
    level = Level(level_size=level_size, n_dims=n_dims)
    game = Game(level=level)

    # print(level.arr)
    # game.move()
    # print(level.arr)

    player = PlayerController3D(game)
    player.start()


if __name__ == "__main__":
    main()
