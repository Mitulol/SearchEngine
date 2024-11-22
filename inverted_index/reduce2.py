#!/usr/bin/env python3
"""Reduce 2: Calculate IDF and prepare document info."""
import sys
import math


def main():
    """Do more stuff."""
    current_term = None
    term_docs = []

    # Get total document count N
    with open("total_document_count.txt", "r", encoding='utf-8') as f:
        n = int(f.read().strip())

    for line in sys.stdin:
        term, value = line.strip().split('\t')
        doc_id, tf = value.split()
        tf = int(tf)

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
