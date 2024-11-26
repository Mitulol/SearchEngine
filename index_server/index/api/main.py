# index/api/main.py
"""Main api."""
import math
import re
from flask import request, jsonify
from index.api import STOPWORDS, PAGERANK, INVERTED_INDEX
from index import app


@app.route('/api/v1/', methods=['GET'])
def get_info():
    """Return API resource URLs."""
    context = {
         "hits": "/api/v1/hits/",
         "url": "/api/v1/"
    }
    return jsonify(**context), 200


@app.route('/api/v1/hits/', methods=['GET'])
def get_hits():
    """Return search results for a query."""
    query = request.args.get("q", "")
    weight = float(request.args.get("w", 0.5))
    # app.logger.info(f"INVERTED_INDEX: {INVERTED_INDEX}")

    # Process query terms
    query_terms = {}
    for term in query.split():
        cleaned_term = re.sub(r"[^a-zA-Z0-9]", "", term).lower()
        # app.logger.info(f"Cleaned term: {cleaned_term}")
        # app.logger.info(f"STOPWORDS: {STOPWORDS}")
        if ((cleaned_term) and (cleaned_term not in STOPWORDS)):
            query_terms[cleaned_term] = query_terms.get(cleaned_term, 0) + 1
            # app.logger.info(f"Term no in STOPWORDS: {cleaned_term}")

    if not query_terms:
        return jsonify({"hits": []}), 200

    # Find documents containing all terms
    candidate_docs = None
    for term in query_terms:  # Looping through all the keys in query_terms
        if term in INVERTED_INDEX:
            doc_ids = {doc[0] for doc in INVERTED_INDEX[term]["docs"]}
            candidate_docs = doc_ids if candidate_docs is None else candidate_docs & doc_ids
        else:
            app.logger.info("Term '%s' not in index", term)
            return jsonify({"hits": []}), 200

    if not candidate_docs:
        return jsonify({"hits": []}), 200

    # Calculate query vector and normalize
    query_vector = {}
    query_norm = 0
    for term, tf_q in query_terms.items():
        if term in INVERTED_INDEX:
            idf = INVERTED_INDEX[term]["idf"]
            weight_q = tf_q * idf
            query_vector[term] = weight_q
            query_norm += weight_q ** 2

    query_norm = math.sqrt(query_norm)
    for term in query_vector:
        query_vector[term] /= query_norm

    # Calculate document scores
    results = {}
    for doc_id in candidate_docs:
        cosine_sim = 0
        for term, q_weight in query_vector.items():
            term_data = INVERTED_INDEX[term]
            for doc in term_data["docs"]:
                if doc[0] == doc_id:
                    tf_d = doc[1]
                    norm_d = math.sqrt(doc[2])
                    d_weight = (tf_d * term_data["idf"]) / norm_d
                    cosine_sim += q_weight * d_weight
                    break

        pagerank_score = PAGERANK.get(doc_id, 0.0)
        final_score = weight * pagerank_score + (1 - weight) * cosine_sim
        results[doc_id] = final_score

    # Sort and format results
    hits = [{"docid": doc_id, "score": score}
            for doc_id, score in sorted(results.items(), key=lambda x: x[1], reverse=True)]

    return jsonify({"hits": hits}), 200
