---
name: yoast-local-seo-widgets
description: "Working with the store locator, opening hours, and Google Maps widgets."
---

# Yoast Local SEO Widgets

Yoast Local SEO provides blocks, shortcodes, and PHP functions to display Google Maps, Opening Hours, and Store Locators.

## Output Methods

### 1. WordPress Blocks
The recommended way to output these elements in modern WordPress is using the dedicated Yoast Local SEO Gutenberg blocks. These blocks have built-in UI settings for zooming, map style, and data display.

### 2. Shortcodes
For classic editor or specific page builder setups:
- `[wpseo_address]` - Outputs address details.
- `[wpseo_map]` - Outputs a Google Map.
- `[wpseo_opening_hours]` - Outputs formatted opening hours.
- `[wpseo_storelocator]` - Outputs an interactive store locator.

### 3. PHP Functions
If you are building a custom theme template, you can call the underlying functions directly:
```php
if ( function_exists( 'yoast_get_local_seo_map' ) ) {
    // Attributes match the shortcode attributes
    $atts = array(
        'id' => 42, // Post ID of the location
        'width' => '100%',
        'height' => '400',
        'zoom' => -1,
        'show_route' => true
    );
    echo yoast_get_local_seo_map( $atts );
}
```

## Customizing the Output

### Filtering the Maps API Key
```php
add_filter( 'wpseo_local_maps_api_key', 'my_custom_maps_key' );
function my_custom_maps_key( $key ) {
    return 'YOUR_API_KEY_HERE';
}
```

## Best Practices
- Always check `function_exists()` before calling the specific PHP functions in your theme to prevent fatal errors if the plugin is deactivated.
- Ensure the Google Maps API key is configured correctly in the Yoast Local SEO settings and has the correct HTTP referrers set in the Google Cloud Console.
