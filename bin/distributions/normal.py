from numpy import random

from .abstract_distribution import AbstractDistribution


class NormalDistribution(AbstractDistribution):

    def __init__(self, mean, stddev):
        self.mean = mean
        self.stddev = stddev

    def random(self) -> int:
        s = random.normal(self.mean, self.stddev, 1)

        return int(s[0])
