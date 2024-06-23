from bs4 import BeautifulSoup

with open("data/stanley_cup_finals.html") as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, "html.parser")
# print(soup.prettify())

WIKIPEDIA_BODY_CONTENT_ID = "mw-content-text"

body = soup.find(id=WIKIPEDIA_BODY_CONTENT_ID)
print(body.prettify())
