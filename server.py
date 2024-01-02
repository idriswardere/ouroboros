"""
Functions that facilitate the link between Ouroboros and the Hydra frontend.
"""
import os
import numpy as np
from stable_baselines3.common.evaluation import evaluate_policy

from ouroboros.level import Level
from ouroboros.game import Game
from ouroboros.environment import Ouroboros

from flask import jsonify
from flask import Flask
from flask_cors import CORS

from train import (get_model_path, 
                   get_model_class, 
                   get_model_configuration_from_filename)

app = Flask(__name__)
cors = CORS(app)

game = None


def get_game_diff(state: np.ndarray, next_state: np.ndarray) -> dict:
    """
    Returns a dict mapping changed indices in the game state to their updated values.
    """
    diff_indices = np.nonzero(state - next_state)
    result = {}

    flat_diff_indices = np.ravel_multi_index(diff_indices, dims=state.shape)
    for i, idx in enumerate(zip(*diff_indices)):
        flat_idx = int(flat_diff_indices[i])
        result[flat_idx] = int(next_state[idx])
    
    return result
        

@app.route("/init/<level_size>/<n_dims>")
def init_game(level_size: int, n_dims: int) -> None:
    """
    Initialize an Ouroboros game from frontend input.
    Returns initial game state.
    """
    # TODO: Investigate whether tokens are necessary for game initialization (and progressing)
    global game
    level_size = int(level_size)
    n_dims = int(n_dims)

    level = Level(level_size=level_size, n_dims=n_dims)
    game = Game(level=level)

    state = game.level.arr.tolist()
    result = {"state": state}

    return jsonify(result)


@app.route("/progress/<direction_int>")
def progress_game(direction_int: int) -> "tuple[list, int]":
    """
    Progress an Ouroboros game given an input direction.
    Returns state matrix as nested lists and game status. 
    Status map: 0: Playing, 1: Lost, 2: Won
    """
    global game
    direction_int = int(direction_int)

    direction = np.zeros(game.level.ndim, dtype=int)
    if direction_int > 0:
        direction[direction_int-1] = 1
    else:
        direction[abs(direction_int)-1] = -1

    state = game.level.arr.copy()

    game.change_direction(direction)
    game.move()
    
    next_state = game.level.arr
    diff_dict = get_game_diff(state, next_state)

    if game.won():
        status = 2
    elif game.finished:
        status = 1
    else:
        status = 0

    result = {
        "diff": diff_dict,
        "status": status,
    }

    return jsonify(result)


@app.route("/game_from_agent/<level_size>/<n_dims>/<model_name>/<train_timesteps>")
def get_game_from_agent(level_size: int, n_dims: int, model_name: str, train_timesteps: int):
    """
    Returns a simulated game using an agent trained under the specified configuration.
    Returned list is of shape (num_timesteps, *) where * is the shape of the game's state matrix.
    Assumes an agent with the appropriate configuration has been already trained. Otherwise, an
    exception is raised.
    """
    # TODO: Optimize space complexity using single timesteps with diffs
    level_size = int(level_size)
    n_dims = int(n_dims)
    train_timesteps = int(train_timesteps)

    model_class = get_model_class(model_name)
    model_path = get_model_path(model_name, n_dims, level_size, train_timesteps)
    model = model_class.load(model_path)
    eval_env = Ouroboros(level_size, n_dims, render_mode="hydra")
    evaluate_policy(model, eval_env, n_eval_episodes=1, render=True)
    
    states = eval_env.history[1]
    initial_state = states[0].tolist()

    diffs = []
    for i in range(len(states)-1):
        diffs.append(get_game_diff(states[i], states[i+1]))

    result = {
        "initial_state": initial_state,
        "diffs": diffs,
    }

    return jsonify(result)


@app.route("/available_agent_configurations")
def get_available_agent_configurations():
    """
    Returns the list of trained agent configurations that ready to be visualized.
    """
    model_configurations = []
    for filename in sorted(os.listdir("models")):
        model_path = os.path.join("models", filename)
        if os.path.isfile(model_path):
            configuration = list(get_model_configuration_from_filename(filename))
            model_configurations.append(configuration)

    result = {"configurations": model_configurations}

    return jsonify(result)


if __name__ == "__main__":
    MODEL_NAME = "ppo"
    N_DIMS = 2
    LEVEL_SIZE = 5
    TRAIN_TIMESTEPS = 5_000_000

    get_game_from_agent(level_size=LEVEL_SIZE, n_dims=N_DIMS, model_name=MODEL_NAME,
                              train_timesteps=TRAIN_TIMESTEPS, num_episodes=1)
