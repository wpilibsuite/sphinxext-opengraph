===================
sphinxext-opengraph
===================

.. image:: https://img.shields.io/pypi/v/sphinxext-opengraph.svg
   :target: https://pypi.org/project/sphinxext-opengraph/
   :alt: Package on PyPI

.. image:: https://github.com/sphinx-doc/sphinxext-opengraph/actions/workflows/test.yml/badge.svg
   :target: https://github.com/sphinx-doc/sphinxext-opengraph/actions
   :alt: Build Status

.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause
   :alt: BSD 3 Clause

Sphinx extension to generate `Open Graph metadata`_
for each page of your documentation.

Installation
============

.. code-block:: sh

   python -m pip install sphinxext-opengraph

The ``matplotlib`` package is required to generate social cards:

.. code-block:: sh

   python -m pip install sphinxext-opengraph[social_cards]

Usage
=====

Just add ``sphinxext.opengraph`` to the extensions list in ``conf.py``

.. code-block:: python

   extensions = [
      'sphinxext.opengraph',
   ]

Options
=======

These values are placed in the ``conf.py`` of your Sphinx project.

Users hosting documentation on Read The Docs *do not* need to set any of the
following unless custom configuration is wanted.
The extension will automatically retrieve your site URL.

``ogp_site_url``
  This config option is important, set it to the URL the site is being hosted on. 

``ogp_description_length``
  Configure the number of characters taken from a page.
  The default of 200 is probably good for most people.
  If something other than a number is used, it defaults back to 200. 

``ogp_site_name``
  **Optional.**
  Name of the site.
  This is displayed above the title.
  Defaults to the Sphinx project__ config value.
  Set to ``False`` to unset and use no default.

  __ https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-project

``ogp_social_cards``
  Configuration for automatically creating social media card PNGs for each page.
  For more information, see `the social media cards docs`__.

  __ https://github.com/sphinx-doc/sphinxext-opengraph/blob/main/docs/socialcards.md

``ogp_image``
  **Optional.**
  Link to image to show.
  Note that all relative paths are converted to be relative to
  the root of the HTML output as defined by ``ogp_site_url``.

``ogp_image_alt``
  **Optional.**
  Alt text for image.
  Defaults to using ``ogp_site_name`` or the document's title as alt text,
  if available.
  Set to ``False`` if you want to turn off alt text completely.

``ogp_use_first_image``
  **Optional.**
  Set to ``True`` to use each page's first image, if available.
  If set to ``True`` but no image is found, Sphinx will use ``ogp_image`` instead.

``ogp_type``
  This sets the ogp type attribute.
  For more information on the types available, see at https://ogp.me/#types.
  By default, it is set to ``website``, which should be fine for most use cases.

``ogp_custom_meta_tags``
  **Optional.** List of custom HTML snippets to insert.

``ogp_enable_meta_description``
  **Optional.**
  When ``True``, generates ``<meta name="description" content="...">`` from the page.

``ogp_canonical_url``
  **Optional.**
  This option can be used to override the "canonical" URL for the page,
  and is used for ``og:url`` and the URL text in generated social media preview cards.
  It is most useful with versioned documentation, where you intend
  to set the "stable" or "latest" version as the canonical location of each page,
  similarly to ``rel="canonical"``.
  If not set, the option defaults to the value of ``ogp_site_url``. 

Example Config
==============

Simple Config
-------------

.. code-block:: python

   ogp_site_url = "http://example.org/"
   ogp_image = "http://example.org/image.png"

Advanced Config
---------------

.. code-block:: python

   ogp_site_url = "http://example.org/"
   ogp_image = "http://example.org/image.png"
   ogp_description_length = 300
   ogp_type = "article"

   ogp_custom_meta_tags = [
       '<meta property="og:ignore_canonical" content="true" />',
   ]

   ogp_enable_meta_description = True

Per Page Overrides
==================

`Field lists`_ can be used to override certain settings on each page
and set unsupported arbitrary Open Graph tags.

Make sure you place the fields at the very start of the document
such that Sphinx will pick them up and also won't build them into the HTML.


Overrides
---------

These are some overrides that can be used on individual pages,
you can actually override any tag and field lists will always take priority.

``:ogp_description_length:``
  Configure the amount of characters to grab for the description of the page.
  If the value isn't a number it will fall back to ``ogp_description_length``.

``:ogp_disable:``
  Disables generation of Open Graph tags on the page.

``:og:description:``
  Lets you override the description of the page.

``:description:`` or ``.. meta:: :description:``
  Sets the ``<meta name="description" content="...">`` description.

``:og:title:``
  Lets you override the title of the page.

``:og:type:``
  Override the type of the page.
  For the list of available types, see at https://ogp.me/#types.

``:og:image:``
  Set the image for the page.
  
  **Note: Relative file paths for images, videos and audio
  are currently not supported when using field lists. 
  Please use an absolute path instead.**

``:og:image:alt:``
  Sets the alt text. Will be ignored if there is no image set.

Example
-------

Remember that the fields **must** be placed at the very start of the file.
You can verify Sphinx has picked up the fields if they aren't shown
in the final HTML file.

.. code-block:: rst

   :og:description: New description
   :og:image: http://example.org/image.png
   :og:image:alt: Example Image

   Page contents
   =============

Arbitrary Tags
--------------

Additionally, you can use field lists to add any arbitrary Open Graph tag
not supported by the extension. 
The syntax for arbitrary tags is the same with ``:og:tag: content``.

For example:

.. code-block:: rst

   :og:video: http://example.org/video.mp4

   Page contents
   =============

**Note: Relative file paths for images, videos and audio
are currently not supported when using field lists. 
Please use an absolute path instead.**

.. _Open Graph metadata: https://ogp.me/
.. _Field lists: https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html
