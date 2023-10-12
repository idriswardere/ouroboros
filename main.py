"""
Main method for demonstration purposes.
"""

from game import Game
from level import create_empty_level, print_level

def main():
    """
    Testing method.
    """
    map_size = 9
    n_dims = 2
    level = create_empty_level(map_size, n_dims)
    game = Game(level)
    print_level(game.level)
    game.move()
    print_level(game.level)


if __name__ == "__main__":
    main()
