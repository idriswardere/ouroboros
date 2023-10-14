"""
Training agents to play Ouroboros using reinforcement learning.
"""

import time

import numpy as np

from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
from stable_baselines3.dqn import DQN
from stable_baselines3.common.base_class import BaseAlgorithm
from stable_baselines3.common.evaluation import evaluate_policy

from ouroboros.game import Game
from ouroboros.level import Level

from ouroboros.environment import Ouroboros


def main():
    """
    Main method for training reinforcement learning agents.
    """
    level_size = 4
    n_dims = 2
    # level = Level(level_size=level_size, n_dims=n_dims)
    # game = Game(level=level)

    env = Ouroboros(level_size, n_dims)
    eval_env = Ouroboros(level_size, n_dims, render_mode="human")
    check_env(env)

    model = DQN('MlpPolicy', env, verbose=0)

    start = time.time()
    mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=100, warn=True)
    end = time.time()
    print(f"random agent - mean reward: {mean_reward:.2f} +/- {std_reward:.2f} - time elapsed: {end-start}")

    start = time.time()
    model.learn(total_timesteps=100_000, progress_bar=True)
    end = time.time()
    print(f"model learning - time elapsed: {end-start}")

    start = time.time()
    mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=100, render=True)
    end = time.time()
    print(f"trained agent - mean reward: {mean_reward:.2f} +/- {std_reward:.2f} - time elapsed: {end-start}")
    


if __name__ == "__main__":
    main()
