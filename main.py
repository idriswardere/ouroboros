"""
Main method for demonstration purposes.
"""

import time

import numpy as np

from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
from stable_baselines3.ppo.policies import MlpPolicy
from stable_baselines3.common.base_class import BaseAlgorithm
from stable_baselines3.common.evaluation import evaluate_policy

from ouroboros.game import Game
from ouroboros.level import Level
from ouroboros.controller import PlayerController2D, PlayerController3D
from ouroboros.environment import Ouroboros


def main():
    """
    Testing method.
    """
    level_size = 9
    n_dims = 2
    level = Level(level_size=level_size, n_dims=n_dims)
    game = Game(level=level)

    # print(level.arr)
    # game.move()
    # print(level.arr)

    # player = PlayerController2D(game)
    # player.start()

    # print(env.game.level.arr)
    # print(env.step(1))
    # print(env.game.level.arr)
    
    env = Ouroboros(level_size, n_dims)
    # check_env(env)

    model = PPO(MlpPolicy, env, verbose=0)

    start = time.time()
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=100, warn=True)
    end = time.time()
    print(f"random agent - mean reward: {mean_reward:.2f} +/- {std_reward:.2f} - time elapsed: {end-start}")

    start = time.time()
    model.learn(total_timesteps=100000)
    end = time.time()
    print(f"model learning - time elapsed: {end-start}")

    start = time.time()
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=100)
    end = time.time()
    print(f"trained agent - mean reward: {mean_reward:.2f} +/- {std_reward:.2f} - time elapsed: {end-start}")
    


if __name__ == "__main__":
    main()
