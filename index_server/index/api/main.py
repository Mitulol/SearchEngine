"""General."""
import flask
import index
import math
from flask import request, jsonify, current_app
from index.api import STOPWORDS, PAGERANK, INVERTED_INDEX
from math import sqrt
import re
# import index_server #not sure if its server or index??


@index.app.route('/api/v1/', methods=['GET'])
def v1():
    """Get infor available."""
    context = {
         "hits": "/api/v1/hits/",
         "url": "/api/v1/"
    }

    return flask.jsonify(**context), 200


@index.app.route('/api/v1/hits/', methods=['GET'])
def get_hits():
    """Return search results for a query."""

    query = request.args.get("q", "")
    weight = float(request.args.get("w", 0.5))

    print("I made it here")


    # query = re.sub(r"[^a-zA-Z0-9 ]+", "", query).lower()

    query_terms = {}
    # query_terms = [term.lower() for term in query.split() if term.lower() not in STOPWORDS]
    # print(query_terms)

    
    for term in query.split():
        cleaned_term = re.sub(r"[^a-zA-Z0-9]", "", term).lower()
        if cleaned_term and cleaned_term not in STOPWORDS:
            query_terms[cleaned_term] = query_terms.get(cleaned_term, 0) + 1
            
    if not query_terms:
        return jsonify({"hits": []}), 200

    # Ensure documents must contain all query terms (AND logic)
    # Whats this?
    candidate_docs = None
    for term in query_terms:
        if term in INVERTED_INDEX:
            doc_ids = {doc[0] for doc in INVERTED_INDEX[term]["docs"]}
            candidate_docs = doc_ids if candidate_docs is None else candidate_docs & doc_ids
        else:
            # If any term is not found, no document can match all terms
            return jsonify({"hits": []}), 200

    if not candidate_docs:
        return jsonify({"hits": []}), 200

    # Calculate scores
    results = {}
    # running_sum = 0 #every time term matches we add the product to running sum 
    # No need for this nvm.
    for term, tf_q in query_terms.items(): # tf_q is the term frequency in the queue
        if term in INVERTED_INDEX:
            term_data = INVERTED_INDEX[term]
            idf = term_data["idf"]
            position = tf_q * idf # TODO: im assuming INVERTED_INDEX works as required and idf is of type float
            # Overwriting the old frequency values with the position values
            query_terms[term] = position
    
    # Calculating normalization factor:
    runningsum = 0
    for term, position in query_terms.items():
        runningsum += position**2
    norm_factor = runningsum ** (1/2)

    # Normalizing the query vector (Dividing every term with the normalization factor)
    for term, position in query_terms.items():
        query_terms[term] = position/norm_factor

    # candidate_docs is the list of docs we will print
    docs = {}
    # docs has doc_id as a key and value as {tk: tfi * idfi} as the value
    for doc in candidate_docs:
        for term, norm_position in query_terms.items():
            term_data = INVERTED_INDEX[term]
            idf = term_data["idf"]
            for i in term_data["docs"]:
                if doc == i[0]:
                    tf_ik = i[1]
                    break
            # I got idf and tf_ik for the required doc and the required term
            docs[doc][term] = tf_ik * idf
    
    # Finished making a dictionary of document vectors
    # docs is a dictionary of the required document vectors with doc_id as the key
    # docs is of the form:
    # {doc_id: {tk: idf*tf_ik}}

    # # Accessing 1 doc
    # for doc, value in docs.items():
    #     for term in INVERTED_INDEX:
    #         if term == 
    #         for docs in term["docs"]:
    #             if docs[0] == doc:
    #                 norm_factor = docs[2] ** 0.5
    #     # runningsum = 0
    #     # for term, position in value.items():
    #     #     runningsum += position ** 2
    #     # norm_factor = runningsum ** 0.5 # TODO: consider pulling norm_factor from INVERTED_INDEX. will need to add checks for equality for doc_id equality
    #     for term, position in value.items():
    #         value[term] = position/norm_factor


    # docs is of the form:
    # {doc_id: {tk: idf*tf_ik}}
    for doc, value in docs.items():
        for term, position in value.items():
            # Getting the required Normalization factor for the specific document for the specific term
            for i in INVERTED_INDEX[term]["docs"]:
                if i[0] == doc:
                    norm_factor = i[2]
                    break
                    # norm_factor = INVERTED_INDEX[term]["docs"][i][2]
            value[term] = position/norm_factor
    
    #DONE
    # docs is of the form:
    # {doc_id: {tk: normalized_position}}

    # has a key as doc_id and value as the sim_score
    # sim_scores= {}

    # Finding dot products (sim scores for each doc)
    for doc, value in docs.items(): # Getting one doc out of all the docs
        sim_score = 0
        for term_d, position_d in value.items(): # Getting one term from a specific doc
            for term_q, position_q in query_terms.items(): # getting one term from the query
                if term_d == term_q: # if they match
                    sim_score += position_d * position_q # multiply them
        results[doc] = weight * PAGERANK.get(doc, 0.0) + (1 - weight) * sim_score


    # DONE
    # results has the key as the doc_id and the value as the score

    # Didn't realize yall already did this part.
    # hits = []

    # sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

    # for docid, score in results.items():

    # context = {

    # }




    # tf-idf similarity score
    # cossim = q dot product documenti

    # Weighted score
    #score(q,d,w) = w*pagerank(d) + (1-w)*cossim(q,d)
    #cossim(q,d is from tf-idf similarity score)



    # the value for every key in query_terms is the normalized value
            # for doc_id, tf, norm in term_data["docs"]:
            #     tf_idf = tf * idf / sqrt(norm)
            #     pagerank = PAGERANK.get(doc_id, 0.0)
            #     cosSim =  
            #     score = weight * pagerank + (1 - weight) * tf_idf # wasnt this supposed to be cosine of this. like similarity? cos?
            #     if doc_id not in results:
            #         results[doc_id] = 0.0
            #     results[doc_id] += score

    # Sort results by score
    sorted_results = [{"docid": doc_id, "score": score} for doc_id, score in sorted(results.items(), key=lambda x: x[1], reverse=True)]

    return jsonify({"hits": sorted_results}), 200