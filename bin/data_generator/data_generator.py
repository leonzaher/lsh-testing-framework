import random
import math
import string

from typing import List

from bin.data_generator.generator_settings import GeneratorSettings
from .expression_data import ExpressionData


def generate_duplicate(generator_settings: GeneratorSettings, expression_data: ExpressionData,
                       index: int) -> ExpressionData:
    duplicate: str = expression_data.expression

    mistakes_count = generator_settings.mistake_count_distribution.random()

    for j in range(0, mistakes_count):
        mistake_index: int = random.randint(0, len(duplicate) - 1)

        allowed_chars: list = list(string.digits) + generator_settings.operators_list
        # remove the character duplicate[mistake_index] so it doesn't get chosen
        allowed_chars.remove(duplicate[mistake_index])

        substitute_char: chr = random.choice(allowed_chars)

        # replace the character on mistake_index with substitute_char
        duplicate = duplicate[:mistake_index] + substitute_char + duplicate[mistake_index + 1:]

    return ExpressionData(expression=duplicate, index=index, is_duplicate=True,
                          parent_expression=expression_data.expression, parent_index=expression_data.index)


def generate_string(generator_settings: GeneratorSettings, index: int) -> ExpressionData:
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

    return ExpressionData(expression=expression, index=index, is_duplicate=False,
                          parent_expression=None, parent_index=None)


def generate_data(generator_settings: GeneratorSettings, max_original_expressions: int) -> List[ExpressionData]:
    """
        Generate data in the form of strings. Data is generated using the generate_string function.
        Data is represented as a list of maps of format {"expression": str, "isDuplicate": boolean, "original": str}
    """

    data = []

    for i in range(0, max_original_expressions):
        expression_index = len(data)
        expression_data = generate_string(generator_settings, expression_index)

        data.append(expression_data)

        duplicates_count = generator_settings.duplicates_count_distribution.random()

        for j in range(0, duplicates_count):
            duplicate_data = generate_duplicate(generator_settings, expression_data, expression_index + j + 1)
            data.append(duplicate_data)

    print(data)

    return data


def write_data_to_file(generator_settings: GeneratorSettings, data: List[ExpressionData], filepath: str):
    file = open(filepath, 'w')

    for expression_data in data:
        if not expression_data.is_duplicate:
            file.write(generator_settings.delimiter)

        line = str(expression_data.index) + " " + expression_data.expression

        line = line + generator_settings.delimiter

        file.write(line)

    file.close()
