from numpy import random

from .abstract_distribution import AbstractDistribution


class UniformDistribution(AbstractDistribution):

    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def random(self) -> int:
        s = random.uniform(self.minimum, self.maximum, 1)

        return int(s[0])
