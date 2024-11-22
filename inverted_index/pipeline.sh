#!/bin/bash
set -Eeuo pipefail

# Optional input directory argument
PIPELINE_INPUT=crawl
if [ -n "${1-}" ]; then
  PIPELINE_INPUT="$1"
fi

# Print commands
set -x

# Remove output directories
rm -rf output output[0-9]
rm -rf index_server/index/inverted_index

# Job 0: Document Count
madoop \
  -input ${PIPELINE_INPUT} \
  -output output0 \
  -mapper ./map0.py \
  -reducer ./reduce0.py

# Copy document count to a separate file
cp output0/part-00000 total_document_count.txt

# Job 1: Parsing
madoop \
  -input ${PIPELINE_INPUT} \
  -output output1 \
  -mapper ./map1.py \
  -reducer ./reduce1.py

# Job 2
madoop \
  -input output1 \
  -output output2 \
  -mapper ./map2.py \
  -reducer ./reduce2.py

# Job 3 (with partitioner)
madoop \
  -input output2 \
  -output output3 \
  -mapper ./map3.py \
  -reducer ./reduce3.py \
  -partitioner ./partition.py \
  -numReduceTasks 3


#idk if we need this bottom part mitul??? but we have it here lol
# Create directory for index server files
mkdir -p index_server/index/inverted_index

# Copy output files to index server directory
for i in {0..2}; do
  if [ -f "output3/part-0000${i}" ]; then
    cp "output3/part-0000${i}" "index_server/index/inverted_index/inverted_index_${i}.txt"
  fi
done