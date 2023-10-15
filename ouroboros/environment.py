"""
Defining gymnasium environment for Ouroboros to facilitate reinforcement learning.
"""

from typing import Optional

import numpy as np
import gymnasium as gym
import pygame

from ouroboros.level import Level
from ouroboros.game import Game


class Ouroboros(gym.Env):
    """
    Environment wrapper for Ouroboros.
    """
    
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 5}

    def __init__(self, level_size: int, n_dims: int,
                 render_mode: Optional[str] = None, max_timesteps: Optional[int] = None) -> None:
        """
        Environment initialization. Actions come from a Discrete space of size n_dims*2.
        Observations come from an integer Box space. `max_timesteps` is the max number of
        timesteps that the snake doesn't eat before the episode is truncated.
        """
        self.level_size = level_size
        self.n_dims = n_dims

        level = Level(level_size, n_dims)
        self.game = Game(level=level)
        if max_timesteps is None:
            flat_length = np.prod(self.game.level.shape)
            self.max_timesteps = flat_length*4
        else:
            self.max_timesteps = max_timesteps
        
        # self.observation_space = gym.spaces.Box(0, Level.NUM_STATES-1, shape=self.game.level.shape, dtype=int)
        self.observation_space = gym.spaces.Box(0, flat_length-1, shape=(flat_length,), dtype=int)
        
        # try flattening observation space? normalize? discretize?
        self.action_space = gym.spaces.Discrete(n_dims*2)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.expansion = 20
        self.cell_colors = {
            Level.HEAD:  175,
            Level.EMPTY: 0,
            Level.BODY: 150,
            Level.FRUIT: 255,
            Level.WALL: 20,
        }
        self.cell_color_map = np.vectorize(lambda key: self.cell_colors[key])
        
        self.window = None
        self.clock = None
    
    def _get_obs(self) -> np.ndarray:
        """
        Returns current observation.
        """
        return self.game.level.arr.flatten()

    def _get_info(self) -> np.ndarray:
        """
        Returns auxiliary information.
        """
        return {'snake_length': self.game.snake_length}
    
    def action_to_direction(self, action: int) -> np.ndarray:
        """
        Returns a np.ndarray direction that can be used to change snake direction 
        given an action from the action space.
        """
        direction = np.zeros(self.n_dims, dtype=int)
        direction[action % self.n_dims] = 1
        if action // self.n_dims == 1:
            direction *= -1
        
        return direction
        
    def reset(self, seed: int = None, options = None) -> tuple:
        """
        Resets the environment.
        """
        super().reset(seed=seed)
        level = Level(self.level_size, self.n_dims)
        self.game = Game(level=level)
        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action: int) -> tuple:
        """
        Move the snake forward once based on the selected direction. 
        """
        direction = self.action_to_direction(action)
        self.game.change_direction(direction)
        fruit_eaten = self.game.move()
        observation = self._get_obs()

        if fruit_eaten:
            reward = 1
        else:
            reward = 0

        terminated = self.game.finished
        if terminated and self.game.won():
            reward += 1000

        truncated = bool((self.game.timestep - self.game.latest_fruit_timestep) >= self.max_timesteps)
        info = self._get_info()
        
        return observation, reward, terminated, truncated, info

    def render(self):
        """
        Render the current game state.
        """
        if self.render_mode == "human":
            return self._render_frame()

    def _render_frame(self):
        """
        Render one frame from of the current game state.
        """
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            display_dim_x = self.game.level.arr.shape[0]*self.expansion
            display_dim_y = self.game.level.arr.shape[1]*self.expansion
            self.window = pygame.display.set_mode((display_dim_y, display_dim_x))
            pygame.display.set_caption('Ouroboros')
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        if self.render_mode == "human":
            display_level_arr = self.cell_color_map(self.game.level.arr.transpose())
            display_level_arr = np.repeat(display_level_arr, self.expansion, axis=0)
            display_level_arr = np.repeat(display_level_arr, self.expansion, axis=1)

            surf = pygame.surfarray.make_surface(display_level_arr)
            self.window.blit(surf, (0, 0))
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:
            return self.game.level.arr