import os

import requests
from flask import Flask, jsonify, request
from openai import OpenAI

DEBUG = False

app = Flask(__name__)


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "Server is running"}), 200


@app.route("/simplify", methods=["GET"])
def simplify():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    # Get the HTML content of the Wikipedia article
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        if DEBUG:
            print(f"{html_content=}")
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

    # Use OpenAI to generate a simplified version of the article
    try:
        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ],
            model="gpt-3.5-turbo",
        )

        print(chat_completion)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True)
