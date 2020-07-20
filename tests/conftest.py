from sphinx.testing.path import path
import pytest
from bs4 import BeautifulSoup

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir():
    return path(__file__).parent.abspath() / "roots"


@pytest.fixture()
def content(app):
    app.build()
    yield app


def _meta_tags(content):
    c = (content.outdir / "index.html").read_text()
    return BeautifulSoup(c, "html.parser").find_all("meta")


@pytest.fixture()
def meta_tags(content):
    return _meta_tags(content)


@pytest.fixture()
def og_meta_tags(content):
    return [
        tag for tag in _meta_tags(content) if tag.get("property", "").startswith("og:")
    ]


def pytest_configure(config):
    config.addinivalue_line("markers", "sphinx")
