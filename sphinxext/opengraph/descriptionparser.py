from __future__ import annotations

import string
from typing import TYPE_CHECKING

import docutils.nodes as nodes

if TYPE_CHECKING:
    from collections.abc import Set


class DescriptionParser(nodes.NodeVisitor):
    """
    Finds the title and creates a description from a doctree
    """

    def __init__(
        self,
        document: nodes.document,
        *,
        desc_len: int,
        known_titles: Set[str] = frozenset(),
    ) -> None:
        super().__init__(document)
        self.description = ""
        self.desc_len = desc_len
        self.list_level = 0
        self.known_titles = known_titles
        self.first_title_found = False

        # Exceptions can't be raised from dispatch_departure()
        # This is used to loop the stop call back to the next dispatch_visit()
        self.stop = False

    def dispatch_visit(self, node: nodes.Element) -> None:
        if self.stop:
            raise nodes.StopTraversal

        # Skip comments & all admonitions
        if isinstance(node, (nodes.Admonition, nodes.Invisible)):
            raise nodes.SkipNode

        # Mark start of nested lists
        if isinstance(node, nodes.Sequential):
            self.list_level += 1
            if self.list_level > 1:
                self.description += "-"

        # Skip the first title if it's the title of the page
        if not self.first_title_found and isinstance(node, nodes.title):
            self.first_title_found = True
            if node.astext() in self.known_titles:
                raise nodes.SkipNode

        if isinstance(node, nodes.raw) or isinstance(node.parent, nodes.literal_block):
            raise nodes.SkipNode

        # Only include leaf nodes in the description
        if len(node.children) == 0:
            text = node.astext().replace("\r", "").replace("\n", " ").strip()

            # Remove double spaces
            while text.find("  ") != -1:
                text = text.replace("  ", " ")

            # Put a space between elements if one does not already exist.
            if (
                len(self.description) > 0
                and len(text) > 0
                and self.description[-1] not in string.whitespace
                and text[0] not in string.whitespace + string.punctuation
            ):
                self.description += " "

            self.description += text

    def dispatch_departure(self, node: nodes.Element) -> None:
        # Separate title from text
        if isinstance(node, nodes.title):
            self.description += ":"

        # Separate list elements
        if isinstance(node, nodes.Part):
            self.description += ","

        # Separate end of list from text
        if isinstance(node, nodes.Sequential):
            if self.description and self.description[-1] == ",":
                self.description = self.description[:-1]
            self.description += "."
            self.list_level -= 1

        # Check for length
        if len(self.description) > self.desc_len:
            self.description = self.description[: self.desc_len]
            if self.desc_len >= 3:
                self.description = self.description[:-3] + "..."

            self.stop = True


def get_description(
    doctree: nodes.document,
    description_length: int,
    known_titles: Set[str] = frozenset(),
) -> str:
    mcv = DescriptionParser(
        doctree, desc_len=description_length, known_titles=known_titles
    )
    doctree.walkabout(mcv)
    return mcv.description
