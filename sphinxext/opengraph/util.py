from .html_parser import HTMLTextParser


def make_tag(tag: str, content: str) -> str:
    return f'<meta property="og:{tag}" content="{content}" />\n  '


def sanitize_title(title: str) -> str:
    # take in a title and return a clean version.
    html_parser = HTMLTextParser()
    html_parser.feed(title)
    html_parser.close()

    return html_parser.text
