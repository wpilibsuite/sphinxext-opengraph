from typing import Dict, Any
from sphinx.application import Sphinx
from docutils import nodes
from urllib.parse import urljoin
from .util import sanitize_title, make_tag, add_tag_from_config
from .visitor import OpenGraphVisitor


def html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: Dict[str, Any],
    doctree: nodes.document,
) -> None:
    if not doctree:
        return
    # Set length of description
    try:
        desc_len = int(app.config["ogp_description_length"])
    except ValueError:
        desc_len = 200

    # grab the description from the page
    visitor = OpenGraphVisitor(doctree, desc_len)
    doctree.walkabout(visitor)

    # title tag# parse out any html from the title
    page_title = sanitize_title(context["title"])
    context["metatags"] += make_tag("title", page_title)

    # type tag
    context["metatags"] += make_tag("type", app.config["ogp_type"])

    # url tag
    # Get the url to the specific page
    page_url = urljoin(
        app.config["ogp_site_url"], context["pagename"] + context["file_suffix"]
    )
    context["metatags"] += make_tag("url", page_url)

    # site name tag
    add_tag_from_config(context, app.config, "site_name")

    # description tag
    context["metatags"] += make_tag("description", visitor.description)

    # image tag
    # Get the image from the app.config
    add_tag_from_config(context, app.config, "image")

    # image alt text
    # todo: change readme
    add_tag_from_config(context, app.config, "image:alt")

    # custom tags
    context["metatags"] += "\n".join(app.config["ogp_custom_meta_tags"])
