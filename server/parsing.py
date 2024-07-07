"""
Parsing helpers. Right now, just focused on Wikipedia.

Maybe I should refactor it into classes or structs or something.
"""

from bs4 import BeautifulSoup

from .constants import WIKIPEDIA_BODY_CONTENT_ID


def tidy_for_summary(html: str) -> str:
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
    # ...but the LLMs do pretty well with just this

    # TODO(michaelfromyeg): re-write to preserve more of the original structure
    lines = text_content.split("\n")
    lines_stripped = [line.strip() for line in lines]
    non_empty_lines = [line for line in lines_stripped if line]
    cleaned_text = "\n".join(non_empty_lines)

    return cleaned_text


def sanitize_summary(output: str) -> str:
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


def format_for_expand(html: str) -> str:
    """
    For the expand task, we need to format the HTML content.
    """
    soup = BeautifulSoup(html, "html.parser")

    selected_element = soup.find(id="selected")

    if selected_element:
        placeholder = "PLACEHOLDER_FOR_SELECTED"
        selected_text = selected_element.get_text()
        selected_element.replace_with(placeholder)

    text_only_with_marked_key = soup.get_text()

    if selected_element:
        replacement_text = f'"{selected_text}"'
        text_only_with_marked_key = text_only_with_marked_key.replace(
            placeholder, replacement_text
        )

    return text_only_with_marked_key


def get_expanded_contents(html: str) -> str:
    """
    Get the inner contents of the expanded text.
    """
    soup = BeautifulSoup(html, "html.parser")
    generated_text = soup.find(id="fin")

    inner_generated_text = "".join(str(element) for element in generated_text.contents)

    return inner_generated_text
