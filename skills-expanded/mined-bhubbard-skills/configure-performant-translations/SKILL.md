---
name: configure-performant-translations
description: Hook into performant_translations filters and handle custom MO file paths.
---

# Configure Performant Translations

The Performant Translations plugin offers developers several filters to modify how it handles `.mo` to `.php` conversion.

## Important Filters

### `performant_translations_load_translation_file`
Allows modifying or short-circuiting the process of loading a specific translation file.

```php
add_filter( 'performant_translations_load_translation_file', function( $load, $domain, $mofile ) {
    // Return false to prevent conversion/loading for a specific text domain
    if ( 'my-plugin-domain' === $domain ) {
        return false;
    }
    return $load;
}, 10, 3 );
```

## Integration Details
- The plugin outputs `.mo.php` files to avoid conflicts with standard `.php` files.
- The conversion logic attempts to use the WP Filesystem API when available.
- For most commercial and custom plugins, the conversion happens automatically during the standard `load_plugin_textdomain()` or `load_textdomain()` calls.
