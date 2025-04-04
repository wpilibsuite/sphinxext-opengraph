"""Configuration to automatically run jobs and tests via `nox`.

For example, to build the documentation with a live server:

  nox -s docs -- live

List available jobs:

  nox -l

ref: https://nox.thea.codes/
"""

from __future__ import annotations

from shlex import split

import nox

nox.options.reuse_existing_virtualenvs = True


@nox.session
def docs(session: nox.Session) -> None:
    """Build the documentation. Use `-- live` to build with a live server."""
    session.install("--group", "docs")
    session.install("-e", ".")
    if "live" in session.posargs:
        session.install("ipython")
        session.install("sphinx-autobuild")
        session.run(*split("sphinx-autobuild -b html docs/source docs/build/html"))
    else:
        session.run(
            *split("sphinx-build -nW --keep-going -b html docs/source docs/build/html"),
        )


@nox.session
def test(session: nox.Session) -> None:
    """Run the test suite."""
    session.install("-e", ".")
    session.install("--group", "test")
    session.run("pytest", *session.posargs)
