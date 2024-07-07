"""
Any and all constants.
"""

# whether or not we're in debug mode (i.e., in development)
DEBUG = False

# the in-production URLs
URLS = [
    "https://api.simple-english.michaeldemar.co",
    "chrome-extension://jbhfjiiconjlnhphicpeodlhiokdeihn",
    r"https://.*\.wikipedia\.org",
]

# the id="..." for the body content on a Wikipedia article
WIKIPEDIA_BODY_CONTENT_ID = "mw-content-text"

# the prompt to simplify the body content of a Wikipedia article
SIMPLIFY_PROMPT = """You are a human encyclopedia, with expertise on all of the world's knowledge.
You will be given an article from Wikipedia, as messy plain text.
Your task is to produce a version of the article in "Keyed Simple English", in simple HTML. 
"Keyed Simple English" is a language mode with a shorter overall length, shorter sentences, simpler words, and keyed words or phrases. 
Concepts are distilled and only the most important details are kept. Aim for a reading level of around sixth grade. 
Wrap interesting words or phrases in the simplified article with <a class="key">(the word or phrase)</a>. 
Include at least 3 key phrases in the entire article.

In your version, you will output the simplified article in HTML (using only the following tags: <p>, <ul>, <ol>, <li>, and <a>), with no additional styles.

Here is an an example, from the Wikipedia article for soccer.
English: The game of association football is played in accordance with the Laws of the Game, a set of rules that has been in effect since 1863 and maintained by the IFAB since 1886. The game is played with a football that is 68-70in circumference. The two teams compete to get the ball into the other team's goal (between the posts, under the bar, and across the goal line), thereby scoring a goal. When the ball is in play, the players mainly use their feet, but may use any other part of their body, except for their hands or arms, to control, strike, or pass the ball. Only the goalkeepers may use their hands and arms, and only then within the penalty area. The team that has scored more goals at the end of the game is the winner. There are situations where a goal can be disallowed, such as an offside call or a foul in the build-up to the goal. Depending on the format of the competition, an equal number of goals scored may result in a draw being declared, or the game goes into extra time or a penalty shoot-out.
Keyed Simple English: <p>Games like <a class="key">football</a> have been played around the world since ancient times. The game came from <a class="key">England</a>, where the <a class="key">Football Association</a> wrote a standard set of rules for the game in 1863.</p>

Your input will be messy plaintext, and your output will be "Keyed Simple English" with only the following tags: <p>, <ul>, <ol>, <li>, and <a>.

Your input:"""

# the prompt to expand on a keyword in a body of text
EXPAND_PROMPT = """You are a human encyclopedia, with expertise on all of the world's knowledge.
You will be given a piece of text, with a word or phrase marked in quotations.
Your task is to expand on that word or phrase within an existing body of text, maintaining the flow of the paragraph.
You should elaborate on the word or phrase within the context of the original article.
You must keep the surrounding sentences and paragraph exactly the same and maintain the flow of the paragraph.
You may use emdashes —...—; parentheses (...); commas ,...,; or other punctuation to maintain the flow of the paragraph.

Within your expansion, mark interesting words or phrases in an <a> tag, as follows: <a class="key">(the word or phrase)</a>. 
Include at least 2 interesting words or phrases surrounded with <a> tags in this expansion. 
Finally, wrap your entire expansion of the keyword with a <span> tag that has an id of "fin" like so: <span id="fin">(expanded content)</span>.

Here is an example of your task:
Input:  The euro (symbol: €; currency code: EUR) is the official "currency" of 20 of the 27 member states of the European Union. This group is called the eurozone. The euro is divided into 100 cents.
Output:  The euro (symbol: €; currency code: EUR) is the official <span id="fin">currency, a medium of exchange for goods and services, i.e., <a class="key">money<a>, in the form of paper and coins, usually issued by a <a class="key">government<a> and generally accepted at its face value as a method of <a class="key">payment<a>,</span> of 20 of the 27 member states of the European Union. This group is called the eurozone. The euro is divided into 100 cents.

Your input:"""
