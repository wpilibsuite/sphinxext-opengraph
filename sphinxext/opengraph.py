from typing import Any, Dict, Iterable, Sequence, Tuple
from urllib.parse import urljoin
import docutils.nodes as nodes
import string
from html.parser import HTMLParser
import sphinx
from sphinx.application import Sphinx

DEFAULT_DESCRIPTION_LENGTH = 200

class HTMLTextParser(HTMLParser):
    """
    Parse HTML into text
    """
    def __init__(self):
        super().__init__()
        # All text found
        self.text = ""
        # Only text outside of html tags
        self.text_outside_tags = ""
        self.level = 0

    def handle_starttag(self, tag, attrs) -> None:
        self.level += 1
        
    def handle_endtag(self, tag) -> None:
        self.level -= 1

    def handle_data(self, data) -> None:
        self.text += data
        if self.level == 0:
            self.text_outside_tags += data

class OGMetadataCreatorVisitor(nodes.NodeVisitor):
    """
    Finds the title and creates a description from a doctree
    """

    def __init__(self, desc_len: int, known_titles: Iterable[str] = None, document: nodes.document = None):

        # Hack to prevent requirement for the doctree to be passed in.
        # It's only used by doctree.walk(...) to print debug messages. 
        if document == None:
            class document_cls:
                class reporter:
                    @staticmethod
                    def debug(*args, **kwaargs):
                        pass

            document = document_cls()

        if known_titles == None:
            known_titles = []

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

        # Skip comments
        if isinstance(node, nodes.Invisible):
            raise nodes.SkipNode

        # Skip all admonitions
        if isinstance(node, nodes.Admonition):
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
            if self.description[-1] == ",":
                self.description = self.description[:-1]
            self.description += "."
            self.list_level -= 1

        # Check for length
        if len(self.description) > self.desc_len:
            self.description = self.description[: self.desc_len]
            if self.desc_len >= 3:
                self.description = self.description[:-3] + "..."

            self.stop = True


def make_tag(property: str, content: str) -> str:
    return f'<meta property="{property}" content="{content}" />\n  '


def get_tags(context: Dict[str, Any], doctree: nodes.document, config: Dict[str, Any]) -> str:

    # Set length of description
    try:
        desc_len = int(config["ogp_description_length"])
    except ValueError:
        desc_len = DEFAULT_DESCRIPTION_LENGTH

    # Get the title and parse any html in it
    htp = HTMLTextParser()
    htp.feed(context["title"])
    htp.close()

    # Parse/walk doctree for metadata (tag/description)
    mcv = OGMetadataCreatorVisitor(desc_len, [htp.text, htp.text_outside_tags])
    doctree.walkabout(mcv)

    tags = "\n  "

    # title tag
    tags += make_tag("og:title", htp.text)

    # type tag
    tags += make_tag("og:type", config["ogp_type"])

    # url tag
    # Get the URL of the specific page
    page_url = urljoin(
        config["ogp_site_url"],
        context["pagename"] + context["file_suffix"]
    )
    tags += make_tag("og:url", page_url)

    # site name tag
    site_name = config["ogp_site_name"]
    if site_name:
        tags += make_tag("og:site_name", site_name)

    # description tag
    tags += make_tag("og:description", mcv.description)

    # image tag
    # Get the image from the config
    image_url = config["ogp_image"]
    if image_url:
        tags += make_tag("og:image", image_url)

    # custom tags
    tags += '\n'.join(config['ogp_custom_meta_tags'])

    return tags


def html_page_context(app: Sphinx, pagename: str, templatename: str, context: Dict[str, Any], doctree: nodes.document) -> None:
    if doctree:
        context['metatags'] += get_tags(context, doctree, app.config)


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_config_value("ogp_site_url", None, "html")
    app.add_config_value("ogp_description_length", DEFAULT_DESCRIPTION_LENGTH, "html")
    app.add_config_value("ogp_image", None, "html")
    app.add_config_value("ogp_type", "website", "html")
    app.add_config_value("ogp_site_name", None, "html")
    app.add_config_value("ogp_custom_meta_tags", [], "html")

    app.connect('html-page-context', html_page_context)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

