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

    # query = re.sub(r"[^a-zA-Z0-9 ]+", "", query).lower()

    query_terms = {}
    # query_terms = [term.lower() for term in query.split() if term.lower() not in STOPWORDS]

    
    for term in query.split():
        cleaned_term = re.sub(r"[^a-zA-Z0-9]", "", term).lower()
        if cleaned_term and cleaned_term not in STOPWORDS:
            query_terms[cleaned_term] = query_terms.get(cleaned_term, 0) + 1
            
    if not query_terms:
        return jsonify({"hits": []})

    # Ensure documents must contain all query terms (AND logic)
    # Whats this?
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

    # Accessing 1 doc
    for doc, value in docs.items():
        runningsum = 0
        for term, position in value:
            runningsum += position ** 2
        norm_factor = runningsum ** 0.5 # TODO: consider pulling norm_factor from INVERTED_INDEX. will need to add checks for equality for doc_id equality
        for term, position in value:
            value[term] = position/norm_factor
    
    #DONE
    # docs is of the form:
    # {doc_id: {tk: normalized_position}}

    
    


        
        

             
    
        docs[doc]= 

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

    return jsonify({"hits": sorted_results})