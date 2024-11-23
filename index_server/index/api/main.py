import math
from flask import Blueprint, jsonify, request, current_app
from index.api.load_data import search_index


@index.app.route('/api/v1')

def get_query_vector():
    """Compute normalized query vector."""
