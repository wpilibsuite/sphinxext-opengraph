import posixpath
from typing import Any, Dict
from urllib.parse import urljoin, urlparse, urlunparse
from pathlib import Path, PurePosixPath

import docutils.nodes as nodes
from sphinx.application import Sphinx
from sphinx.util import images

from .descriptionparser import get_description
from .titleparser import get_title

import os


DEFAULT_DESCRIPTION_LENGTH = 200

# A selection from https://www.iana.org/assignments/media-types/media-types.xhtml#image
IMAGE_MIME_TYPES = {
    "gif": "image/gif",
    "apng": "image/apng",
    "webp": "image/webp",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "png": "image/png",
    "bmp": "image/bmp",
    "heic": "image/heic",
    "heif": "image/heif",
    "tiff": "image/tiff",
}


def image_abs_url(image_uri: str, docname: str, site_url: str, app: Sphinx):
    parsed_url = urlparse(image_uri)

    if not parsed_url.scheme:
        # Convert relative url to absolute urls and make sure image gets copied on build
        return urljoin(site_url, note_image(parsed_url.path, docname, app))

    return image_uri


def note_image(image_path: str, docname: str, app: Sphinx):
    # potentially temporary solution
    if any([PurePosixPath(image_path).match(dir + "/*") for dir in app.config["html_static_path"] + app.config["html_extra_path"]]):
        return image_path

    if not (image_path.startswith('/') or image_path.startswith(os.sep)):
        image_path = str(PurePosixPath(docname).parent / image_path)

    new_path = app.builder.images[image_path] = app.env.images.add_file(docname, image_path)
    return posixpath.join(app.builder.imgpath, new_path)


def make_tag(property: str, content: str) -> str:
    # Parse quotation, so they won't break html tags if smart quotes are disabled
    content = content.replace('"', "&quot;")
    return f'<meta property="{property}" content="{content}" />\n  '


def get_tags(
    app: Sphinx,
    context: Dict[str, Any],
    doctree: nodes.document,
    config: Dict[str, Any],
) -> str:
    docname = context["pagename"]
    # Get field lists for per-page overrides
    fields = context["meta"]
    if fields is None:
        fields = {}
    tags = {}

    # Set length of description
    try:
        desc_len = int(
            fields.get("ogp_description_length", config["ogp_description_length"])
        )
    except ValueError:
        desc_len = DEFAULT_DESCRIPTION_LENGTH

    # Get the title and parse any html in it
    title = get_title(context["title"], skip_html_tags=False)
    title_excluding_html = get_title(context["title"], skip_html_tags=True)

    # Parse/walk doctree for metadata (tag/description)
    description = get_description(doctree, desc_len, [title, title_excluding_html])

    # title tag
    tags["og:title"] = title

    # type tag
    tags["og:type"] = config["ogp_type"]

    if os.getenv("READTHEDOCS") and config["ogp_site_url"] is None:
        # readthedocs uses html_baseurl for sphinx > 1.8
        parse_result = urlparse(config["html_baseurl"])

        if config["html_baseurl"] is None:
            raise EnvironmentError("ReadTheDocs did not provide a valid canonical URL!")

        # Grab root url from canonical url
        config["ogp_site_url"] = urlunparse(
            (
                parse_result.scheme,
                parse_result.netloc,
                parse_result.path,
                "",
                "",
                "",
            )
        )

    # url tag
    # Get the URL of the specific page
    if context["builder"] == "dirhtml":
        page_url = urljoin(config["ogp_site_url"], docname + "/")
    else:
        page_url = urljoin(
            config["ogp_site_url"], docname + context["file_suffix"]
        )
    tags["og:url"] = page_url

    # site name tag
    site_name = config["ogp_site_name"]
    if site_name:
        tags["og:site_name"] = site_name

    # description tag
    if description:
        tags["og:description"] = description

    # image tag
    # Get basic values from config or field list
    #image_url = fields.pop("og:image", config["ogp_image"])
    #ogp_image_alt = fields.pop("og:image:alt", config["ogp_image_alt"])
    if "og:image" in fields:
        image_url = image_abs_url(fields.pop("og:image"), docname, site_name, app)
        image_alt = fields.pop("og:image:alt", None)
    elif fields.get("ogp_use_first_image", config["ogp_use_first_image"]) and (first_image := doctree.next_node(nodes.image)):
        image_url = first_image["uri"]
        image_alt = first_image.get("alt", None)
    else:
        image_url = config["ogp_image"]
        # if alt text isn't provided, use site_name instead
        image_alt = config["ogp_image_alt"]

    if image_url:
        image_url_parsed = urlparse(image_url)
        if not image_url_parsed.scheme:
            # Relative image path detected. Make absolute.
            image_url = urljoin(config["ogp_site_url"], note_image(image_url_parsed.path, docname, app))
        tags["og:image"] = image_url

        # Add image alt text (either provided by config or from site_name)
        if isinstance(image_alt, str):
            tags["og:image:alt"] = image_alt
        elif image_alt is None and site_name:
            tags["og:image:alt"] = site_name
        elif image_alt is None and title:
            tags["og:image:alt"] = title

    # arbitrary tags and overrides
    tags.update({k: v for k, v in fields.items() if k.startswith("og:")})

    return "\n" + "\n".join(
        [make_tag(p, c) for p, c in tags.items()] + config["ogp_custom_meta_tags"]
    )


def html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: Dict[str, Any],
    doctree: nodes.document,
) -> None:
    if doctree:
        context["metatags"] += get_tags(app, context, doctree, app.config)


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_config_value("ogp_site_url", None, "html")
    app.add_config_value("ogp_description_length", DEFAULT_DESCRIPTION_LENGTH, "html")
    app.add_config_value("ogp_image", None, "html")
    app.add_config_value("ogp_image_alt", None, "html")
    app.add_config_value("ogp_use_first_image", False, "html")
    app.add_config_value("ogp_type", "website", "html")
    app.add_config_value("ogp_site_name", None, "html")
    app.add_config_value("ogp_custom_meta_tags", [], "html")

    app.connect("html-page-context", html_page_context)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
