from .distributions.abstract_distribution import AbstractDistribution


class GeneratorSettings(object):
    """
    Class representing settings for data generator.
    """

    def __init__(self):
        self.mistake_count_distribution: AbstractDistribution = None
        self.length_distribution: AbstractDistribution = None
        self.duplicates_count_distribution: AbstractDistribution = None
        self.numbers_length_distribution: AbstractDistribution = None

        self.operators_list: list = None

        self.default_string_delimiter = "\n"
        self.default_line_delimiter = "\n\n"

    def set_mistake_count_distribution(self, distribution: AbstractDistribution):
        self.mistake_count_distribution = distribution

    def set_length_distribution(self, distribution: AbstractDistribution):
        self.length_distribution = distribution

    def set_duplicates_count_distribution(self, distribution: AbstractDistribution):
        self.duplicates_count_distribution = distribution

    def set_numbers_length_distribution(self, distribution: AbstractDistribution):
        self.numbers_length_distribution = distribution

    def set_operators_list(self, operators_list: list):
        self.operators_list = operators_list
