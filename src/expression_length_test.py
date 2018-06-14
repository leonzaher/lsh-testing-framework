from submodules.MathDataGenerator.data_generator.generator_settings import GeneratorSettings
from submodules.MathDataGenerator.data_generator.recursive_descent_generator import Generator
from submodules.MathDataGenerator.error_generator.generate_errors import ErrorGenerator
from lib.metric_analysis.stats import Stats
from lib.metric_analysis.metrics import Metrics
from lib.plotter import *

from simhash import Simhash
from datasketch import MinHash
from collections import namedtuple
import random
import itertools

expression_data = namedtuple('Expression', ['expression', 'duplicate_of'])

hashes = dict()  # dict of hashes: {expression_data: hash}
test_results = dict()  # {expression_length: {}}

# test settings
start_length = 50
end_length = 200
expressions_per_length = 25

duplicates_count = 2  # how many duplicates should be created out of each original
error_percent_min = 10
error_percent_max = 30

lsh_threshold_percent = 7

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


def minhash(tokens):
    minhash = MinHash()

    for token in tokens:
        minhash.update(token.encode('utf8'))

    return minhash


def tokenize_string(string, token_size):
    return [string[i:i + token_size] for i in range(max(len(string) - token_size + 1, 1))]


def generate_data(length):
    result = list()

    for _ in range(expressions_per_length):
        expression = expression_data(generator.generate_expression(length), None)

        result.append(expression)

    duplicates = list()

    for original_expression in result:
        for _ in range(duplicates_count):
            error_percent = random.randrange(error_percent_min, error_percent_max)
            error_count = int(round(error_percent / 100. * length))

            duplicate_str = error_generator.generate_errors(original_expression.expression, error_count)

            new_expression = expression_data(duplicate_str, original_expression)

            duplicates.append(new_expression)

    result.extend(duplicates)

    return result


def expression_length_test():
    for expression_length in range(start_length, end_length + 1):
        print("Running tests for expression length {}...".format(expression_length))

        expressions = generate_data(expression_length)
        stats = Stats()

        for expression in expressions:
            hashes[expression] = minhash(tokenize_string(expression.expression, 5))

        for expression1, expression2 in itertools.combinations(expressions, 2):
            predicted_duplicate = hashes[expression1].jaccard(hashes[expression2]) < \
                                  int(round(lsh_threshold_percent / 100. * expression_length))

            if predicted_duplicate and (expression1.duplicate_of == expression2 or expression2.duplicate_of == expression1):
                stats.true_positive += 1

            if predicted_duplicate and (expression1.duplicate_of != expression2 and expression2.duplicate_of != expression1):
                stats.false_positive += 1

            if not predicted_duplicate and (expression1.duplicate_of != expression2 and expression2.duplicate_of != expression1):
                stats.true_negative += 1

            if not predicted_duplicate and (expression1.duplicate_of == expression2 or expression2.duplicate_of == expression1):
                stats.false_negative += 1

        metrics = Metrics(stats)

        test_results[expression_length] = metrics

    plot_metrics(test_results, "expression length")


if __name__ == '__main__':
    expression_length_test()
