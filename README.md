# sphinxext-opengraph
Sphinx extension to generate OpenGraph metadata (https://ogp.me/)

## Installation

`python -m pip install sphinxext-opengraph`

## Options
These values are placed in the conf.py of your sphinx project.

* `ogp_site_url`
    * This config option is very important, set it to the URL the site is being hosted on. 
* `ogp_description_length`
    * Configure the amount of characters taken from a page. The default of 200 is probably good for most people. If something other than a number is used, it defaults back to 200. 
* `ogp_image`
    * This is not required. Link to image to show.
* `ogp_type`
    * This sets the ogp type attribute, for more information on the types available please take a look at https://ogp.me/#types. By default it is set to `website`, which should be fine for most use cases.

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
```
