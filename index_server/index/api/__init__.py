# index/api/__init__.py
"""Init for api."""
import os
from pathlib import Path
import logging

# Global variables
STOPWORDS = set()
PAGERANK = {}
INVERTED_INDEX = {}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = True


def load_index():
    """Load inverted index, stopwords, and PageRank into memory."""
    # global STOPWORDS, PAGERANK, INVERTED_INDEX
    # Get the index directory path
    index_dir = Path(__file__).parent.parent
    # logger.debug(f"Index directory: {index_dir}")

    # Load stopwords
    # stopwords_path = index_dir / "stopwords.txt"
    # logger.debug(f"Loading stopwords from: {stopwords_path}")
    # # with open(stopwords_path, "r", encoding='utf-8') as f:
    # #     # logger.info(f"Opened this file!! Yay!")
    # #     STOPWORDS = set(f.read().splitlines())
    # if stopwords_path.exists():
    #     with open(stopwords_path, "r", encoding='utf-8') as f:
    #         STOPWORDS = set(f.read().splitlines())
    #     logger.info(f"Loaded {len(STOPWORDS)} stopwords")
    # else:
    #     logger.error(f"Stopwords file not found: {stopwords_path}")

    # stopwords_path = index_dir / "stopwords.txt"
    if os.path.exists(index_dir / "stopwords.txt"):
        with open(index_dir / "stopwords.txt", "r", encoding='utf-8') as f:
            # Properly handle each line, stripping whitespace
            # STOPWORDS = set(f.read().splitlines())
            # STOPWORDS = set(line.strip() for line in f if line.strip())
            for line in f:
                STOPWORDS.add(line.strip())
            # words = [word.strip() for word in f.readlines()]
            # STOPWORDS = set(word for word in words if word)

    # Load PageRank
    # pagerank_path = index_dir / "pagerank.out"
    # logger.debug(f"Loading PageRank from: {pagerank_path}")
    # if os.path.exists(pagerank_path):
    #     with open(pagerank_path, "r", encoding='utf-8') as f:
    # PAGERANK = {int(line.split(",")[0]): float(line.split(",")[1].strip())
    #                 for line in f}

    # pagerank_path = index_dir / "pagerank.out"
    if os.path.exists(index_dir / "pagerank.out"):
        with open(index_dir / "pagerank.out", "r", encoding='utf-8') as f:
            # Handle each line properly with error checking
            for line in f:
                if ',' in line:
                    docid_str, score_str = line.strip().split(',')
                    try:
                        docid = int(docid_str)
                        score = float(score_str)
                        PAGERANK[docid] = score
                    except ValueError:
                        continue

    # Load inverted index
    index_filename = os.getenv("INDEX_PATH", "inverted_index_1.txt")
    index_path = index_dir / "inverted_index" / index_filename

    if os.path.exists(index_path):
        with open(index_path, "r", encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                # term = parts[0]
                # idf = float(parts[1])
                docs = []

                # Process document data in groups of 3
                for i in range(2, len(parts), 3):
                    doc_id = int(parts[i])
                    tf = int(parts[i + 1])
                    norm = float(parts[i + 2])
                    docs.append((doc_id, tf, norm))

                INVERTED_INDEX[parts[0]] = {
                    "idf": float(parts[1]),
                    "docs": docs
                }
