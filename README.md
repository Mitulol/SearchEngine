# **Search Engine Project (EECS 485 - Project 5)**

## **Introduction**
This project implements a **scalable search engine** using **MapReduce, TF-IDF scoring, and PageRank ranking**. It processes a large dataset of web pages to construct an **inverted index**, allowing for efficient keyword-based search queries. The system consists of:

- **Inverted Index Construction (MapReduce)**: Generates an index of words and their occurrences in documents.
- **Index Server**: Handles search queries by retrieving relevant documents.
- **Search Server**: Provides a web-based interface for querying the index.

## **How It Works**

### **1. Inverted Index Construction (MapReduce)**

The search engine constructs an **inverted index** using MapReduce to process large-scale web page data efficiently. The steps are:

- **Job 0: Document Count**: Computes the total number of documents in the dataset.
- **Job 1: Parsing**: Extracts words from web pages and removes stopwords.
- **Job 2: Term Frequency (TF) Calculation**: Computes how often each term appears in a document.
- **Job 3: Inverted Index Construction**: Aggregates the results and partitions the index into multiple files for efficient lookup.

The index is split into **three segments** (`inverted_index_0.txt`, `inverted_index_1.txt`, `inverted_index_2.txt`). Each Index Server instance only loads one segment based on `INDEX_PATH`.

### **2. TF-IDF Calculation**

Each word’s importance is computed using **Term Frequency-Inverse Document Frequency (TF-IDF)**:

- **Term Frequency (TF)**:

  `TF(t, d) = f(t, d) / Σ f(w, d)`

- **Inverse Document Frequency (IDF)**:

  `IDF(t) = log(N / df(t))`

  where:
  - `f(t, d)` is the number of times term `t` appears in document `d`.
  - `df(t)` is the number of documents containing `t`.
  - `N` is the total number of documents.

  **Example Calculation:**
  Suppose "Michigan" appears 5 times in a document with 100 words.
  - `TF(Michigan) = 5 / 100 = 0.05`
  - If "Michigan" appears in 50 out of 10,000 documents:
    `IDF(Michigan) = log(10,000 / 50) ≈ 2.3`
  - `TF-IDF(Michigan) = 0.05 * 2.3 ≈ 0.115`

### **3. PageRank Computation**

PageRank is used to rank documents based on their importance in the web graph. The iterative formula is:

`PR(A) = (1 - d) / N + d * Σ (PR(B) / L(B)) for B ∈ M(A)`

where:
- `PR(A)` is the PageRank of document `A`.
- `d` is the damping factor (commonly 0.85).
- `N` is the total number of documents.
- `M(A)` is the set of documents linking to `A`.
- `L(B)` is the number of outbound links in document `B`.

Ranking is computed as:

`Score(q, d, w) = w * PR(d) + (1 - w) * cosSim(q, d)`

Where `w` is a tunable parameter (0 ≤ w ≤ 1).

- `w=0`: Ranking is purely TF-IDF-based.
- `w=1`: Ranking is purely PageRank-based.

### **4. Index Server**

- Queries all **Index Servers in parallel** and merges results using `heapq.merge()`.
- Computes relevance using **TF-IDF and PageRank**.
- Returns ranked JSON results.

### **5. Search Server**

- Web UI for user queries.
- Fetches top results from Index Server.
- Displays relevant documents.

---

## **Setup Instructions**

### **1. Clone the Repository**

```bash
git clone <repository_url>
cd p5-search-engine
```

### **2. Create and Activate a Python Virtual Environment**

```bash
python3 -m venv env
source env/bin/activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
pip install -e index_server
pip install -e search_server
```

### **4. Extract Crawl Data**

```bash
cd inverted_index
tar -xvJf crawl.tar.xz
```

### **5. Build the Inverted Index**

Run the MapReduce pipeline:

```bash
cd inverted_index
./pipeline.sh crawl
```

The pipeline script automatically moves the generated index files to the `index_server` directory, so no manual copying is needed.

### **6. Setup the Index Server**

Start the index server:

```bash
./bin/index start
```

Check status:

```bash
./bin/index status
```

Stop the server:

```bash
./bin/index stop
```

### **7. Setup the Search Server**

Create the search database:

```bash
./bin/searchdb
```

Start the search server:

```bash
./bin/search start
```

Check status:

```bash
./bin/search status
```

Stop the server:

```bash
./bin/search stop
```

### **8. Running Tests**

Run public tests:

```bash
pytest -v tests/
```

Check code style:

```bash
pylint index_server search_server inverted_index
pycodestyle index_server search_server inverted_index
pydocstyle index_server search_server inverted_index
```

---

## **Project Structure**

```
.
├── bin/                 # Scripts for managing servers
├── inverted_index/      # MapReduce index construction
│   ├── crawl/          # Web page dataset
│   ├── output/         # Generated inverted index files
│   ├── pipeline.sh     # Shell script for MapReduce
│   ├── stopwords.txt   # Common words to ignore
│   ├── pagerank.out    # Precomputed PageRank values
├── index_server/       # API for index-based search
│   ├── index/
│   │   ├── inverted_index/
│   │   ├── pagerank.out
│   │   ├── stopwords.txt
│   ├── api/
│   │   ├── main.py
├── search_server/      # Web-based search engine
│   ├── search/
│   │   ├── templates/index.html  # Search UI
│   │   ├── static/css/style.css  # Styles
│   │   ├── config.py  # API configurations
│   │   ├── model.py   # Database functions
│   │   ├── views/__init__.py  # Flask views
├── tests/              # Unit tests
├── var/                # Logs and database
│   ├── search.sqlite3  # Search database
├── requirements.txt    # Dependencies
```

---

## **Debugging & Troubleshooting**

- Querying Individual Index Servers:
  ```bash
  http "localhost:9000/api/v1/hits/?q=machine+learning&w=0.7"
  ```
- Testing Index Server API:
  ```bash
  pytest -v tests/test_index_server_public.py
  ```
- Verifying Correct TF-IDF and PageRank Values:
  ```bash
  grep "^machine " index_server/index/inverted_index/inverted_index_*.txt
  grep "12345678," index_server/index/pagerank.out
  ```

---

## **Authors & Acknowledgments**

- **Developed for EECS 485 (University of Michigan).**
- **Instructors: Andrew DeOrio, Melina O’Dell, Maya Baveja.**
- **Data: Wikipedia subset on Michigan and Technology.**

