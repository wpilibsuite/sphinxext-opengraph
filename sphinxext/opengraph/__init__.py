from typing import Any, Dict
from urllib.parse import urljoin

import docutils.nodes as nodes
from sphinx.application import Sphinx

from .descriptionparser import get_description
from .titleparser import get_title

DEFAULT_DESCRIPTION_LENGTH = 200


def make_tag(property: str, content: str) -> str:
    return f'<meta property="{property}" content="{content}" />\n  '


def get_tags(
    context: Dict[str, Any], doctree: nodes.document, config: Dict[str, Any]
) -> str:

    # Set length of description
    try:
        desc_len = int(config["ogp_description_length"])
    except ValueError:
        desc_len = DEFAULT_DESCRIPTION_LENGTH

    # Get the title and parse any html in it
    title = get_title(context["title"], skip_html_tags=False)
    title_excluding_html = get_title(context["title"], skip_html_tags=True)

    # Parse/walk doctree for metadata (tag/description)
    description = get_description(doctree, desc_len, [title, title_excluding_html])

    tags = "\n  "

    # title tag
    tags += make_tag("og:title", title)

    # type tag
    tags += make_tag("og:type", config["ogp_type"])

    # url tag
    # Get the URL of the specific page
    page_url = urljoin(
        config["ogp_site_url"], context["pagename"] + context["file_suffix"]
    )
    tags += make_tag("og:url", page_url)

    # site name tag
    site_name = config["ogp_site_name"]
    if site_name:
        tags += make_tag("og:site_name", site_name)

    # description tag
    tags += make_tag("og:description", description)

    # image tag
    # Get the image from the config
    image_url = config["ogp_image"]
    if image_url:
        tags += make_tag("og:image", image_url)

    # Add image alt text (either provided by config or from site_name)
    ogp_image_alt = config["ogp_image_alt"]
    if isinstance(ogp_image_alt, str):
        tags += make_tag("og:image:alt", ogp_image_alt)
    elif ogp_image_alt and site_name:
        tags += make_tag("og:image:alt", site_name)
    elif ogp_image_alt and title:
        tags += make_tag("og:image:alt", title)

    # custom tags
    tags += "\n".join(config["ogp_custom_meta_tags"])

    return tags


def html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: Dict[str, Any],
    doctree: nodes.document,
) -> None:
    if doctree:
        context["metatags"] += get_tags(context, doctree, app.config)


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_config_value("ogp_site_url", None, "html")
    app.add_config_value("ogp_description_length", DEFAULT_DESCRIPTION_LENGTH, "html")
    app.add_config_value("ogp_image", None, "html")
    app.add_config_value("ogp_image_alt", True, "html")
    app.add_config_value("ogp_type", "website", "html")
    app.add_config_value("ogp_site_name", None, "html")
    app.add_config_value("ogp_custom_meta_tags", [], "html")

    app.connect("html-page-context", html_page_context)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
