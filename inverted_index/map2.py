#!/usr/bin/env python3
"""Map 2: Count terms in documents."""
import sys


def main():
    """Stuff."""
    # Load stopwords
    # whats this??
    with open("stopwords.txt", "r", encoding='utf-8') as f:
        stopwords = set(line.strip() for line in f)

    for line in sys.stdin:
        doc_id, content = line.strip().split('\t')
        terms = content.lower().split()

        # Count term frequencies
        term_counts = {}
        for term in terms:
            if term not in stopwords:
                term_counts[term] = term_counts.get(term, 0) + 1

        # Emit with term as key for grouping
        for term, count in term_counts.items():  # Use .items() here
            print(f"{term}\t{doc_id} {count}")


if __name__ == "__main__":
    main()
