import os
import pathlib
import math

class SearchIndex:
    """Class to hold search index data structures."""
    def __init__(self):
        self.inverted_index = {}  # word -> [(docid, tf_idf), ...]
        self.pagerank = {}        # docid -> score
        self.stopwords = set()    # set of stopwords
        self.doc_norms = {}       # docid -> normalization factor

# Global instance
search_index = SearchIndex()

def load_index():
    """Load inverted index, pagerank, and stopwords into memory."""
    index_dir = pathlib.Path(__file__).parent.parent

    # Load stopwords
    stopwords_path = index_dir / "stopwords.txt"
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        search_index.stopwords = set(line.strip() for line in f)

    # Load PageRank scores
    pagerank_path = index_dir / "pagerank.out"
    with open(pagerank_path, 'r', encoding='utf-8') as f:
        for line in f:
            docid, score = line.strip().split(',')
            search_index.pagerank[int(docid)] = float(score)

    # Load inverted index segment
    index_path = index_dir / "inverted_index" / os.getenv("INDEX_PATH", "inverted_index_1.txt")
    with open(index_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            word = parts[0]
            idf = float(parts[1])
            
            # Process posting list pairs (docid, tf)
            postings = []
            for i in range(2, len(parts), 3):
                docid = int(parts[i])
                tf = int(parts[i + 1])
                norm_factor = float(parts[i + 2])
                search_index.doc_norms[docid] = math.sqrt(norm_factor)
                tf_idf = tf * idf
                postings.append((docid, tf_idf))
            
            search_index.inverted_index[word] = postings