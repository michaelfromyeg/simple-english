from bs4 import BeautifulSoup

DEBUG = True


def tidy_html(html: str) -> str:
    """
    Tidy the HTML content of a Wikipedia article.
    """
    soup = BeautifulSoup(html, "html.parser")

    WIKIPEDIA_BODY_CONTENT_ID = "mw-content-text"

    body = soup.find(id=WIKIPEDIA_BODY_CONTENT_ID)

    h2_elements = soup.find_all("h2", class_=None)
    for h2_element in h2_elements:
        if h2_element.find("span", id="See_also"):
            while h2_element:
                next_element = h2_element.find_next_sibling()
                h2_element.decompose()
                h2_element = next_element

    text_content = body.get_text()

    lines = text_content.split("\n")

    # Remove leading and trailing whitespace from each line
    lines_stripped = [line.strip() for line in lines]

    # Remove empty lines
    non_empty_lines = [line for line in lines_stripped if line]

    # Join the non-empty lines with newlines
    cleaned_text = "\n".join(non_empty_lines)

    # Print the cleaned text
    print(cleaned_text)
    return cleaned_text


with open("data/stanley-cup-finals.html") as f:
    html_doc = f.read()

tidied = tidy_html(html_doc)

with open("data/stanley-cup-finals-tidied.txt", "w", encoding="utf-8") as f:
    f.write(tidied)
