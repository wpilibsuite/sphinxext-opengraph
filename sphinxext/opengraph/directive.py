from typing import List
from sphinx.util.docutils import SphinxDirective
from docutils.nodes import Node


class OpenGraphDirective(SphinxDirective):
    def run(self) -> List[Node]:
        pass

    pass
