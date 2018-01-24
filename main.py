from bin.generator_settings import GeneratorSettings
from bin.distributions.uniform import UniformDistribution
from bin.distributions.normal import NormalDistribution
from bin import data_generator
from bin.metric_analysis import calculate_metrics
from bin.metric_analysis.stats import Stats

from datasketch import MinHash, MinHashLSH
from nltk import ngrams


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


def run_minhash(expression_list: list) -> list:
    threshold = 0.5

    lsh = MinHashLSH(threshold, num_perm=128)

    results_list = []

    # Create MinHash objects
    minhashes = {}
    for c, i in enumerate(expression_list):
        minhash = MinHash(num_perm=128)
        for d in ngrams(i, 3):
            minhash.update("".join(d).encode('utf-8'))
        lsh.insert(c, minhash)
        minhashes[c] = minhash

    for i in range(len(minhashes.keys())):
        result = lsh.query(minhashes[i])
        result.remove(i)

        result_map = {"index": i, "predicted": result}

        results_list.append(result_map)

        print("Candidates with Jaccard similarity >", threshold, "for input", i, ":", result)

    return results_list


def main():
    data = generate_sample_data()

    expression_list = [map["expression"] for map in data]

    results = run_minhash(expression_list)

    stats: Stats = calculate_metrics.calculate_stats(data, results)

    print("Precision is:", calculate_metrics.calculate_precision(stats))
    print("Recall is:", calculate_metrics.calculate_recall(stats))


if __name__ == '__main__':
    main()
