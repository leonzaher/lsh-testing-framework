from datasketch import MinHash, MinHashLSH
from nltk import ngrams


def minhash(expression_list: list, threshold: float) -> list:
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

        # print("Candidates with Jaccard similarity >", threshold, "for input", i, ":", result)

    return results_list