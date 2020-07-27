from docutils import nodes


class OpenGraphVisitor(nodes.GenericNodeVisitor):
    def __init__(
        self, document: nodes.document, desc_len: int, title_count: int = 1
    ) -> None:
        super().__init__(document)
        self.description = ""
        self.desc_len = desc_len
        self.title_count = title_count
        self.first_list = ""  # todo: rename

    def default_visit(self, node: nodes.Element) -> None:
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
                # raise nodes.StopTraversal
                pass

        if not self.first_list and isinstance(
            node, (nodes.bullet_list, nodes.enumerated_list)
        ):
            # get the first list on a page to be used instead of description
            self.first_list = node.astext().replace("\n\n", ", ")

        if isinstance(node, nodes.paragraph):
            # Add only paragraphs to the description

            if self.description:
                # add a space between paragraphs in case one does not exist
                # if there is a double space it will be removed automatically
                self.description += " "

            self.description += node.astext()

    def default_departure(self, node: nodes.Element) -> None:
        # remove all double spaces
        self.description = self.description.replace("  ", " ")

        if len(self.description) > self.desc_len:
            self.description = self.description[: self.desc_len]

            if self.desc_len > 3:
                self.description = self.description[:-3] + "..."

        # runs only when this is the last node
        if node.parent is None:
            # switch to use the list if the description is only the same list
            if self.description == self.first_list.replace(
                ",", ""
            ):
                self.description = self.first_list
