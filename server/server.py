"""
The server for the Simple English project.
"""

import logging
import signal
import sys
from signal import Signals
from types import FrameType
from typing import Tuple

import requests
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request
from flask_caching import Cache
from flask_cors import CORS
from openai import AuthenticationError, BadRequestError, OpenAI

from .cache import read_article, save_article, url_to_wid
from .constants import DEBUG, EXPAND_PROMPT, SIMPLIFY_PROMPT, URLS
from .exceptions import BadUrlError, MissingTokenError, WikipediaLimitError
from .logger import logger
from .parsing import (
    format_for_expand,
    get_expanded_contents,
    sanitize_summary,
    tidy_for_summary,
)

load_dotenv()

if DEBUG:
    logging.getLogger("flask_cors").level = logging.DEBUG

app = Flask(__name__)

if DEBUG:
    logger.info("Running in DEBUG mode, using CORS for all origins")
    CORS(app, supports_credentials=True)
else:
    logger.info("Running in production mode, using CORS for a specific origin")
    CORS(
        app,
        supports_credentials=True,
        methods=["OPTIONS", "GET", "POST"],
        resources={r"/*": {"origins": URLS}},
        expose_headers=["Content-Type", "Authorization"],
        allow_headers=["Content-Type", "Authorization"],
    )

cache = Cache(
    config={
        "CACHE_TYPE": "filesystem",
        "CACHE_DIR": "cache",
        "CACHE_DEFAULT_TIMEOUT": 3600 * 24 * 7,
    }
)
cache.init_app(app)


@app.route("/status", methods=["GET"])
def status() -> Tuple[Response, int]:
    """
    Make sure the API is alive.
    """
    return jsonify({"status": "up"}), 200


def make_simplify_cache_key():
    """
    Turn the Wikipedia URL into a cache key.
    """
    url = request.args.get("url")
    return url_to_wid(url)


@app.route("/simplify", methods=["GET"])
@cache.cached(make_cache_key=make_simplify_cache_key)
def simplify() -> Tuple[Response, int]:
    """
    Simplfy article content.
    """
    url = request.args.get("url")
    if not url:
        raise BadUrlError("A valid Wikipedia URL is required.")

    # NOTE: the calls to read_article and save_article are for naive caching
    # ...they only run if the DEBUG flag is set!
    llm_response = read_article(url, short=True)
    if llm_response is not None:
        return jsonify({"content": llm_response}), 200

    html_content = read_article(url)
    if html_content is None:
        response = requests.get(url)
        response.raise_for_status()

        html_content = tidy_for_summary(response.text)

        save_article(url, html_content)

    if html_content is None or not html_content:
        raise WikipediaLimitError("Could not retrieve Wikipedia article content.")

    token = request.args.get("token")
    if not token:
        raise MissingTokenError("An OpenAI token is required.")

    client = OpenAI(
        api_key=token,
    )

    logger.debug("[simplify] html_content: %s", html_content)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SIMPLIFY_PROMPT},
            {"role": "user", "content": html_content},
        ],
    )
    llm_response = completion.choices[0].message.content
    logger.debug("[simplify] llm_response: %s", llm_response)

    sanitized_content = sanitize_summary(llm_response)

    save_article(url, sanitized_content, short=True)

    return jsonify({"content": sanitized_content}), 200


@app.route("/expand", methods=["POST"])
def expand() -> Tuple[Response, int]:
    """
    Expand on a given key phrase.
    """
    data = request.get_json()

    # TODO(michaelfromyeg): add a guard for content
    html_content = data["content"]

    token = request.args.get("token")
    if not token:
        raise MissingTokenError("An OpenAI token is required.")

    client = OpenAI(
        api_key=token,
    )

    user_prompt = format_for_expand(html_content)
    logger.debug("[expand] user_prompt: %s", user_prompt)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": EXPAND_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    llm_response = completion.choices[0].message.content
    logger.debug("[expand] llm_response: %s", llm_response)

    expanded_content = get_expanded_contents(llm_response)
    return jsonify({"content": expanded_content}), 200


@app.errorhandler(BadRequestError)
def handle_openai_error(error: BadRequestError) -> Tuple[Response, int]:
    """
    Handle OpenAI errors and return a 400 response.
    """
    logger.warning(str(error))
    return jsonify({"error": "Bad OpenAI Request", "message": str(error)}), 400


@app.errorhandler(AuthenticationError)
def handle_openai_auth_error(error: AuthenticationError) -> Tuple[Response, int]:
    """
    Handle OpenAI errors and return a 401 response.
    """
    logger.warning(str(error))
    return jsonify({"error": "Authentication Error", "message": str(error)}), 401


@app.errorhandler(BadUrlError)
def handle_url_error(error: BadUrlError) -> Tuple[Response, int]:
    """
    Handle BadUrlError and return a 400 response.
    """
    logger.warning(str(error))
    return jsonify({"error": "Bad URL", "message": str(error)}), 400


@app.errorhandler(MissingTokenError)
def handle_token_error(error: MissingTokenError) -> Tuple[Response, int]:
    """
    Handle MissingTokenError and return a 400 response.
    """
    logger.warning(str(error))
    return jsonify({"error": "Missing Token", "message": str(error)}), 400


@app.errorhandler(WikipediaLimitError)
def handle_wikipedia_error(error: WikipediaLimitError) -> Tuple[Response, int]:
    """
    Handle WikipediaError and return a 429 response.
    """
    logger.warning(str(error))
    return jsonify({"error": "Wikipedia Limit", "message": str(error)}), 429


@app.errorhandler(400)
def bad_request_error(error: Exception) -> Tuple[Response, int]:
    """
    Wrap the error in a 400 JSON response.
    """
    logger.warning(str(error))
    return jsonify({"error": "Bad Request", "message": str(error)}), 400


@app.errorhandler(404)
def not_found_error(error: Exception) -> Tuple[Response, int]:
    """
    Wrap the error in a 404 JSON response.
    """
    logger.warning(str(error))
    return jsonify({"error": "Not Found", "message": str(error)}), 404


@app.errorhandler(500)
def internal_error(error: Exception) -> Tuple[Response, int]:
    """
    Wrap the error in a 500 JSON response.
    """
    logger.error(str(error))
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500


def interrupt_handler(sig: Signals, frame: FrameType) -> None:
    """
    Perform any necessary clean-up steps in development.
    """
    logger.info("Received Ctrl+C, cleaning up...")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, interrupt_handler)
    app.run(debug=DEBUG)
