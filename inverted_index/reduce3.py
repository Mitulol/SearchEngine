#!/usr/bin/env python3
"""Reduce 3: Create final inverted index format."""
import sys
from collections import defaultdict


def calculate_norm_factor(doc_weights):
    """Calculate document normalization factor (sum of squared weights)."""
    sum_squares = 0
    for tf, idf in doc_weights.values():
        weight = float(tf) * float(idf)
        sum_squares += weight * weight
    return sum_squares


def main():
    """Do stuff."""
    current_partition = None
    term_info = defaultdict(list)  # term -> list of (docid, tf, idf)
    doc_weights = defaultdict(dict)  # docid -> {term: (tf, idf)}

    for line in sys.stdin:
        partition_key, rest = line.strip().split('\t')
        partition_key = int(partition_key)
        term, doc_id, tf, idf = rest.split()
        tf = int(tf)
        idf = float(idf)

        if current_partition != partition_key:
            if current_partition is not None:
                # Process all terms in the current partition
                for term in sorted(term_info.keys()):
                    parts = [term, str(term_info[term][0][2])]  # term and idf
                    for doc_id, tf, _ in sorted(term_info[term]):
                        doc_weights_for_id = doc_weights[doc_id]
                        norm_factor = calculate_norm_factor(doc_weights_for_id)

                        parts.extend([doc_id, str(tf), str(norm_factor)])
                    print(" ".join(parts))

            current_partition = partition_key
            term_info.clear()
            doc_weights.clear()

        term_info[term].append((doc_id, tf, idf))
        doc_weights[doc_id][term] = (tf, idf)

    # Handle last partition
    if current_partition is not None:
        for term in sorted(term_info.keys()):
            parts = [term, str(term_info[term][0][2])]  # term and idf
            for doc_id, tf, _ in sorted(term_info[term]):
                norm_factor = calculate_norm_factor(doc_weights[doc_id])
                parts.extend([doc_id, str(tf), str(norm_factor)])
            print(" ".join(parts))


if __name__ == "__main__":
    main()



# Code I wrote to be consistent with the reduce template from madoop.
# I haven't checked if this code is good.



#!/usr/bin/env python3
# """
# Reduce 3: Create final inverted index format.

# https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
# """x
# import sys
# from collections import defaultdict
# import itertools


# def calculate_norm_factor(doc_weights):
#     """Calculate document normalization factor (sum of squared weights)."""
#     sum_squares = 0
#     for tf, idf in doc_weights.values():
#         weight = float(tf) * float(idf)
#         sum_squares += weight * weight
#     return sum_squares


# def reduce_one_group(partition_key, group):
#     """Process one partition group."""
#     term_info = defaultdict(list)  # term -> list of (docid, tf, idf)
#     doc_weights = defaultdict(dict)  # docid -> {term: (tf, idf)}

#     for line in group:
#         _, rest = line.strip().split("\t")
#         term, doc_id, tf, idf = rest.split()
#         tf = int(tf)
#         idf = float(idf)

#         term_info[term].append((doc_id, tf, idf))
#         doc_weights[doc_id][term] = (tf, idf)

#     # Process all terms in the partition
#     for term in sorted(term_info.keys()):
#         parts = [term, str(term_info[term][0][2])]  # term and idf
#         for doc_id, tf, _ in sorted(term_info[term]):
#             norm_factor = calculate_norm_factor(doc_weights[doc_id])
#             parts.extend([doc_id, str(tf), str(norm_factor)])
#         print(" ".join(parts))


# def keyfunc(line):
#     """Return the partition key from a TAB-delimited key-value pair."""
#     return int(line.partition("\t")[0])


# def main():
#     """Divide sorted lines into groups that share a partition key."""
#     for partition_key, group in itertools.groupby(sys.stdin, keyfunc):
#         reduce_one_group(partition_key, group)


# if __name__ == "__main__":
#     main()



