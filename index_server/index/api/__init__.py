import os

# Global variables for stopwords, pagerank, and inverted index
# TODO: these variable declarations should go inside the outer __init__.py, or a separate config.py file for that
STOPWORDS = set()
PAGERANK = {}
INVERTED_INDEX = {}

def load_index():
    """Load inverted index, stopwords, and PageRank into memory."""
    global STOPWORDS, PAGERANK, INVERTED_INDEX

    # Load stopwords
    stopwords_path = "index/stopwords.txt"
    if os.path.exists(stopwords_path):
        with open(stopwords_path, "r") as f:
            STOPWORDS = set(f.read().splitlines())

    # Load PageRank
    pagerank_path = "index/pagerank.out"
    if os.path.exists(pagerank_path):
        with open(pagerank_path, "r") as f:
            PAGERANK = {int(line.split(",")[0]): float(line.split(",")[1]) for line in f}

    # Load inverted index
    # TODO modify hardcoded inverted_index_1
    # Nah this is good
    # TODO: need to modify this to be valid for relative paths, hardcode a base app directory and then 
    # add then concatenate the relative path to it.
    index_path = os.getenv("INDEX_PATH", "index/inverted_index/inverted_index_1.txt")
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            for line in f:
                term, idf, *docs = line.strip().split()
                idf = float(idf)
                docs = [(int(doc.split()[0]), int(doc.split()[1]), float(doc.split()[2])) for doc in docs]
                INVERTED_INDEX[term] = {"idf": idf, "docs": docs}
