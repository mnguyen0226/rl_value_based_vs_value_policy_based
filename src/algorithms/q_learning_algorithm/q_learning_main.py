# Implementation of Bipedal Walking with Q Learning
# By Minh Nguyen
# ECE 5984 - Reinforcement Learning
# 11/20/2021

# Reference: https://github.com/sweetice/Deep-reinforcement-learning-with-pytorch

import numpy as np
import gym
import time
import matplotlib.pyplot as plt
from collections import defaultdict
from algorithms.q_learning_algorithm import q_learning


def q_learning_main():
    """Q-LEARNING ALGORITHM"""
    # log training date
    localtime = time.asctime(time.localtime(time.time()))
    with open("assets/training_times/q_learning_algorithm/training_time.txt", "a") as f:
        f.write(localtime)
        f.write("----------\n")

    # create a list of learning rate
    alpha_list = [0.0001, 0.001, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9]
    color_list = [
        "black",
        "red",
        "yellow",
        "green",
        "aqua",
        "darkblue",
        "orange",
        "pink",
    ]

    # plot
    plot = plt.figure()
    subplot = plot.add_subplot()

    # run all experimental learning rate
    for i in range(len(alpha_list)):
        t0 = time.time()  # for logging training time

        # initialize hyperparameters
        highest_reward = -400
        num_episodes = 1000  # number of episode
        gamma = 0.99  # discount factor

        env = gym.make("BipedalWalker-v2")
        q_table = defaultdict(lambda: np.zeros((10, 10, 10, 10)))

        # plot
        xval, yval = [], []
        plt.xlabel("Number Episodes")
        plt.ylabel("Rewards")
        plt.title(
            "Bipedal Walker v2\nQ-Learning Rewards vs Number Episodes\nwith gamma=0.99, num_episodes=1000"
        )
        string_label = "λ = " + str(alpha_list[i])
        (plotLine,) = subplot.plot(xval, yval, color_list[i], label=string_label)
        subplot.set_xlim([0, num_episodes])
        subplot.set_ylim([-220, -60])

        # for each episode do
        for j in range(1, num_episodes + 1):

            # run the q-learning, collect rewards and highest reward
            curr_episode_reward, highest_reward = q_learning(
                env=env,
                num_episode=j,
                q_table=q_table,
                highest_reward=highest_reward,
                alpha=alpha_list[i],
                gamma=gamma,
                render=False,
            )
            print(f"Episode {j} finished. Highest reward: {highest_reward}")

            # if agent was able to get the highest rewards of 300, then log the episode number
            if highest_reward >= 300.0:
                with open(
                    "assets/log_episodes_300_rewards/q_learning_algorithm/log_300.txt",
                    "a",
                ) as f:
                    f.write(
                        "Episode "
                        + str(j)
                        + " of learning rate "
                        + str(alpha_list[i])
                        + " has the reward of "
                        + str(highest_reward)
                        + ".\n"
                    )
                    f.close()

            # append plot
            xval.append(j - 1)
            yval.append(curr_episode_reward)
            plotLine.set_xdata(xval)
            plotLine.set_ydata(yval)
            plot.savefig("./results/q_learning_max_reward")

        # plot legend upper right of the graph
        plot.legend(loc="upper right")

        t1 = time.time()
        print(f"All episodes finished. Training time of Q Learning is: {t1-t0}")

        # write training time to file
        with open(
            "assets/training_times/q_learning_algorithm/training_time.txt", "a"
        ) as f:
            f.write(
                "- The training time for 1000 episode of Q-Learning with the learning rate of "
            )
            f.write(str(alpha_list[i]))
            f.write(" is: ")
            f.write(str(t1 - t0))
            f.write(" seconds.\n")
            f.close()
