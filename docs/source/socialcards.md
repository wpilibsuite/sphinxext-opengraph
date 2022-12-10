# Social media card images

This extension will automatically generate a PNG meant for sharing documentation links on social media platforms.
These cards display metadata about the page that you link to, and are meant to catch the attention of readers.

See [the opengraph.xyz website](https://www.opengraph.xyz/) for a way to preview what your social media cards look like.
Here's an example of what the card for this page looks like:

% This causes an *expected* warning because the image doesn't exist relative
%   to the source file, but it does exist relative to the built HTML file.
%   So we expect Sphinx to say the image doesn't exist but it'll look correct in HTML.
```{image} /_images/social_previews/summary_socialcards.png
:width: 500
```

## Disable card images

To disable social media card images, use the following configuration:

```{code-block} python
:caption: conf.py

ogp_social_cards = {
    "enable": False
}
```

## Customize the card

There are several customization options to change the text and look of the social media preview card.
Below is a summary of these options.

- **`site_url`**: Set a custom site URL.
- **`image`**: Over-ride the top-right image (by default, `html_logo` is used).
- **`line_color`**: Color of the border line at the bottom of the card, in hex format.
% TODO: add an over-ride for each part of the card.