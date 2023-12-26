"""
Training agents to play Ouroboros using reinforcement learning.
"""

import time
import os

from stable_baselines3 import PPO
from stable_baselines3.dqn import DQN

from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy

from ouroboros.environment import Ouroboros

MODEL_NAME = "ppo"
N_DIMS = 3
LEVEL_SIZE = 5
TOTAL_TRAIN_TIMESTEPS = 25_000_000
N_EVAL_EPISODES = 100
RENDER = False


def get_model_class(model_name: str):
    MODEL_DICT = {
        "dqn": DQN,
        "ppo": PPO,
    }
    return MODEL_DICT[model_name]


def get_model_path(model_name, n_dims, level_size, timesteps):
    return f"models/{model_name}/{n_dims}d_size{level_size}_{timesteps}steps"


def train(level_size, n_dims, model_name, n_eval_episodes, timesteps, save_path):
    """
    Main method for training reinforcement learning agents.
    """
    env = Ouroboros(level_size, n_dims)
    eval_env = Ouroboros(level_size, n_dims, render_mode="human")
    # check_env(env)
    model_class = get_model_class(model_name)
    model = model_class('MlpPolicy', env, verbose=0)

    start = time.time()
    mean_reward, std_reward = evaluate_policy(model, eval_env,
                                              n_eval_episodes=n_eval_episodes,
                                              warn=True)
    end = time.time()
    print(f"random agent - mean reward: {mean_reward:.2f} +/- {std_reward:.2f} - time elapsed: {end-start}")

    start = time.time()
    model.learn(total_timesteps=timesteps, progress_bar=True)
    end = time.time()
    print(f"model learning - time elapsed: {end-start}")
    model.save(save_path)

    start = time.time()
    mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=n_eval_episodes, render=False)
    end = time.time()
    print(f"trained agent - mean reward: {mean_reward:.2f} +/- {std_reward:.2f} - time elapsed: {end-start}")


def test(model_name, n_dims, level_size, timesteps, n_eval_episodes, render):
    """
    Testing trained agents on a loaded model.
    """
    model_class = get_model_class(model_name)
    model_path = get_model_path(model_name, n_dims, level_size, timesteps)
    model = model_class.load(model_path)
    eval_env = Ouroboros(level_size, n_dims, render_mode="human")

    start = time.time()
    mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=n_eval_episodes, render=render)
    end = time.time()
    print(f"trained agent - mean reward: {mean_reward:.2f} +/- {std_reward:.2f} - time elapsed: {end-start}")


if __name__ == "__main__":
    cmd = input("Select an option\n1: Train\n2: Evaluate\n")
    if cmd == "1":
        save_path = get_model_path(model_name=MODEL_NAME, n_dims=N_DIMS,
                                level_size=LEVEL_SIZE, timesteps=TOTAL_TRAIN_TIMESTEPS)
        if os.path.exists(save_path + ".zip"):
            cmd = input("An agent trained with the chosen configuration already exists.\n"\
                        "Would you like to continue?\n1: Yes\n2: No\n")
            if cmd != "1":
                exit(0)
        train(level_size=LEVEL_SIZE, n_dims=N_DIMS, model_name=MODEL_NAME, 
              n_eval_episodes=N_EVAL_EPISODES, timesteps=TOTAL_TRAIN_TIMESTEPS,
              save_path=save_path)
    elif cmd == "2":
        model_path = get_model_path(model_name=MODEL_NAME, n_dims=N_DIMS,
                                level_size=LEVEL_SIZE, timesteps=TOTAL_TRAIN_TIMESTEPS)
        if not os.path.exists(model_path + ".zip"):
            print("An agent trained with the chosen configuration does not exist.")
            exit(1)
        test(model_name=MODEL_NAME, n_dims=N_DIMS, level_size=LEVEL_SIZE,
             timesteps=TOTAL_TRAIN_TIMESTEPS, n_eval_episodes=N_EVAL_EPISODES,
             render=RENDER)
