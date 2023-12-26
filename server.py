"""
Functions that facilitate the link between Ouroboros and the Hydra frontend.
"""
import numpy as np
from stable_baselines3.common.evaluation import evaluate_policy

from ouroboros.level import Level
from ouroboros.game import Game
from ouroboros.environment import Ouroboros

from train import get_model_path, get_model_class


game = None


def init_game(level_size: int, n_dims: int) -> None:
    """
    Initialize an Ouroboros game from frontend input.
    """
    # TODO: Investigate whether tokens are necessary for game initialization (and progressing)
    global game
    level = Level(level_size=level_size, n_dims=n_dims)
    game = Game(level=level)


def progress_game(direction: np.ndarray) -> "tuple[list, int]":
    """
    Progress an Ouroboros game given an input direction.
    Returns state matrix as nested lists and game status. 
    Status map: 0: Playing, 1: Lost, 2: Won
    """
    global game
    game.change_direction(direction)
    game.move()
    
    state = game.level.arr.tolist()

    if game.won():
        status = 2
    elif game.finished:
        status = 1
    else:
        status = 0

    return state, status


def get_game_from_agent(level_size: int, n_dims: int, model_name: str, train_timesteps: int, num_episodes: int):
    """
    Returns `num_episodes` simulated games using an agent trained under the specified configuration.
    Returned list is of shape (num_episodes, num_timesteps, *) where * is the shape of the game's state matrix.
    Assumes an agent with the appropriate configuration has been already trained. Otherwise, an
    exception is raised.
    """
    # TODO: Optimize space complexity using single timesteps with diffs
    model_class = get_model_class(model_name)
    model_path = get_model_path(model_name, n_dims, level_size, train_timesteps)
    model = model_class.load(model_path)
    eval_env = Ouroboros(level_size, n_dims, render_mode="hydra")
    evaluate_policy(model, eval_env, n_eval_episodes=num_episodes, render=True)
    
    relevant_history = eval_env.history[1:num_episodes+1]
    for i, episode_history in enumerate(relevant_history):
        relevant_history[i] = [obs.tolist() for obs in episode_history]

    return relevant_history


def get_available_agent_configurations():
    """
    Returns the list of trained agent configurations that ready to be visualized.
    """
    # TODO
    pass


if __name__ == "__main__":
    MODEL_NAME = "ppo"
    N_DIMS = 2
    LEVEL_SIZE = 5
    TRAIN_TIMESTEPS = 5_000_000

    get_game_from_agent(level_size=LEVEL_SIZE, n_dims=N_DIMS, model_name=MODEL_NAME,
                              train_timesteps=TRAIN_TIMESTEPS, num_episodes=1)
