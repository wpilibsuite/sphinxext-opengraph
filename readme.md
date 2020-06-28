# wpilib-ogpgit
Sphinx extension to add support for ogp (https://ogp.me/)

## Options
These values are placed in the conf.py of your sphinx project.

### Site URL
- *Formal Name:* `ogp_site_url`
- *Default Value:* None

This config option is very important, set it to the URL the site is being hosted on.

### Description Length
- *Formal Name:* `ogp_description_length`
- *Default Value:* `200`

Configure the amount of characters taken from a page. The default of 200 is probably good for most people. If something other than a number is used, it defaults back to 200.

### Image
- *Formal Name:* `ogp_image`
- *Default Value:* None

This is not required. Link to image to show.

### Type
- *Formal Name:* `ogp_type`
- *Default Value:* `website`

This sets the ogp type attribute, for more information on the types available please take a look at https://ogp.me/#types.