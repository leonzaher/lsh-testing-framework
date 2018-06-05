from .stats import Stats


class Metrics(object):
    def __init__(self, stats: Stats, lsh_threshold: float):
        self.precision = calculate_precision(stats)
        self.recall = calculate_recall(stats)
        self.f1 = calculate_f1(stats)

        self.lsh_threshold = lsh_threshold


def calculate_precision(stats: Stats) -> float:
    return stats.true_positive / (stats.true_positive + stats.false_positive)


def calculate_recall(stats: Stats) -> float:
    return stats.true_positive / (stats.true_positive + stats.false_negative)


def calculate_f1(stats: Stats) -> float:
    precision = calculate_precision(stats)
    recall = calculate_recall(stats)

    return (2 * precision * recall) / (precision + recall)
