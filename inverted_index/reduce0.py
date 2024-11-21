#!/usr/bin/env python3
"""Reduce 0."""
import sys

def main():
    total = 0
    for line in sys.stdin:
        total += 1

    print(total)  

if __name__ == "__main__":
    main()