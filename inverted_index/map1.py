#!/usr/bin/env python3
"""Map 1: Get DocID."""
import sys
import re
import bs4

# Parse one HTML document at a time.  Note that this is still O(1) memory
# WRT the number of documents in the dataset.
HTML = ""
for line in sys.stdin:
    # Assume well-formed HTML docs:
    # - Starts with <!DOCTYPE html>
    # - End with </html>
    # - Contains a trailing newline
    if "<!DOCTYPE html>" in line:
        HTML = line
    else:
        HTML += line

    # If we're at the end of a document, parse
    if "</html>" not in line:
        continue

    # Configure Beautiful Soup parser
    soup = bs4.BeautifulSoup(HTML, "html.parser")

    # Get docid from document
    doc_id = soup.find("meta",
                       attrs={"eecs485_docid": True}).get("eecs485_docid")

    # Parse content from document
    # get_text() will strip extra whitespace and
    # concatenate content, separated by spaces
    element = soup.find("html")
    content = element.get_text(separator=" ", strip=True)
    # Remove extra newlines
    content = content.replace("\n", "")

    # Map 1 output.  Emit one line for each document, including the doc
    # ID and document content (You will need them later!)

    # clean the content
    content = re.sub(r"[^a-zA-Z0-9 ]+", "", content)
    # print the doc id and content
    print(f"{doc_id}\t{content}")
