#!/usr/bin/env python3
"""Reduce 2: Calculate IDF and prepare document info."""
import sys
import math

# TODO: consider edge cases

def main():
    """Do more stuff."""
    current_term = None
    term_docs = []

    # Get total document count N
    with open("total_document_count.txt", "r", encoding='utf-8') as f:
        n = int(f.read().strip()) # total number of documents

    for line in sys.stdin: # of the form term: doc_id tf ik OR tk: di tfik
        term, value = line.strip().split('\t')
        doc_id, tf = value.split()
        tf = int(tf) # term frequency in that document tf ik

        if current_term != term:
            if current_term is not None:
                # Calculate and emit for previous term
                n_k = len(term_docs)  # number of docs containing term
                idf = math.log10(n / n_k)
                for doc, freq in sorted(term_docs):
                    print(f"{doc}\t{current_term} {freq} {idf}")
            current_term = term
            term_docs = []

        term_docs.append((doc_id, tf))

    # Handle last term
    if current_term is not None:
        n_k = len(term_docs)
        idf = math.log10(n / n_k)
        for doc, freq in sorted(term_docs):
            print(f"{doc}\t{current_term} {freq} {idf}")


if __name__ == "__main__":
    main()


# Code I wrote to be consistent with the reduce template from madoop.
# This code is good, should work. I think. - Mitul

# #!/usr/bin/env python3
# """
# Reduce 2: Calculate IDF and prepare document info.

# https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
# """
# import sys
# import math
# import itertools


# def reduce_one_group(term, group):
#     """Reduce one group of lines with the same term."""
#     # Get total document count N
#     with open("total_document_count.txt", "r", encoding="utf-8") as f:
#         n = int(f.read().strip())  # Total number of documents

#     term_docs = []

#     # Parse the lines in the group
#     for line in group:
#         _, value = line.strip().split("\t")
#         doc_id, tf = value.split()
#         tf = int(tf)  # Term frequency in that document
#         term_docs.append((doc_id, tf))

#     # Calculate IDF for the term
#     n_k = len(term_docs)  # Number of docs containing term
#     idf = math.log10(n / n_k)

#     # Emit results for each document containing the term
#     for doc, freq in sorted(term_docs):
#         print(f"{doc}\t{term} {freq} {idf}")


# def keyfunc(line):
#     """Return the key from a TAB-delimited key-value pair."""
#     return line.partition("\t")[0]


# def main():
#     """Divide sorted lines into groups that share a key."""
#     for key, group in itertools.groupby(sys.stdin, keyfunc):
#         reduce_one_group(key, group)


# if __name__ == "__main__":
#     main()
