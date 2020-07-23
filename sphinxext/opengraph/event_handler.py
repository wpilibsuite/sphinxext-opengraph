from typing import Dict, Any
from sphinx.application import Sphinx
from docutils import nodes
from .util import insert_tags


def html_page_context(
        app: Sphinx,
        pagename: str,
        templatename: str,
        context: Dict[str, Any],
        doctree: nodes.document) -> None:
    if doctree:
        insert_tags(context, doctree, app.config)
