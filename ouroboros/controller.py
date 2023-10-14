"""
Controllers for players and agents playing Snake. 
Controllers work by interacting with an instance of the Game object.
"""

from typing import Optional
import time

import pygame
import numpy as np
import matplotlib.pyplot as plt

from ouroboros.game import Game
from ouroboros.level import Level

class Controller:
    """
    Controller interface. 
    """
    def __init__(self, game: Game) -> None:
        self.game = game
    
    def play(self) -> None:
        pass
    
    def display(self):
        pass


class PlayerController2D(Controller):
    """
    Controller for human players. Only works on 2D levels.
    """
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        assert game.level.ndim == 2

        self.expansion = 20

        self.cell_colors = {
            Level.HEAD:  175,
            Level.EMPTY: 0,
            Level.BODY: 150,
            Level.FRUIT: 255,
            Level.WALL: 20,
        }
        self.cell_color_map = np.vectorize(lambda key: self.cell_colors[key])

        self.keybinds = {
            pygame.K_w: np.array([-1, 0]),
            pygame.K_a: np.array([0, -1]),
            pygame.K_s: np.array([1, 0]),
            pygame.K_d: np.array([0, 1]),
        }

    
    def play(self, input: Optional[str]) -> None:
        pass
    
    def start(self) -> None:
        pygame.init()
        display_dim_x = self.game.level.arr.shape[0]*self.expansion
        display_dim_y = self.game.level.arr.shape[1]*self.expansion
        self.dis = pygame.display.set_mode((display_dim_y, display_dim_x))
        pygame.display.update()
        pygame.display.set_caption('Ouroboros')

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key in self.keybinds.keys():
                        new_direction = self.keybinds[event.key]
                        self.game.change_direction(new_direction)
                        self.game.move()
                        print(self.game.won())
                        print(self.game.finished)

            display_level_arr = self.cell_color_map(self.game.level.arr.transpose())
            display_level_arr = np.repeat(display_level_arr, self.expansion, axis=0)
            display_level_arr = np.repeat(display_level_arr, self.expansion, axis=1)

            surf = pygame.surfarray.make_surface(display_level_arr)
            self.dis.blit(surf, (0, 0))
            pygame.display.update()


class PlayerController3D(Controller):
    """
    Controller for human players. Only works on 3D levels.
    """
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        assert game.level.ndim == 3

        self.cell_colors = {
            Level.HEAD:  'blue',
            Level.EMPTY: 0,
            Level.BODY: 'green',
            Level.FRUIT: 'red',
            Level.WALL: 'black',
        }
        self.cell_color_map = np.vectorize(lambda key: self.cell_colors[key], otypes=[object])

        self.keybinds = {
            pygame.K_w: np.array([0, 1, 0]),
            pygame.K_s: np.array([0, -1, 0]),
            pygame.K_a: np.array([-1, 0, 0]),
            pygame.K_d: np.array([1, 0, 0]),
            pygame.K_k: np.array([0, 0, -1]),
            pygame.K_j: np.array([0, 0, 1]),
        }

    def play(self, input: Optional[str]) -> None:
        pass
    
    def start(self) -> None:
        pygame.init()
        self.dis = pygame.display.set_mode((400, 400))
        pygame.display.update()
        pygame.display.set_caption('Ouroboros')
        #plt.ion()
        

        done = False
        while not done:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key in self.keybinds.keys():
                        new_direction = self.keybinds[event.key]
                        self.game.change_direction(new_direction)
                        self.game.move()
                        print(self.game.level.arr)

                        display_level_arr = self.game.level.arr != Level.EMPTY
                        color_arr = self.cell_color_map(self.game.level.arr.astype(object))
                        fig = plt.figure()
                        ax = fig.add_subplot(projection='3d')
                        ax.voxels(display_level_arr, facecolors=color_arr, edgecolor='k')
                        plt.show(block=True)
            
            