import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from openai import AssistantEventHandler, OpenAI
from typing_extensions import override

load_dotenv()

DEBUG = False

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

assistant = client.beta.assistants.create(
    name="Simple English Wikipedia Assistant",
    instructions="""You are a human encyclopedia, with expertise on all of the world's knowledge.
You will be given an article from Wikipedia, as HTML.
Your job is to produce a version of the article in "Keyed Simple English", also in HTML. "Keyed Simple English" is a language mode with a shorter overall length, shorter sentences, simpler words, and keyed words or phrases. Concepts are distilled and only the most important details are kept. Aim for a reading level of around sixth grade. In your outputted version, you will remove all links to other Wikipedia pages or external sources. Instead, wrap interesting words or phrases in the simplified article with <a class="key">(the word or phrase)</a>. Do this sparingly, for concepts or words you think the user might want to learn more about. Include at least 3 key phrases in the entire article.
Here is an an example, from the Wikipedia article for soccer. 
English: ```<p>The game of association football is played in accordance with the <a href="/wiki/Laws_of_the_Game_(association_football)" title="Laws of the Game (association football)">Laws of the Game</a>, a set of rules that has been in effect since 1863 and maintained by the <a href="/wiki/International_Football_Association_Board" title="International Football Association Board">IFAB</a> since 1886. The game is played with a <a href="/wiki/Ball_(association_football)" title="Ball (association football)">football</a> that is 68–70&nbsp;cm (27–28&nbsp;in) in <a href="/wiki/Circumference" title="Circumference">circumference</a>. The two teams compete to get the ball into the other team's goal (between the posts, under the bar, and across the goal line), thereby scoring a goal. When the ball is in play, the players mainly use their feet, but may use any other part of their body, except for their hands or arms, to control, strike, or pass the ball. Only the <a href="/wiki/Goalkeeper_(association_football)" title="Goalkeeper (association football)">goalkeepers</a> may use their hands and arms, and only then within the <a href="/wiki/Penalty_area" title="Penalty area">penalty area</a>. The team that has scored more goals at the end of the game is the winner. There are situations where a goal can be disallowed, such as an offside call or a foul in the build-up to the goal. Depending on the format of the competition, an equal number of goals scored may result in a <a href="/wiki/Tie_(draw)#Association_football" title="Tie (draw)">draw</a> being declared, or the game goes into <a href="/wiki/Overtime_(sports)#Association_football" title="Overtime (sports)">extra time</a> or a <a href="/wiki/Penalty_shoot-out_(association_football)" title="Penalty shoot-out (association football)">penalty shoot-out</a>.<sup id="cite_ref-laws51-52_6-0" class="reference"><a href="#cite_note-laws51-52-6">[5]</a></sup></p>```
Simple English: ```<p>Games like <a class="key">football</a> have been played around the world since ancient times. The game came from <a class="key">England</a>, where the <a class="key">Football Association</a> wrote a standard set of rules for the game in 1863.</p>```
Your input will be valid HTML, and your output must also be valid HTML.""",
    tools=[],
    model="gpt-4o",
)


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print("\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)


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

    try:
        thread = client.beta.threads.create()

        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="<p><i><b>Hockey</b></i> is a term used to denote a family of various types of both summer and winter team sports which originated on either an outdoor field, sheet of ice, or dry floor such as in a gymnasium. While these sports vary in specific rules, numbers of players, apparel, and playing surface, they share broad characteristics of two opposing teams using a stick to propel a ball or disk into a goal. </p>",
        )

        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=EventHandler(),
        ) as stream:
            stream.until_done()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ok"}), 200


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
