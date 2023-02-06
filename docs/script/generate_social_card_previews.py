"""
A helper script to test out what social previews look like.
I should remove this when I'm happy with the result.
"""
# %load_ext autoreload
# %autoreload 2

from pathlib import Path
from textwrap import dedent
from sphinxext.opengraph.socialcards import (
    render_social_card,
    MAX_CHAR_PAGE_TITLE,
    MAX_CHAR_DESCRIPTION,
)
import random

here = Path(__file__).parent

# Dummy lorem text
lorem = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum
""".split()  # noqa

kwargs_fig = dict(
    image=here / "../source/_static/og-logo.png",
    image_mini=here / "../../sphinxext/opengraph/_static/sphinx-logo-shadow.png",
)

print("Generating previews of social media cards...")
plt_objects = None
embed_text = []
for perm in range(20):
    # Create dummy text description and pagetitle for this iteration
    random.shuffle(lorem)
    title = " ".join(lorem[:100])
    title = title[: MAX_CHAR_PAGE_TITLE - 3] + "..."

    random.shuffle(lorem)
    desc = " ".join(lorem[:100])
    desc = desc[: MAX_CHAR_DESCRIPTION - 3] + "..."

    path_tmp = Path(here / "../tmp")
    path_tmp.mkdir(exist_ok=True)
    path_out = Path(path_tmp / f"num_{perm}.png")

    plt_objects = render_social_card(
        path=path_out,
        site_title="Sphinx Social Card Demo",
        page_title=title,
        description=desc,
        siteurl="sphinxext-opengraph.readthedocs.io",
        plt_objects=plt_objects,
        kwargs_fig=kwargs_fig,
    )

    path_examples_page_folder = here / ".."
    embed_text.append(
        dedent(
            f"""
    ````{{grid-item}}
    ```{{image}} ../{path_out.relative_to(path_examples_page_folder)}
    ```
    ````
    """
        )
    )

embed_text = "\n".join(embed_text)
embed_text = f"""
`````{{grid}} 2
:gutter: 5

{embed_text}
`````
"""

# Write markdown text that we can use to embed these images in the docs
(here / "../tmp/embed.txt").write_text(embed_text)

print("Done generating previews of social media cards...")
