import gym
from torch.nn import MSELoss
from torch.optim import RMSprop

from torchrl.archs import SimplePolicyNet
from torchrl.learners import A2CLearner
from torchrl import EpisodeRunner

NUM_EPISODES = 350


class CartPoleLearner(A2CLearner):
    """
    A DeepQLearner with some reward shaping - penalize when the
    cart pole falls (i.e. episode ends)
    """
    def transition(self, episode_id, state, action, reward, next_state, done, action_log_prob):
        if done:
            reward = -1
        super(CartPoleLearner, self).transition(episode_id, state, action, reward, next_state, done, action_log_prob)


def main():
    env = gym.make('CartPole-v1')
    runner = EpisodeRunner(env, max_steps=1000)

    policy_net = SimplePolicyNet(env.observation_space.shape[0], env.action_space.n)

    mse_loss = MSELoss()
    rms_prop = RMSprop(policy_net.parameters(), lr=1e-3, weight_decay=0.99)

    learner = CartPoleLearner(policy_net, mse_loss, rms_prop, env.action_space.n,
                         gamma=0.9, eps_max=1.0, eps_min=0.1, temperature=2000.0)

    for i in range(1, NUM_EPISODES + 1):
        runner.reset()

        ##
        # Only running single step runs each time to count the rewards (stats are work in progress)
        # A better run for each episode would simply be
        # ```
        # while not runner.run(learner):
        #   pass
        # learner.learn()
        # ```
        #
        reward = 0
        while not runner.run(learner, steps=1):
            reward += 1
        learner.learn()

        if i % 10 == 0:
            print('Episode {}: {} steps'.format(i, reward))

    env.close()


if __name__ == '__main__':
    main()
