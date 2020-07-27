from typing import Dict, Any
from sphinx.config import Config
from docutils import nodes
from urllib.parse import urljoin
from .visitor import OpenGraphVisitor
from .html_parser import HTMLTextParser


def make_tag(property: str, content: str) -> str:
    return f'<meta property="{property}" content="{content}" />\n  '


def insert_tags(
    context: Dict[str, Any], doctree: nodes.document, config: Config
) -> None:
    # Set length of description
    try:
        desc_len = int(config["ogp_description_length"])
    except ValueError:
        desc_len = 300

    # parse out any html from the title
    html_parser = HTMLTextParser()
    if context["title"] != "&lt;no title&gt;":
        # only use title if its exists
        html_parser.feed(context["title"])
    html_parser.close()

    # grab the description from the page
    visitor = OpenGraphVisitor(doctree, desc_len)
    doctree.walkabout(visitor)

    # title tag
    context["metatags"] += make_tag("og:title", html_parser.text)

    # type tag
    context["metatags"] += make_tag("og:type", config["ogp_type"])

    # url tag
    # Get the url to the specific page
    page_url = urljoin(
        config["ogp_site_url"], context["pagename"] + context["file_suffix"]
    )
    context["metatags"] += make_tag("og:url", page_url)

    # site name tag
    site_name = config["ogp_site_name"]
    if site_name:
        context["metatags"] += make_tag("og:site_name", site_name)

    # description tag
    context["metatags"] += make_tag("og:description", visitor.description)

    # image tag
    # Get the image from the config
    image_url = config["ogp_image"]
    if image_url:
        context["metatags"] += make_tag("og:image", image_url)

    # image alt text
    # todo: change readme
    ogp_image_alt = config["ogp_image_alt"]
    if ogp_image_alt:
        context["metatags"] += make_tag("og:image:alt", ogp_image_alt)

    # custom tags
    context["metatags"] += "\n".join(config["ogp_custom_meta_tags"])
