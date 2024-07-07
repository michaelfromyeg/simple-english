"""
A "dumb" caching technique that works by writing files to disk.

Only used in development to save time and avoid rate limiting.
"""

import os

from server.constants import DEBUG


def url_to_wid(url: str) -> str:
    """
    Convert a Wikipedia URL to a (w)ID.
    """
    title = url.split("/wiki/")[-1]
    wid = title.replace("_", "-").lower()

    # remove any query parameters
    if "?" in wid:
        wid = wid.split("?")[0]

    return wid


def save_article(url: str, article: str, short: bool = False) -> None:
    """
    Save the HTML file of an article to disk.

    Only runs in DEBUG mode.
    """
    if not DEBUG:
        return None

    wid = url_to_wid(url)
    file_name = f"{wid}-short.txt" if short else f"{wid}.txt"
    file_path = os.path.join("data", file_name)

    if os.path.isfile(file_path):
        return

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(article)

    return None


def read_article(url: str, short: bool = False) -> str | None:
    """
    Read the article from disk, if it exists.

    Only runs in DEBUG mode.
    """
    if not DEBUG:
        return None

    wid = url_to_wid(url)
    file_name = f"{wid}-short.txt" if short else f"{wid}.txt"
    file_path = os.path.join("data", file_name)

    if not os.path.isfile(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    return content
