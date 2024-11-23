# index_server/index/__init__.py
import os
from flask import Flask
import index.api


app = Flask(__name__)

# if test_config is None:
#     app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
# else:
#     app.config.update(test_config)

INDEX_PATH = os.getenv("INDEX_PATH", "inverted_index/inverted_index_1.txt")
app.config["INDEX_PATH"] = INDEX_PATH

index.api.load_index()


