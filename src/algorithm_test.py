from submodules.MathDataGenerator.data_generator.generator_settings import GeneratorSettings
from submodules.MathDataGenerator.data_generator.recursive_descent_generator import Generator
from submodules.MathDataGenerator.error_generator.generate_errors import ErrorGenerator
from lib.metric_analysis.stats import Stats
from lib.metric_analysis.metrics import Metrics

from simhash import Simhash
from datasketch import MinHash
from lib.nilsimsa import nilsimsa

import matplotlib.pyplot as plt
from collections import namedtuple
import random
import itertools
import numpy as np


expression_data = namedtuple('Expression', ['expression', 'duplicate_of'])

hashes = dict()  # {algorithm: {expression: hash}}

original_expression_count = 200
expression_length_dist = (100, 20)
duplicates_count_dist = (2, 1)
error_count_dist = (5, 5)

lsh_threshold_percent = 8


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


def minhash(tokens):
    minhash = MinHash()

    for token in tokens:
        minhash.update(token.encode('utf8'))

    return minhash


def generate_data():
    print("Generating data...")

    result = list()

    for _ in range(original_expression_count):
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

    print("Generated total {} expressions.".format(len(result)))

    return result


def calculate_stats(expressions):
    print("Calculating stats...")

    stats = {"simhash": Stats(), "minhash": Stats(), "nilsimsa": Stats()}

    for expression1, expression2 in itertools.combinations(expressions, 2):
        predictions = {"simhash": hashes[expression1]["simhash"].distance(hashes[expression2]["simhash"]) < \
                                  int(round(lsh_threshold_percent / 100. *
                                            (len(expression1.expression) + len(expression2.expression)) / 2)),
                       "minhash": hashes[expression1]["minhash"].jaccard(hashes[expression2]["minhash"]) < \
                                  int(round(lsh_threshold_percent / 100. *
                                            (len(expression1.expression) + len(expression2.expression)) / 2)),
                       "nilsimsa": hashes[expression1]["nilsimsa"].similarity(hashes[expression2]["nilsimsa"]) < \
                                   int(round(lsh_threshold_percent / 100. *
                                            (len(expression1.expression) + len(expression2.expression)) / 2))}

        for algorithm in predictions.keys():
            if predictions[algorithm] and (
                    expression1.duplicate_of == expression2 or expression2.duplicate_of == expression1):
                stats[algorithm].true_positive += 1

            if predictions[algorithm] and (
                    expression1.duplicate_of != expression2 and expression2.duplicate_of != expression1):
                stats[algorithm].false_positive += 1

            if not predictions[algorithm] and (
                    expression1.duplicate_of != expression2 and expression2.duplicate_of != expression1):
                stats[algorithm].true_negative += 1

            if not predictions[algorithm] and (
                    expression1.duplicate_of == expression2 or expression2.duplicate_of == expression1):
                stats[algorithm].false_negative += 1

    return {"simhash": Metrics(stats["simhash"]), "minhash": Metrics(stats["minhash"]),
                    "nilsimsa": Metrics(stats["nilsimsa"])}


def plot_results(test_results):
    fig, ax = plt.subplots()

    index = np.arange(3)
    bar_width = 0.25
    error_config = {'ecolor': '0.3'}

    simhash = [test_results["simhash"].precision, test_results["simhash"].recall, test_results["simhash"].f1]
    minhash = [test_results["minhash"].precision, test_results["minhash"].recall, test_results["minhash"].f1]
    nilsimsa = [test_results["nilsimsa"].precision, test_results["nilsimsa"].recall, test_results["nilsimsa"].f1]

    print("Simhash: ", simhash)
    print("Minhash: ", minhash)
    print("Nilsimsa: ", nilsimsa)

    rects1 = ax.bar(index, simhash, bar_width, color='b', error_kw=error_config, label='Simhash')

    rects2 = ax.bar(index + bar_width, minhash, bar_width, color='r', error_kw=error_config, label='Minhash')

    rects3 = ax.bar(index + bar_width * 2, nilsimsa, bar_width, color='g', error_kw=error_config, label='Nilsimsa')

    ax.set_xlabel('Score name')
    ax.set_ylabel('Scores')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(('Precision', 'Recall', 'F1'))
    ax.legend()

    fig.tight_layout()
    plt.show()


def algorithm_test():
    expressions = generate_data()

    print("Hashing...")

    for expression in expressions:
        hashes[expression] = dict()
        hashes[expression]["simhash"] = Simhash(tokenize_string(expression.expression, 3))
        hashes[expression]["minhash"] = minhash(tokenize_string(expression.expression, 3))
        hashes[expression]["nilsimsa"] = nilsimsa(expression.expression)

    test_results = calculate_stats(expressions)
    plot_results(test_results)


if __name__ == '__main__':
    algorithm_test()
