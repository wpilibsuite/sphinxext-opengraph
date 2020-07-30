from typing import Dict, Any
from sphinx.config import Config
from .html_parser import HTMLTextParser


def make_tag(tag: str, content: str) -> str:
    return f'<meta property="og:{tag}" content="{content}" />\n  '


def add_tag_from_config(context: Dict[str, Any], config: Config, tag: str, conf_name: str = ""):
    if not conf_name:
        conf_name = tag.replace(":", "_")

    conf_name = f"ogp_{conf_name}"

    value = config[conf_name]
    if value:
        context["metatags"] += make_tag(tag, value)


def sanitize_title(title: str) -> str:
    # take in a title and return a clean version.
    html_parser = HTMLTextParser()
    html_parser.feed(title)
    html_parser.close()

    return html_parser.text
