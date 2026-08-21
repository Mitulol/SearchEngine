# Search Engine Project

## Overview

This project implements a scalable search engine using **MapReduce**, **TF-IDF scoring**, and **PageRank ranking**. It processes a large dataset of web pages to construct an inverted index, allowing for efficient keyword-based search queries. The system consists of:

- **Inverted Index Construction (MapReduce)** — generates an index of words and their occurrences across documents.
- **Index Server** — handles search queries by retrieving relevant documents from the index.
- **Search Server** — provides a web-based interface for querying the index.

## How It Works

### 1. Inverted Index Construction (MapReduce)

The search engine constructs an inverted index using a MapReduce pipeline to process large-scale web page data efficiently:

- **Job 0: Document Count** — computes the total number of documents in the dataset.
- **Job 1: Parsing** — extracts words from web pages and removes stopwords.
- **Job 2: Term Frequency (TF) Calculation** — computes how often each term appears in a document.
- **Job 3: Inverted Index Construction** — aggregates the results and partitions the index into multiple files for efficient lookup.

The index is split into three segments (`inverted_index_0.txt`, `inverted_index_1.txt`, `inverted_index_2.txt`). Each Index Server instance loads only one segment, based on `INDEX_PATH`.

### 2. TF-IDF Calculation

Each word's importance is computed using Term Frequency-Inverse Document Frequency (TF-IDF):

**Term Frequency (TF):**

`TF(t, d) = f(t, d) / Σ f(w, d)`

**Inverse Document Frequency (IDF):**

`IDF(t) = log(N / df(t))`

where `f(t, d)` is the number of times term `t` appears in document `d`, `df(t)` is the number of documents containing `t`, and `N` is the total number of documents.

**Example:** suppose "algorithm" appears 5 times in a document with 100 words:
- `TF(algorithm) = 5 / 100 = 0.05`
- If "algorithm" appears in 50 out of 10,000 documents: `IDF(algorithm) = log(10,000 / 50) ≈ 2.3`
- `TF-IDF(algorithm) = 0.05 * 2.3 ≈ 0.115`

### 3. PageRank Computation

PageRank ranks documents by importance in the web graph, computed with the iterative formula:

`PR(A) = (1 - d) / N + d * Σ (PR(B) / L(B)) for B ∈ M(A)`

where `d` is the damping factor (commonly 0.85), `N` is the total number of documents, `M(A)` is the set of documents linking to `A`, and `L(B)` is the number of outbound links in document `B`.

Final ranking blends the two signals via a tunable weight:

`Score(q, d, w) = w * PR(d) + (1 - w) * cosSim(q, d)`

At `w=0`, ranking is purely TF-IDF-based; at `w=1`, it's purely PageRank-based.

### 4. Index Server

Queries all index shards in parallel and merges results with `heapq.merge()`, computing relevance from the blended TF-IDF/PageRank score and returning ranked JSON results.

### 5. Search Server

A Flask-based web UI that fetches ranked results from the Index Server and displays them to the user.

---

## Setup Instructions

**1. Clone the repository**
```bash
git clone <repository_url>
cd search-engine
```

**2. Create and activate a Python virtual environment**
```bash
python3 -m venv env
source env/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
pip install -e index_server
pip install -e search_server
```

**4. Extract crawl data**
```bash
cd inverted_index
tar -xvJf crawl.tar.xz
```

**5. Build the inverted index**

Run the MapReduce pipeline:
```bash
cd inverted_index
./pipeline.sh crawl
```
The pipeline script automatically moves the generated index files to the `index_server` directory — no manual copying needed.

**6. Start the Index Server**
```bash
./bin/index start   # ./bin/index status | ./bin/index stop
```

**7. Start the Search Server**
```bash
./bin/searchdb       # creates the search database
./bin/search start   # ./bin/search status | ./bin/search stop
```

**8. Run tests**
```bash
pytest -v tests/
```

---

## Project Structure

```
.
├── bin/                 # Scripts for managing servers
├── inverted_index/      # MapReduce index construction
│   ├── crawl/           # Web page dataset
│   ├── output/          # Generated inverted index files
│   ├── pipeline.sh      # Shell script for the MapReduce pipeline
│   ├── stopwords.txt    # Common words to ignore
│   └── pagerank.out     # Precomputed PageRank values
├── index_server/        # API for index-based search
│   ├── index/
│   │   ├── inverted_index/
│   │   ├── pagerank.out
│   │   └── stopwords.txt
│   └── api/
│       └── main.py
├── search_server/       # Web-based search interface
│   └── search/
│       ├── templates/index.html
│       ├── static/css/style.css
│       ├── config.py
│       ├── model.py
│       └── views/__init__.py
├── tests/                # Unit tests
├── var/                  # Logs and database
│   └── search.sqlite3
└── requirements.txt
```

---

## Debugging & Troubleshooting

Querying an individual Index Server directly:
```bash
http "localhost:9000/api/v1/hits/?q=machine+learning&w=0.7"
```

Testing the Index Server API:
```bash
pytest -v tests/test_index_server_public.py
```

Verifying TF-IDF and PageRank values:
```bash
grep "^machine " index_server/index/inverted_index/inverted_index_*.txt
grep "12345678," index_server/index/pagerank.out
```

---

## Author

**Mitul Goel** — [GitHub](https://github.com/Mitulol) · [LinkedIn](https://linkedin.com/in/mitul-goel)

B.S.E. Computer Science
College of Engineering
University of Michigan
