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

    # parse out html from the page title
    page_title = sanitize_title(context["title"])

    # get the page's url
    page_url = urljoin(
        app.config["ogp_site_url"], context["pagename"] + context["file_suffix"]
    )

    # add all the tags which need to be added
    context["metatags"] += make_tag("title", page_title)
    context["metatags"] += make_tag("type", app.config["ogp_type"])
    context["metatags"] += make_tag("url", page_url)
    add_tag_from_config(context, app.config, "site_name")
    context["metatags"] += make_tag("description", visitor.description)
    add_tag_from_config(context, app.config, "image")
    add_tag_from_config(context, app.config, "image:alt")

    # custom tags
    context["metatags"] += "\n".join(app.config["ogp_custom_meta_tags"])
