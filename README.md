# sphinxext-opengraph
![Build](https://github.com/wpilibsuite/sphinxext-opengraph/workflows/Test%20and%20Deploy/badge.svg)

Sphinx extension to generate OpenGraph metadata (https://ogp.me/)

## Installation

`python -m pip install sphinxext-opengraph`

## Usage
Just add `sphinxext.opengraph` to your extensions list in your `conf.py`

```python
extensions = [
   sphinxext.opengraph,
]
```
## Options
These values are placed in the conf.py of your sphinx project.

* `ogp_site_url`
    * This config option is very important, set it to the URL the site is being hosted on. 
* `ogp_description_length`
    * Configure the amount of characters taken from a page. The default of 200 is probably good for most people. If something other than a number is used, it defaults back to 200. 
* `ogp_site_name`
    * This is not required. Name of the site. This is displayed above the title.
* `ogp_image`
    * This is not required. Link to image to show.
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
