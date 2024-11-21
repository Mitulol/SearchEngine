#!/usr/bin/env python3
"""Map 0."""
import sys


def main():
    key = 0
    for line in sys.stdin:
        if "<!DOCTYPE html>" in line:
            print(f"{key}\t1")
            key += 1

if __name__ == "__main__":
    main()
