# sphinxext-opengraph
![Build](https://github.com/wpilibsuite/sphinxext-opengraph/workflows/Test%20and%20Deploy/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Sphinx extension to generate OpenGraph metadata (https://ogp.me/)

## Installation

`python -m pip install sphinxext-opengraph`

## Usage
Just add `sphinxext.opengraph` to your extensions list in your `conf.py`

```python
extensions = [
   "sphinxext.opengraph",
]
```
## Options
These values are placed in the conf.py of your sphinx project.

Users hosting documentation on Read The Docs *do not* need to set any of the following unless custom configuration is wanted. The extension will automatically retrieve your site url.

* `ogp_site_url`
    * This config option is very important, set it to the URL the site is being hosted on. 
* `ogp_description_length`
    * Configure the amount of characters taken from a page. The default of 200 is probably good for most people. If something other than a number is used, it defaults back to 200. 
* `ogp_site_name`
    * This is not required. Name of the site. This is displayed above the title.
* `ogp_image`
    * This is not required. Link to image to show. Note that all relative paths are converted to be relative to the root of the html output as defined by `ogp_site_name.
* `ogp_image_alt`
    * This is not required. Alt text for image. Defaults to using `ogp_site_name` or the document's title as alt text, if available. Set to `False` if you want to turn off alt text completely.
* `ogp_use_first_image`
    * This is not required. Set to True to use each page's first image, if available. If set to True but no image is found, Sphinx will use `ogp_image` instead.
* `ogp_type`
    * This sets the ogp type attribute, for more information on the types available please take a look at https://ogp.me/#types. By default it is set to `website`, which should be fine for most use cases.
* `ogp_custom_meta_tags`
    * This is not required. List of custom html snippets to insert.
    
## Example Config

### Simple Config

```python
ogp_site_url = "http://example.org/"
ogp_image = "http://example.org/image.png"
```

### Advanced Config

```python
ogp_site_url = "http://example.org/"
ogp_image = "http://example.org/image.png"
ogp_description_length = 300
ogp_type = "article"

ogp_custom_meta_tags = [
    '<meta property="og:ignore_canonical" content="true" />',
]

```

## Per Page Overrides
[Field lists](https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html) are used to allow you to override certain settings on each page and set unsupported arbitrary OpenGraph tags.

Make sure you place the fields at the very start of the document such that Sphinx will pick them up and also won't build them into the html.

### Overrides
These are some overrides that can be used, you can actually override any tag and field lists will always take priority.

* `:og_description_length:`
  * Configure the amount of characters to grab for the description of the page. If the value isn't a number it will fall back to `ogp_description_length`. Note the slightly different syntax because this isn't directly an OpenGraph tag.
* `:og:description:`
  * Lets you override the description of the page.
* `:og:title:`
  * Lets you override the title of the page.
* `:og:type:`
  * Override the type of the page, for the list of available types take a look at https://ogp.me/#types.
* `:ogp:image:`
  * Set the image for the page.[^1]
* `:ogp:image:alt:`
  * Sets the alt text. Will be ignored if there is no image set.

### Example
Remember that the fields **must** be placed at the very start of the file. You can verify Sphinx has picked up the fields if they aren't shown in the final html file.

```rst
:og:description: New description
:og:image: http://example.org/image.png
:og:image:alt: Example Image

Page contents
=============
```

### Arbitrary Tags[^1]
Additionally, you can use field lists to add any arbitrary OpenGraph tag not supported by the extension. The syntax for arbitrary tags is the same with `:og:tag: content`. For Example:

```rst
:og:video: http://example.org/video.mp4

Page contents
=============
```

[^1]: Note: Relative file paths for images, videos and audio are currently **not** supported when using field lists. Please use an absolute path instead.
