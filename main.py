from bin.generator_settings import GeneratorSettings
from bin.distributions.uniform import UniformDistribution
from bin.distributions.normal import NormalDistribution
from bin import data_generator


def generate_sample_data() -> list:
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
    data = generate_sample_data()

    print(data)


if __name__ == '__main__':
    main()
