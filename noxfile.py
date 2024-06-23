"""
Configuration to automatically run jobs and tests via `nox`.
For example, to build the documentation with a live server:

  nox -s docs -- live

List available jobs:

  nox -l

ref: https://nox.thea.codes/
"""

import nox
from shlex import split

nox.options.reuse_existing_virtualenvs = True


@nox.session
def docs(session):
    """Build the documentation. Use `-- live` to build with a live server."""
    session.install("-r", "docs/requirements.txt")
    session.install("-e", ".")
    if "live" in session.posargs:
        session.install("ipython")
        session.install("sphinx-autobuild")
        session.run(*split("sphinx-autobuild -b html docs/source docs/build/html"))
    else:
        session.run(
            *split("sphinx-build -nW --keep-going -b html docs/source docs/build/html")
        )


@nox.session
def test(session):
    """Run the test suite."""
    session.install("-e", ".")
    session.install("-r", "dev-requirements.txt")
    session.run(*(["pytest"] + session.posargs))
