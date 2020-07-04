from urllib.parse import urljoin

DEFAULT_DESCRIPTION_LENGTH = 200

def make_tag(property: str, content: str) -> str:
    return f'<meta property="{property}" content="{content}" />\n  '

def get_tags(context, doctree, config):
    tags = ""

    # title tag
    tags += make_tag("og:title", context["title"])

    # type tag
    tags += make_tag("og:type", config["ogp_type"])

    # url tag
    # Get the URL of the specific page
    page_url = urljoin(
        config["ogp_site_url"],
        context["pagename"] + context["file_suffix"]
    )
    tags += make_tag("og:url", page_url)


    # description tag
    # Get the first X letters from the page (Configured in config)
    description = doctree.astext().replace('\n', ' ')

    try:
        desc_len = int(config["ogp_description_length"])
    except ValueError:
        desc_len = DEFAULT_DESCRIPTION_LENGTH

    if len(description) > desc_len:
        description = description[:desc_len - 3] + "..."

    tags += make_tag("og:description", description)

    # image tag
    # Get the image from the config
    image_url = config["ogp_image"]
    if image_url:
        tags += make_tag("og:image", image_url)

    return tags


def html_page_context(app, pagename, templatename, context, doctree):
    if doctree:
        context['metatags'] += get_tags(context, doctree, app.config)


def setup(app):
    app.add_config_value("ogp_site_url", None, "html")
    app.add_config_value("ogp_description_length", DEFAULT_DESCRIPTION_LENGTH, "html")
    app.add_config_value("ogp_image", None, "html")
    app.add_config_value("ogp_type", "website", "html")

    app.connect('html-page-context', html_page_context)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

