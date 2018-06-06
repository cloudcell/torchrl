import torch
import numpy as np
import random
import gym

from torchrl.learners import BaseLearner
from torchrl.episode_runner import EpisodeRunner


def set_seeds(seed):
  """
  Set the seed value for PyTorch, NumPy and Python.
  Important for reproducible runs!
  :param seed: seed value
  :return:
  """
  if seed is None:
    return
  torch.manual_seed(seed)
  torch.cuda.manual_seed_all(seed)
  np.random.seed(seed)
  random.seed(seed)


def get_gym_spaces(env_id: str):
  """
  A utility function to get observation and actions spaces of a
  Gym environment
  :param env_id: Environment ID of a Gym registered environment
  :return: gym.Spaces
  """
  env = gym.make(env_id)
  observation_space = env.observation_space
  action_space = env.action_space
  env.close()
  return observation_space, action_space


def eval_gym_env(args, agent: BaseLearner):
  """
  Evaluate an agent and return the average reward some trials
  :param args:
  :param agent:
  :return:
  """
  env = gym.make(args.env)
  runner = EpisodeRunner(env, max_steps=args.max_episode_steps)
  rewards = []
  for _ in range(args.num_eval):
    runner.reset()
    _, _, reward_history, _, _ = runner.collect(agent, store=True)
    rewards.append(np.sum(reward_history, axis=0))
  runner.stop()

  return np.average(rewards)
