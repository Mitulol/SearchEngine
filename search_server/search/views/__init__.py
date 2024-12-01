"""Search server views."""
import threading
import heapq
from concurrent.futures import ThreadPoolExecutor
import requests
import flask
from search import app
from search.model import get_db


def get_hits_for_segment(url, query, weight):
    """Get search hits from one index segment."""
    try:
        response = requests.get(
            url,
            params={"q": query, "w": weight},
            timeout=5
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()["hits"]
    except (requests.RequestException, KeyError) as e:
        print(f"Error fetching hits from {url}: {str(e)}")
        return []


@app.route('/')
def show_index():
    """Display / route."""
    # Get search parameters
    query = flask.request.args.get('q', '')
    weight = flask.request.args.get('w', '0.5')

    # If no query, just show the search page
    if not query:
        return flask.render_template("index.html", query=query, weight=weight)

    # Make concurrent requests to all index segments using ThreadPoolExecutor
    urls = app.config['SEARCH_INDEX_SEGMENT_API_URLS']
    with ThreadPoolExecutor(max_workers=len(urls)) as executor:
        # Submit all requests concurrently
        future_to_url = {
            executor.submit(get_hits_for_segment, url, query, weight): url
            for url in urls
        }

        # Gather all hits from completed requests
        all_hits = []
        for future in future_to_url:
            # This will wait for each request to complete
            hits = future.result()
            all_hits.extend(hits)

    # Sort all hits by score (descending) and take top 10
    results = heapq.nlargest(10, all_hits, key=lambda x: x["score"])

    # Get document info from database
    db = get_db()
    documents = []
    for hit in results:
        doc = db.execute(
            "SELECT * FROM documents WHERE docid = ?",
            (hit["docid"],)
        ).fetchone()
        if doc:
            documents.append(doc)

    return flask.render_template(
        "index.html",
        query=query,
        weight=weight,
        documents=documents
    )
