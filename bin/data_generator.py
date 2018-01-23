import random
import math
import string

from .generator_settings import GeneratorSettings


def generate_duplicates(generator_settings: GeneratorSettings, expression: str) -> list:
    duplicates = []

    duplicates_count = generator_settings.duplicates_count_distribution.random()

    for i in range(0, duplicates_count):
        duplicate: str = expression

        mistakes_count = generator_settings.mistake_count_distribution.random()

        for j in range(0, mistakes_count):
            mistake_index: int = random.randint(0, len(duplicate) - 1)

            allowed_chars: list = list(string.digits) + generator_settings.operators_list
            # remove the character duplicate[mistake_index] so it doesn't get chosen
            allowed_chars.remove(duplicate[mistake_index])

            substitute_char: chr = random.choice(allowed_chars)

            # replace the character on mistake_index with substitute_char
            duplicate = duplicate[:mistake_index] + substitute_char + duplicate[mistake_index + 1:]

        duplicates.append(duplicate)

    return duplicates


def generate_string(generator_settings: GeneratorSettings) -> list:
    max_length = generator_settings.length_distribution.random()

    expression: str = ""

    while len(expression) <= max_length:

        operator: str = random.choice(generator_settings.operators_list)

        number_length: int = generator_settings.numbers_length_distribution.random()

        # number length cannot be 0
        if number_length <= 0:
            number_length = 1

        # string cannot be longer than max_length so we must scale the last number
        if len(expression) + number_length > max_length:
            number_length = max_length - len(expression)

        # calculate max number based on the length of the number
        max_number = math.pow(10, number_length)

        number: str = str(random.randint(0, max_number))

        expression = expression + number

        if len(expression) < max_length:
            expression = expression + operator

    return [expression] + generate_duplicates(generator_settings, expression)


def generate_data(generator_settings: GeneratorSettings, max_items: int, output_file: str):
    """
        Generate data in the form of strings. Data is generated using the generate_string function.
        Data is written to output file.
    """

    file = open(output_file, 'w')

    for i in range(0, max_items):
        string_list: list = generate_string(generator_settings)

        line = generator_settings.default_string_delimiter.join(string_list) + generator_settings.default_line_delimiter

        file.write(line)

    file.close()
