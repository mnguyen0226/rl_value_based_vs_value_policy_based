from collections import namedtuple
import random

# Explanation: https://deeplizard.com/learn/video/Bcuj2fTH4_4
# Reference: https://github.com/ziguiyingcang/Deep-Reinforcement-Learning-for-Traffic-Signal-Control/blob/main/agent_3DQN_PSER.py

TransitionVal = namedtuple(
    "Transition", ("state", "action", "mask", "next_state", "reward")
)


class Memory(object):
    def __init__(self):
        """Constructor"""
        self.memory = []

    def push(self, *arg):
        """Push transition to memory"""
        self.memory.append(TransitionVal(*arg))

    def sample(self, batch_size=None):
        """Sampling data from batch size

        Args:
            batch_size: batch size. Defaults to None.

        Returns:
            Transition values batch
        """
        if batch_size is None:
            return TransitionVal(*zip(*self.memory))
        else:
            random_batch = random.sample(self.memory, batch_size)
            return TransitionVal(*zip(*random_batch))

    def append(self, new_memory):
        """Append new memory to memory array

        Args:
            new_memory: new memory value
        """
        self.memory += new_memory.memory

    def __len__(self):
        """Overrided len() of array

        Returns:
            Len of memory array
        """
        return len(self.memory)
