#!/usr/bin/env python3
"""Map 0: Count documents in collection."""
import sys


def main():
    """Count number of HTML documents."""
    for line in sys.stdin:
        if "<!DOCTYPE html>" in line:
            # Emit 1 for each document found
            print("key\t1")


if __name__ == "__main__":
    main()
