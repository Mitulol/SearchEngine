# index_server/index/__init__.py
import os
from flask import Flask
import index.api
import pathlib


app = Flask(__name__)

# if test_config is None:
#     app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
# else:
#     app.config.update(test_config)

# TODO: I changed this from "inverted_index/inverted_index_1.txt" to "inverted_index_1.txt" 
# cause we were failing the very first assert statement on every test
INDEX_PATH = os.getenv("INDEX_PATH", "inverted_index_1.txt")
app.config["INDEX_PATH"] = INDEX_PATH
app.config["ASK485_ROOT"] = pathlib.Path(__file__).parent.parent.parent
app.config["INDEX_DIR"] = app.config["ASK485_ROOT"]/'index_server'/'index'/'inverted_index'
index.api.load_index()


