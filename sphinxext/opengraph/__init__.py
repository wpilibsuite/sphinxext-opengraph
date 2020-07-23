from typing import Any, Dict
from .directive import OpenGraphDirective
from .event_handler import html_page_context
from sphinx.application import Sphinx


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_config_value("ogp_site_url", None, "html")
    app.add_config_value("ogp_description_length", 200, "html")
    app.add_config_value("ogp_image", None, "html")
    app.add_config_value("ogp_image_alt", True, "html")
    app.add_config_value("ogp_type", "website", "html")
    app.add_config_value("ogp_site_name", None, "html")
    app.add_config_value("ogp_custom_meta_tags", [], "html")

    # app.add_directive("opengraph", OpenGraphDirective)

    app.connect("html-page-context", html_page_context)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
