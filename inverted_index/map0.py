#!/usr/bin/env python3
"""Map 0: Count documents in collection."""
import sys

# DO: Include a newline at the end of every line of map output,
# and every line of reduce output.
# Does this mean we should add an extra \n?
# Python adds a newline character by default, so no need for another right?


def main():
    """Count number of HTML documents."""
    for line in sys.stdin:
        if "<!DOCTYPE html>" in line:
            # Emit 1 for each document found
            print("key\t1")


if __name__ == "__main__":
    main()
