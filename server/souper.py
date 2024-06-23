from bs4 import BeautifulSoup

with open("data/stanley_cup_finals.html") as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, "html.parser")

print(soup.prettify())
