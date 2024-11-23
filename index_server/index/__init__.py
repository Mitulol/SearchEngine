# index_server/index/__init__.py
import os
from flask import Flask


def create_app(test_config=None):
    """Create and configure the Flask app."""
    app = Flask(__name__)

    if test_config is None:
        app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
    else:
        app.config.update(test_config)

    import index.api # noqa: E402  pylint: disable=wrong-import-position

    # Load inverted index, stopwords, and pagerank into memory
    index.api.load_index()

    return app
