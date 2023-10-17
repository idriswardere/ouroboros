"""
Training agents to play Ouroboros using reinforcement learning.
"""

import time

from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
from stable_baselines3.dqn import DQN
from stable_baselines3.common.base_class import BaseAlgorithm
from stable_baselines3.common.evaluation import evaluate_policy

from ouroboros.environment import Ouroboros

N_DIMS = 2
LEVEL_SIZE = 5
TOTAL_TRAIN_TIMESTEPS = 5_000_000
N_EVAL_EPISODES = 100

TRAIN = False
MODEL = PPO
MODEL_PATH = f"models/ppo/{N_DIMS}d_size{LEVEL_SIZE}_{TOTAL_TRAIN_TIMESTEPS}steps"

RENDER = True


def train():
    """
    Main method for training reinforcement learning agents.
    """
    env = Ouroboros(LEVEL_SIZE, N_DIMS)
    eval_env = Ouroboros(LEVEL_SIZE, N_DIMS, render_mode="human")
    check_env(env)

    model = MODEL('MlpPolicy', env, verbose=0)

    start = time.time()
    mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=N_EVAL_EPISODES, warn=True)
    end = time.time()
    print(f"random agent - mean reward: {mean_reward:.2f} +/- {std_reward:.2f} - time elapsed: {end-start}")

    start = time.time()
    model.learn(total_timesteps=TOTAL_TRAIN_TIMESTEPS, progress_bar=True)
    end = time.time()
    print(f"model learning - time elapsed: {end-start}")
    model.save(MODEL_PATH)

    start = time.time()
    mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=N_EVAL_EPISODES, render=False)
    end = time.time()
    print(f"trained agent - mean reward: {mean_reward:.2f} +/- {std_reward:.2f} - time elapsed: {end-start}")


def test():
    """
    Testing trained agents on a loaded model.
    """
    model = MODEL.load(MODEL_PATH)
    eval_env = Ouroboros(LEVEL_SIZE, N_DIMS, render_mode="human")

    start = time.time()
    mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=N_EVAL_EPISODES, render=RENDER)
    end = time.time()
    print(f"trained agent - mean reward: {mean_reward:.2f} +/- {std_reward:.2f} - time elapsed: {end-start}")


if __name__ == "__main__":
    if TRAIN:
        train()
    else:
        test()
