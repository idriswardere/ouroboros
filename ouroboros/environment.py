"""
Defining gymnasium environment for Ouroboros to facilitate reinforcement learning.
"""

from typing import Optional

import numpy as np
import gymnasium as gym

from ouroboros.level import Level
from ouroboros.game import Game


class Ouroboros(gym.Env):
    """
    Environment wrapper for Ouroboros.
    """
    
    #metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, level_size: int, n_dims: int, max_timesteps: Optional[int] = None) -> None:
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
            self.max_timesteps = flat_length*3
        else:
            self.max_timesteps = max_timesteps
        
        self.observation_space = gym.spaces.Box(0, Level.NUM_STATES-1, shape=self.game.level.shape, dtype=int)
        self.action_space = gym.spaces.Discrete(n_dims*2)
    
    def _get_obs(self) -> np.ndarray:
        """
        Returns current observation.
        """
        return self.game.level.arr

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
        reward = int(self.game.move())
        observation = self._get_obs()

        done = self.game.finished
        if done and self.game.won():
            reward += 10

        truncated = (self.game.timestep - self.game.latest_fruit_timestep) >= self.max_timesteps
        info = self._get_info()
        
        return observation, reward, done, truncated, info

    def render(self):
        """
        Render the current game state.
        """
        print(self.game.level.arr)