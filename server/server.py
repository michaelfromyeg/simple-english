"""
The backend for simplifying and expanding Wikipedia articles/

Simplify prompt.

```
You are a human encyclopedia, with expertise on all of the world's knowledge.
You will be given an article from Wikipedia, as messy plain text.
Your job is to produce a version of the article in "Keyed Simple English", in simple HTML. "Keyed Simple English" is a language mode with a shorter overall length, shorter sentences, simpler words, and keyed words or phrases. Concepts are distilled and only the most important details are kept. Aim for a reading level of around sixth grade. Wrap interesting words or phrases in the simplified article with <a class="key">(the word or phrase)</a>. Include at least 3 key phrases in the entire article.

In your version, you will output the simplified article in HTML (using only the following tags: <p>, <ul>, <ol>, <li>, and <a>), with no additional styles.

Here is an an example, from the Wikipedia article for soccer.
English: ```The game of association football is played in accordance with the Laws of the Game, a set of rules that has been in effect since 1863 and maintained by the IFAB since 1886. The game is played with a football that is 68-70in circumference. The two teams compete to get the ball into the other team's goal (between the posts, under the bar, and across the goal line), thereby scoring a goal. When the ball is in play, the players mainly use their feet, but may use any other part of their body, except for their hands or arms, to control, strike, or pass the ball. Only the goalkeepers may use their hands and arms, and only then within the penalty area. The team that has scored more goals at the end of the game is the winner. There are situations where a goal can be disallowed, such as an offside call or a foul in the build-up to the goal. Depending on the format of the competition, an equal number of goals scored may result in a draw being declared, or the game goes into extra time or a penalty shoot-out.```
Simple English: ```<p>Games like <a class="key">football</a> have been played around the world since ancient times. The game came from <a class="key">England</a>, where the <a class="key">Football Association</a> wrote a standard set of rules for the game in 1863.</p>```

Your input will be messy plaintext, and your output will be "Keyed Simple English" with only the following tags: <p>, <ul>, <ol>, <li>, and <a>.
```

Expand prompt.

```
TODO(michaelfromyeg): write!
```
"""

import os
import signal
import sys
from typing import Tuple

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from openai import AssistantEventHandler, OpenAI
from typing_extensions import override

load_dotenv()

DEBUG = True

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# NOTE: this creates an assistant programatically; maybe there's a way to just 'update' one
# ...use it sparingly

# assistant = client.beta.assistants.create(
#     name="Simple English Wikipedia Assistant",
#     instructions="""You are a human encyclopedia, with expertise on all of the world's knowledge.
# You will be given an article from Wikipedia, as HTML.
# Your job is to produce a version of the article in "Keyed Simple English", also in HTML. "Keyed Simple English" is a language mode with a shorter overall length, shorter sentences, simpler words, and keyed words or phrases. Concepts are distilled and only the most important details are kept. Aim for a reading level of around sixth grade. In your outputted version, you will remove all links to other Wikipedia pages or external sources. Instead, wrap interesting words or phrases in the simplified article with <a class="key">(the word or phrase)</a>. Do this sparingly, for concepts or words you think the user might want to learn more about. Include at least 3 key phrases in the entire article.
# Here is an an example, from the Wikipedia article for soccer.
# English: ```<p>The game of association football is played in accordance with the <a href="/wiki/Laws_of_the_Game_(association_football)" title="Laws of the Game (association football)">Laws of the Game</a>, a set of rules that has been in effect since 1863 and maintained by the <a href="/wiki/International_Football_Association_Board" title="International Football Association Board">IFAB</a> since 1886. The game is played with a <a href="/wiki/Ball_(association_football)" title="Ball (association football)">football</a> that is 68–70&nbsp;cm (27–28&nbsp;in) in <a href="/wiki/Circumference" title="Circumference">circumference</a>. The two teams compete to get the ball into the other team's goal (between the posts, under the bar, and across the goal line), thereby scoring a goal. When the ball is in play, the players mainly use their feet, but may use any other part of their body, except for their hands or arms, to control, strike, or pass the ball. Only the <a href="/wiki/Goalkeeper_(association_football)" title="Goalkeeper (association football)">goalkeepers</a> may use their hands and arms, and only then within the <a href="/wiki/Penalty_area" title="Penalty area">penalty area</a>. The team that has scored more goals at the end of the game is the winner. There are situations where a goal can be disallowed, such as an offside call or a foul in the build-up to the goal. Depending on the format of the competition, an equal number of goals scored may result in a <a href="/wiki/Tie_(draw)#Association_football" title="Tie (draw)">draw</a> being declared, or the game goes into <a href="/wiki/Overtime_(sports)#Association_football" title="Overtime (sports)">extra time</a> or a <a href="/wiki/Penalty_shoot-out_(association_football)" title="Penalty shoot-out (association football)">penalty shoot-out</a>.<sup id="cite_ref-laws51-52_6-0" class="reference"><a href="#cite_note-laws51-52-6">[5]</a></sup></p>```
# Simple English: ```<p>Games like <a class="key">football</a> have been played around the world since ancient times. The game came from <a class="key">England</a>, where the <a class="key">Football Association</a> wrote a standard set of rules for the game in 1863.</p>```
# Your input will be valid HTML, and your output must also be valid HTML.""",
#     tools=[],
#     model="gpt-4o",
# )

ASSISTANT_ID = "asst_pllDb28NQQGNfOzTN7mb9Ads"

WIKIPEDIA_BODY_CONTENT_ID = "mw-content-text"


def url_to_wid(url: str) -> str:
    """
    Convert a Wikipedia URL to a (w)ID.
    """
    title = url.split("/wiki/")[-1]
    wid = title.replace("_", "-").lower()

    return wid


def save_article(url: str, article: str, short: bool = False) -> None:
    """
    Save the HTML file of an article to disk.
    """
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
    """
    wid = url_to_wid(url)
    file_name = f"{wid}-short.txt" if short else f"{wid}.txt"
    file_path = os.path.join("data", file_name)

    if not os.path.isfile(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    return content


def tidy(html: str) -> str:
    """
    Tidy the HTML content of a Wikipedia article.
    """
    soup = BeautifulSoup(html, "html.parser")

    body = soup.find(id=WIKIPEDIA_BODY_CONTENT_ID)

    # Remove everything from "See also" on
    h2_elements = body.find_all("h2", class_=None)
    for h2_element in h2_elements:
        if h2_element.find("span", id="See_also"):
            while h2_element:
                next_element = h2_element.find_next_sibling()
                h2_element.decompose()
                h2_element = next_element

    # Remove the side panel, if it exists
    infobox = body.find("table", class_="infobox")
    if infobox:
        infobox.decompose()

    text_content = body.get_text()

    # Dump the content into a text file, stripping links, etc.
    # if we had more time, it'd be nice to preserve some structure (e.g., headings, paragraphs)
    # but GPT-4o does pretty well with just this
    lines = text_content.split("\n")
    lines_stripped = [line.strip() for line in lines]
    non_empty_lines = [line for line in lines_stripped if line]
    cleaned_text = "\n".join(non_empty_lines)

    return cleaned_text


def sanitize(output: str) -> str:
    """
    Check for bad parts of the output, by line.

    There's definitely a faster way you could do this, but we're
    dominated by the LLM right now so who cares.
    """
    lines = output.split("\n")

    if lines[0] == "```html":
        lines = lines[1:]

    if lines[-1] == "```":
        lines = lines[:-1]

    return "\n".join(lines)


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print("", end="")

    @override
    def on_text_delta(self, delta, snapshot) -> None:
        print(delta.value, end="")

    @override
    def on_end(self) -> None:
        print("", end="", flush=True)


@app.route("/status", methods=["GET"])
def status() -> Tuple[Response, int]:
    """
    Make sure the API is alive.
    """
    return jsonify({"status": "up"}), 200


@app.route("/simplify", methods=["GET"])
def simplify() -> Tuple[Response, int]:
    """ """
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    # naive caching so the project looks cool
    simple_content = read_article(url, short=True)
    if simple_content is not None:
        return jsonify({"content": simple_content}), 200

    # first, get the article contents
    # checks an on-disk cache first (so we don't get rate-limited, or something)
    html_content = read_article(url)
    if html_content is None:
        try:
            response = requests.get(url)
            response.raise_for_status()

            if DEBUG:
                print(f"Got response of {response.status_code} for {url}")

            html_content = tidy(response.text)
            save_article(url, html_content)
        except requests.RequestException as e:
            return jsonify({"error": str(e)}), 500

    if html_content is None or not html_content:
        return jsonify({"error": "Couldn't get content for page"}), 500

    try:
        thread = client.beta.threads.create()

        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=html_content,
        )

        # TODO(michaelfromyeg): replace this step with data in the actual response
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID,
        )

        print(f"Run for {url} completed with status: {run.status}")

        simple_content = ""
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)

            for message in messages:
                assert message.content[0].type == "text"
                if message.role == "assistant":
                    simple_content += message.content[0].text.value

        sanitized_content = sanitize(simple_content)

        # naive caching part 2
        save_article(url, sanitized_content, short=True)

        return jsonify({"content": sanitized_content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found_error(error):
    response = jsonify({"error": "Not Found", "message": str(error)})
    response.status_code = 404
    return response


@app.errorhandler(500)
def internal_error(error):
    response = jsonify({"error": "Internal Server Error", "message": str(error)})
    response.status_code = 500
    return response


if __name__ == "__main__":
    app.run(debug=True)


def signal_handler(sig, frame):
    print("Received Ctrl+C - cleaning up...")
    # client.beta.assistants.delete(assistant.id)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
