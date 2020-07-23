from typing import Dict, Any
from sphinx.config import Config
from docutils import nodes
from .visitor import OpenGraphVisitor
from sphinx.util import logging
logger = logging.getLogger(__name__)


def insert_tags(context: Dict[str, Any],
                doctree: nodes.document,
                config: Config) -> None:
    visitor = OpenGraphVisitor(doctree, 300)
    doctree.walkabout(visitor)
    logger.info(visitor.description)
    logger.info(len(visitor.description))
