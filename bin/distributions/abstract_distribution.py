from abc import ABC, abstractmethod


class AbstractDistribution(ABC):
    @abstractmethod
    def random(self) -> int:
        pass
