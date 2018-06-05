from datasketch import MinHash, MinHashLSH
from nltk import ngrams
from typing import List

from .algorithm_result import AlgorithmResult


def minhash(expression_list: List[str], threshold: float) -> List[AlgorithmResult]:
    lsh = MinHashLSH(threshold, num_perm=128)

    results_list: List[AlgorithmResult] = []

    # Create MinHash objects
    minhashes = {}
    for c, i in enumerate(expression_list):
        minhash = MinHash(num_perm=128)
        for d in ngrams(i, 3):
            minhash.update("".join(d).encode('utf-8'))
        lsh.insert(c, minhash)
        minhashes[c] = minhash

    for i in range(len(minhashes.keys())):
        predicted_indexes = lsh.query(minhashes[i])
        predicted_indexes.remove(i)

        result = AlgorithmResult(index=i, predicted_indexes=predicted_indexes)

        results_list.append(result)

    return results_list
