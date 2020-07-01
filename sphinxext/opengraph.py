from urllib.parse import urljoin

DEFAULT_DESCRIPTION_LENGTH = 200


def get_tags(context, doctree, config):

    # Get the URL of the specific page
    page_url = urljoin(config["ogp_site_url"], context["pagename"] + context["file_suffix"])
    # Get the image from the config
    image_url = config["ogp_image"]
    # Get the site name from the config
    site_name = config["ogp_site_name"]

    # Get the first X letters from the page (Configured in config)
    description = doctree.astext().replace('\n', ' ')

    try:
        desc_len = int(config["ogp_description_length"])
    except ValueError:
        desc_len = DEFAULT_DESCRIPTION_LENGTH

    if len(description) > desc_len:
        description = description[:desc_len - 3] + "..."

    # Make the ogp tags
    tags = """
    <meta property="og:title" content="{title}" />
    <meta property="og:type" content="{type}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:description" content="{desc}" />
    """.format(title=context["title"], type=config["ogp_type"], url=page_url, desc=description)

    if site_name:
        tags += f'<meta property="og:site_name" content="{site_name}" />'

    if image_url:
        tags += '<meta property="og:image" content="{image}" />'.format(image=image_url)

    return tags


def html_page_context(app, pagename, templatename, context, doctree):
    if doctree:
        context['metatags'] += get_tags(context, doctree, app.config)


def setup(app):
    app.add_config_value("ogp_site_url", None, "html")
    app.add_config_value("ogp_description_length", DEFAULT_DESCRIPTION_LENGTH, "html")
    app.add_config_value("ogp_image", None, "html")
    app.add_config_value("ogp_site_name", None, "html")
    app.add_config_value("ogp_type", "website", "html")

    app.connect('html-page-context', html_page_context)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

