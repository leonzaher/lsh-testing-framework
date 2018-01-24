import random
import math
import string

from .generator_settings import GeneratorSettings


def generate_duplicates(generator_settings: GeneratorSettings, expression_data: map) -> map:
    duplicate: str = expression_data["expression"]

    mistakes_count = generator_settings.mistake_count_distribution.random()

    for j in range(0, mistakes_count):
        mistake_index: int = random.randint(0, len(duplicate) - 1)

        allowed_chars: list = list(string.digits) + generator_settings.operators_list
        # remove the character duplicate[mistake_index] so it doesn't get chosen
        allowed_chars.remove(duplicate[mistake_index])

        substitute_char: chr = random.choice(allowed_chars)

        # replace the character on mistake_index with substitute_char
        duplicate = duplicate[:mistake_index] + substitute_char + duplicate[mistake_index + 1:]

    data_map = {"expression": duplicate, "is_duplicate": True, "original": expression_data["expression"],
                "parent_index": expression_data["index"]}

    return data_map


def generate_string(generator_settings: GeneratorSettings) -> map:
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

    data_map = {"expression": expression, "is_duplicate": False}

    return data_map


def generate_data(generator_settings: GeneratorSettings, max_items: int) -> list:
    """
        Generate data in the form of strings. Data is generated using the generate_string function.
        Data is represented as a list of maps of format {"expression": str, "isDuplicate": boolean, "original": str}
    """

    data = []

    for i in range(0, max_items):
        expression_data = generate_string(generator_settings)
        expression_index = len(data)
        expression_data["index"] = expression_index

        data.append(expression_data)

        duplicates_count = generator_settings.duplicates_count_distribution.random()

        for j in range(0, duplicates_count):
            duplicate_data = generate_duplicates(generator_settings, expression_data)
            duplicate_data["index"] = len(data)
            data.append(duplicate_data)

    print(data)

    return data


def write_data_to_file(generator_settings: GeneratorSettings, data: list, filepath: str):
    file = open(filepath, 'w')

    line_index = 0

    for map in data:
        if not map["is_duplicate"]:
            file.write(generator_settings.delimiter)

        line = str(line_index) + " " + map["expression"]

        line = line + generator_settings.delimiter

        file.write(line)

        line_index += 1

    file.close()
