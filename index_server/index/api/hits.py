"""Hits."""
from flask import request, jsonify
import index
from index.api import STOPWORDS, PAGERANK, INVERTED_INDEX
from math import sqrt
import re

# import index_server #not sure if its server or index??

@index.app.route('/api/v1/hits', methods=['GET'])
def get_hits():
    """Return search results for a query."""

    query = request.args.get("q", "")
    weight = float(request.args.get("w", 0.5))

    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query).lower()

    query_terms = [term.lower() for term in query.split() if term.lower() not in STOPWORDS]
    if not query_terms:
        return jsonify({"hits": []})

    # Ensure documents must contain all query terms (AND logic)
    candidate_docs = None
    for term in query_terms:
        if term in INVERTED_INDEX:
            doc_ids = {doc[0] for doc in INVERTED_INDEX[term]["docs"]}
            candidate_docs = doc_ids if candidate_docs is None else candidate_docs & doc_ids
        else:
            # If any term is not found, no document can match all terms
            return jsonify({"hits": []})

    if not candidate_docs:
        return jsonify({"hits": []})

    # Calculate scores
    results = {}
    running_sum = 0 #every time term matches we add the product to running sum 
    for term in query_terms:
        if term in INVERTED_INDEX:
            term_data = INVERTED_INDEX[term]
            idf = term_data["idf"]
            for doc_id, tf, norm in term_data["docs"]:
                tf_idf = tf * idf / sqrt(norm)
                pagerank = PAGERANK.get(doc_id, 0.0)
                cosSim = 
                score = weight * pagerank + (1 - weight) * tf_idf # wasnt this supposed to be cosine of this. like similarity? cos?
                if doc_id not in results:
                    results[doc_id] = 0.0
                results[doc_id] += score

    # Sort results by score
    sorted_results = [{"docid": doc_id, "score": score} for doc_id, score in sorted(results.items(), key=lambda x: x[1], reverse=True)]

    return jsonify({"hits": sorted_results})