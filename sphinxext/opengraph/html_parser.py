from html.parser import HTMLParser


class HTMLTextParser(HTMLParser):
    """
    Parse HTML into text
    """

    def __init__(self):
        super().__init__()
        # Text from html tags
        self.text = ""

    def handle_data(self, data) -> None:
        self.text += data
