#!/usr/bin/env python3
"""Map 3: Group by partition and prepare for normalization."""
import sys


def main():
    """Loop through lines."""
    for line in sys.stdin:
        doc_id, rest = line.strip().split('\t')
        term, tf, idf = rest.split()

        # Use doc_id % 3 as partition key
        partition_key = int(doc_id) % 3
        print(f"{partition_key}\t{term} {doc_id} {tf} {idf}")


if __name__ == "__main__":
    main()
