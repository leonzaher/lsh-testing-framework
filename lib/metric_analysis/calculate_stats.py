import collections

from typing import List

from .stats import Stats


def calculate_stats(data: List[ExpressionData], algorithm_results: list) -> Stats:
    """
    true_positive: if index is in predicted_indexes and in true_indexes
    false_positive: if index is in predicted_indexes and not in true_indexes
    false_negative: if index is not in predicted_indexes and is in true_indexes

    :param data:
    :param algorithm_results:
    :return:
    """
    stats: Stats = Stats()

    for prediction in algorithm_results:
        extracted_indexes = extract_indexes(data, prediction)

        predicted_indexes = extracted_indexes.predicted_indexes
        true_indexes = extracted_indexes.true_indexes

        # we need to clone the true_indexes list so we can count the false_negatives
        # count of false negatives = len(true_indexes) - len(predicted_indexes)
        # this list is used just for optimization
        false_negative_indexes = true_indexes[:]

        # calculates stats from extracted data
        for index in predicted_indexes:
            if index in true_indexes:
                stats.true_positive += 1
                false_negative_indexes.remove(index)
            else:
                stats.false_positive += 1

        stats.false_negative += len(false_negative_indexes)

    return stats


def extract_indexes(data: List[ExpressionData], prediction: AlgorithmResult):
    """
    Used for extracting predicted indexes from the prediction map and true indexes from data list
    """
    current_index: int = prediction.index

    current_data = data[current_index]

    true_indexes = []

    if current_data.is_duplicate:
        # we know this expression is a duplicate and that it has a parent
        parent_index = current_data.parent_index
    else:
        # we know this expression is a parent
        parent_index = current_data.index

    for element in data:
        if element.is_duplicate and element.parent_index == parent_index and element.index != current_index:
            true_indexes.append(element.index)

    true_indexes.append(parent_index)

    ReturnResult = collections.namedtuple("ReturnResult", ["true_indexes", "predicted_indexes"])

    return ReturnResult(true_indexes=true_indexes, predicted_indexes=prediction.predicted_indexes)
