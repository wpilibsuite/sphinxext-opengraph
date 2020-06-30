import pytest


def get_tag(tags, tag_type):
    return [tag for tag in tags if tag.get("property") == "og:{}".format(tag_type)][0]


def get_tag_content(tags, tag_type):
    # Gets the content of a specific ogp tag
    return get_tag(tags, tag_type).get("content", "")


@pytest.mark.sphinx("html", testroot="simple")
def test_simple(og_meta_tags):
    description = get_tag_content(og_meta_tags, "description")

    assert len(og_meta_tags) > 0
    assert get_tag_content(og_meta_tags, "type") == "website"
    assert len(description) == 200
    assert description == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse at lorem ornare, fringilla massa nec, venenatis mi. Donec erat sapien, tincidunt nec rhoncus nec, scelerisque id diam. Orci vari..."


@pytest.mark.sphinx("html", testroot="simple")
def test_site_url(og_meta_tags):
    # Uses the same directory as simple, because it already contains url for a minimal config
    assert get_tag_content(og_meta_tags, "url") == "http://example.org/index.html"


@pytest.mark.sphinx("html", testroot="image")
def test_image(og_meta_tags):
    assert get_tag_content(og_meta_tags, "image") == "http://example.org/image.png"


@pytest.mark.sphinx("html", testroot="type")
def test_type(og_meta_tags):
    assert get_tag_content(og_meta_tags, "type") == "article"


@pytest.mark.sphinx("html", testroot="description-length")
def test_description_length(og_meta_tags):
    assert len(get_tag_content(og_meta_tags, "description")) == 50
