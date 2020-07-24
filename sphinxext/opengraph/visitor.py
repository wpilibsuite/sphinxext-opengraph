from typing import List
from docutils import nodes
from sphinx.util import logging

logger = logging.getLogger(__name__)


class OpenGraphVisitor(nodes.GenericNodeVisitor):
    def __init__(
        self, document: nodes.document, desc_len: int, title_count: int = 1
    ) -> None:
        super().__init__(document)
        self.description = ""
        self.desc_len = desc_len
        self.title_count = title_count

    def default_visit(self, node: nodes.Element):
        if len(self.description) >= self.desc_len:
            # Stop the traversal if the description is long enough
            # raise nodes.StopTraversal
            pass

        if isinstance(node, (nodes.Invisible, nodes.Admonition)):
            # Skip all comments and admonitions
            raise nodes.SkipNode

        if isinstance(node, nodes.title):
            # title count refers to the amount of titles remaining
            self.title_count -= 1
            if self.title_count < 0:
                pass
                # raise nodes.StopTraversal

        logger.info(type(node))
        logger.info(node.astext())
        if isinstance(node, nodes.paragraph):
            # Add only paragraphs to the description
            logger.debug(f"Adding node {type(node)} to description.")
            self.description += node.astext() + "\n"

    def default_departure(self, node: nodes.Element):
        if len(self.description) > self.desc_len:
            self.description = self.description[: self.desc_len]

            if self.desc_len > 3:
                self.description = self.description[:-3] + "..."
