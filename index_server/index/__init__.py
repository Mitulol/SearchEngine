# index/__init__.py
"""Index init py."""
import os
from pathlib import Path
from flask import Flask

# Create flask app
app = Flask(__name__)

# Configure app
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")

# Import views after app is created to avoid circular imports
import index.api  # noqa: E402  pylint: disable=wrong-import-position
import index.api.main  # noqa: E402  pylint: disable=wrong-import-position
index.api.load_index()
