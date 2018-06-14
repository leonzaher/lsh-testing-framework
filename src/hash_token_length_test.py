from submodules.MathDataGenerator.data_generator.generator_settings import GeneratorSettings
from submodules.MathDataGenerator.data_generator.recursive_descent_generator import Generator
from submodules.MathDataGenerator.error_generator.generate_errors import ErrorGenerator
from lib.metric_analysis.stats import Stats
from lib.metric_analysis.metrics import Metrics
from lib.plotter import *

import matplotlib.pyplot as plt
import numpy as np
from simhash import Simhash
from collections import namedtuple
import random
import itertools

expression_data = namedtuple('Expression', ['expression', 'duplicate_of'])

test_results = dict()  # {expression_length: {}}

# test settings
original_expressions = 100
expression_length_dist = (250, 20)
duplicates_count_dist = (2, 1)
error_count_dist = (4, 3)

hash_threshold = 7

hash_token_size_range = (2, 20)

generator_settings = GeneratorSettings(
    operators=['+', '-', '*', '/'],
    variables=['x', 'y', 'z'],
    functions=['sin', 'cos', 'tan'],
    max_depth=4
)

generator_settings.set_generation_probability(descentP=0.3, expressionP=0.4, closeP=0.3)
generator_settings.set_number_vs_variable_probability(numberP=0.7)

generator = Generator(generator_settings)

error_generator = ErrorGenerator(
    "/home/leonzaher/PycharmProjects/LSHTestingFramework/submodules/MathDataGenerator/error_generator/default_probabilities_map")


def tokenize_string(string, token_size):
    return [string[i:i + token_size] for i in range(max(len(string) - token_size + 1, 1))]


def generate_data():
    print("Generating data...")

    result = list()

    for _ in range(original_expressions):
        expression_length = int(round(random.normalvariate(expression_length_dist[0], expression_length_dist[1])))
        expression = expression_data(generator.generate_expression(expression_length), None)

        result.append(expression)

    duplicates = list()

    for original_expression in result:

        duplicates_count = int(round(random.normalvariate(duplicates_count_dist[0], duplicates_count_dist[1])))
        if duplicates_count < 0:
            duplicates_count = 0

        for _ in range(duplicates_count):
            error_count = int(round(random.normalvariate(error_count_dist[0], error_count_dist[1])))
            if error_count <= 0:
                error_count = 1

            duplicate = error_generator.generate_errors(original_expression.expression, error_count)

            dup_expression = expression_data(duplicate, original_expression)

            duplicates.append(dup_expression)

    result.extend(duplicates)

    print("Generated total {} expressions.\n".format(len(result)))

    return result



def expression_length_test():
    expressions = generate_data()

    for token_size in range(hash_token_size_range[0], hash_token_size_range[1] + 1):
        print("Calculating stats for token size {}...".format(token_size))

        hashes = dict()
        stats = Stats()

        for expression in expressions:
            hashes[expression] = Simhash(tokenize_string(expression.expression, token_size))

        for expression1, expression2 in itertools.combinations(expressions, 2):
            predicted_duplicate = hashes[expression1].distance(hashes[expression2]) < \
                                  int(round(hash_threshold / 100. *
                                            (len(expression1.expression) + len(expression2.expression)) / 2))

            if predicted_duplicate and (
                    expression1.duplicate_of == expression2 or expression2.duplicate_of == expression1):
                stats.true_positive += 1

            if predicted_duplicate and (
                    expression1.duplicate_of != expression2 and expression2.duplicate_of != expression1):
                stats.false_positive += 1

            if not predicted_duplicate and (
                    expression1.duplicate_of != expression2 and expression2.duplicate_of != expression1):
                stats.true_negative += 1

            if not predicted_duplicate and (
                    expression1.duplicate_of == expression2 or expression2.duplicate_of == expression1):
                stats.false_negative += 1

        metrics = Metrics(stats)

        test_results[token_size] = metrics

    plot_metrics(test_results, "Token size")


if __name__ == '__main__':
    expression_length_test()
