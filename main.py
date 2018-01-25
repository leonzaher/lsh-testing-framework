import numpy

from typing import List

from bin.data_generator.generator_settings import GeneratorSettings
from bin.distributions.uniform import UniformDistribution
from bin.distributions.normal import NormalDistribution

from bin import plotter
from bin.data_generator import data_generator
from bin.algorithms import minhash
from bin.metric_analysis import calculate_stats
from bin.metric_analysis.stats import Stats
from bin.metric_analysis.metrics import Metrics
from bin.data_generator.expression_data import ExpressionData


def generate_sample_data() -> List[ExpressionData]:
    generator_settings: GeneratorSettings = GeneratorSettings()

    numbers_d = NormalDistribution(mean=10, stddev=2)
    lengths_d = UniformDistribution(minimum=100, maximum=150)
    duplicates_count_d = UniformDistribution(minimum=0, maximum=5)
    mistakes_count_d = NormalDistribution(mean=10, stddev=3)

    operators: list = ["*", "/", "+", "-"]

    generator_settings.set_numbers_length_distribution(numbers_d)
    generator_settings.set_length_distribution(lengths_d)
    generator_settings.set_duplicates_count_distribution(duplicates_count_d)
    generator_settings.set_mistake_count_distribution(mistakes_count_d)
    generator_settings.set_operators_list(operators)

    data = data_generator.generate_data(generator_settings, 10)

    data_generator.write_data_to_file(generator_settings, data, "output.txt")

    return data


def main():
    data: List[ExpressionData] = generate_sample_data()

    expression_list = [expression_data.expression for expression_data in data]

    metrics_list: List[Metrics] = []

    for threshold in numpy.arange(0.0, 0.5, 0.01):
        results = minhash.minhash(expression_list, threshold)

        stats: Stats = calculate_stats.calculate_stats(data, results)

        metrics: Metrics = Metrics(stats, threshold)

        metrics_list.append(metrics)

    plotter.plot_metrics_list(metrics_list)


if __name__ == '__main__':
    main()
