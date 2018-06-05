from typing import List


class AlgorithmResult(object):
    def __init__(self, index: int, predicted_indexes: List[int]):
        self.index = index
        self.predicted_indexes = predicted_indexes

    def __str__(self):
        return "AlgorithmResult(index = {}, predicted_indexes = {}"\
            .format(self.index, self.predicted_indexes)

    def __repr__(self):
        return self.__str__()
