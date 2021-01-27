from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict
from urllib.parse import urljoin

import docutils.nodes as nodes
from sphinx.application import Sphinx

from .descriptionparser import get_description
from .titleparser import get_title

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

# A selection from https://www.iana.org/assignments/media-types/media-types.xhtml#video
VIDEO_MIME_TYPES = {
    "3gpp": "video/3gpp",
    "3gp2": "video/3gp2",
    "3gpp2": "video/3gpp2",
    "av1": "video/AV1",
    "dv": "video/DV",
    "h263": "video/H263",
    "h264": "video/H264",
    "h265": "video/H265",
    "jpeg": "video/JPEG",
    "jpeg2000": "video/jpeg2000",
    "MPV": "video/MPV",
    "ogg": "video/ogg",
    "quicktime": "video/quicktime",
    "raw": "video/raw",
    "vc1": "video/vc1",
    "vc2": "video/vc2",
    "vp8": "video/VP8",
    "mp4": "video/mp4",
    "webm": "video/webm",
    "m4v": "video/mp4",
}

# A selection from https://www.iana.org/assignments/media-types/media-types.xhtml#audio
AUDIO_MIME_TYPES = {
    "wave": "audio/x-wav",
    "wav": "audio/x-wav",
    "webm": "audio/webm",
    "ogg": "audio/ogg",
    "3gpp": "audio/3gpp",
    "3gpp2": "audio/3gpp2",
    "3gp2": "audio/3gp2",
    "aac": "audio/aac",
    "ac3": "audio/ac3",
    "aptx": "audio/aptx",
    "dv": "audio/DV",
    "mpeg": "audio/mpeg",
    "opus": "audio/opus",
    "vorbis": "audio/vorbis",
    "m3u": "audio/x-mpegurl",
    "m3u8": "audio/x-mpegurl",
    "mid": "audio/midi",
    "midi": "audio/midi",
    "mp2": "audio/mpeg",
    "mp3": "audio/mpeg",
    "m4a": "audio/mp4",
    "aiff": "audio/x-aiff",
}


def make_tag(property: str, content: str) -> str:
    return f'<meta property="{property}" content="{content}" />\n  '


def get_tags(
    app: Sphinx,
    pagename: str,
    context: Dict[str, Any],
    doctree: nodes.document,
    config: Dict[str, Any],
) -> str:

    # Set length of description
    try:
        desc_len = int(config["ogp_description_length"])
    except ValueError:
        desc_len = DEFAULT_DESCRIPTION_LENGTH

    meta = OrderedDict()

    # Get the title and parse any html in it
    title = get_title(context["title"], skip_html_tags=False)
    title_excluding_html = get_title(context["title"], skip_html_tags=True)
    meta["og:title"] = title

    # Parse/walk doctree for metadata (tag/description)
    description = get_description(doctree, desc_len, [title, title_excluding_html])
    meta["og:description"] = description

    # type tag
    meta["og:type"] = config["ogp_type"]

    # url tag
    # Get the URL of the specific page
    page_url = urljoin(
        config["ogp_site_url"], context["pagename"] + context["file_suffix"]
    )
    meta["og:url"] = page_url

    # site name tag
    site_name = config["ogp_site_name"]
    if site_name:
        meta["og:site_name"] = site_name

    # image tag
    # Get basic values from config
    image_url = config["ogp_image"]
    ogp_use_first_image = config["ogp_use_first_image"]
    ogp_image_alt = config["ogp_image_alt"]

    if ogp_use_first_image:
        first_image = doctree.next_node(nodes.image)
        if (
            first_image
            and Path(first_image.get("uri", "")).suffix[1:].lower() in IMAGE_MIME_TYPES
        ):
            image_url = first_image["uri"]
            ogp_image_alt = first_image.get("alt", None)

    if image_url:
        meta["og:image"] = image_url

        # Add image alt text (either provided by config or from site_name)
        if isinstance(ogp_image_alt, str):
            meta["og:image:alt"] = ogp_image_alt
        elif ogp_image_alt is None and site_name:
            meta["og:image:alt"] = site_name
        elif ogp_image_alt is None and title:
            meta["og:image:alt"] = title

    # apply overrides
    # __import__("code").interact(local={**locals(), **globals()})
    meta.update(context.get("meta") or {})

    # fix relative overrides
    for prop in ["og:image", "og:audio", "og:video"]:
        if prop not in meta:
            continue
        value = meta[prop]

        if not (value.startswith("http://") or value.startswith("https://")):
            meta[prop] = app.env.relfn2path(value, pagename)

    # add mime types
    def add_mime_type(prop: str, mime_types: dict):
        if prop not in meta:
            return
        value = meta[prop]
        ext = value.split(".")[-1].split("?")[0].split("#")[0].lower()
        if ext in mime_types:
            meta[prop + ":type"] = mime_types[ext]

    add_mime_type("og:image", IMAGE_MIME_TYPES)
    add_mime_type("og:video", VIDEO_MIME_TYPES)
    add_mime_type("og:audio", AUDIO_MIME_TYPES)

    # write tags
    tags = "".join([make_tag(k, v) for k, v in meta.items()])

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
        context["metatags"] += get_tags(app, pagename, context, doctree, app.config)


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
