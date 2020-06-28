from urllib.parse import urljoin


def get_tags(context, doctree, config):
    page_url = urljoin(config["ogp_site_url"], context["pagename"] + context["file_suffix"])
    image_url = config["ogp_image"]
    description = doctree.astext().replace('\n', ' ')

    if len(description) > 200:
        description = description[:197] + "..."

    tags = """
    <meta property="og:title" content="{title}" />
    <meta property="og:type" content="{type}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:description" content="{desc}" />
    """.format(title=context["title"], type=config["type"], url=page_url, desc=description)

    if image_url:
        tags += '<meta property="og:image" content="{image}" />'.format(image=image_url)

    return tags


def html_page_context(app, pagename, templatename, context, doctree):
    if doctree:
        context['metatags'] += get_tags(context, doctree, app.config)


def setup(app):
    app.add_config_value("ogp_site_url", None, "html")
    app.add_config_value("ogp_image", None, "html")
    app.add_config_value("ogp_type", "website", "html")

    app.connect('html-page-context', html_page_context)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

