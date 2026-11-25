---
name: yoast-seo-blocks
description: "Working with Yoast's structured data blocks (like Breadcrumbs, FAQ, How-to)."
---

# Yoast SEO Blocks

Yoast SEO provides several custom blocks for the WordPress Gutenberg editor that automatically output both formatted HTML and perfectly structured Schema.org JSON-LD.

## Reference
[Blocks Documentation](https://developer.yoast.com/features/blocks/breadcrumbs/)

## Available Blocks
- **Breadcrumbs Block**: Outputs the breadcrumb trail.
- **FAQ Block**: Outputs an accordion/list of questions and answers, and injects `FAQPage` schema.
- **How-to Block**: Outputs a step-by-step guide and injects `HowTo` schema.
- **Estimated Reading Time**: Outputs the calculated reading time.

## Breadcrumbs Customization
The Breadcrumbs block (and the classic `yoast_breadcrumb()` PHP function) can be heavily customized via filters.

### `wpseo_breadcrumb_links`
Modify the array of breadcrumb links before they are rendered.
```php
add_filter( 'wpseo_breadcrumb_links', 'modify_breadcrumb_trail' );
function modify_breadcrumb_trail( $links ) {
    // Insert a custom link after the Home link (index 0)
    if ( is_singular( 'product' ) ) {
        $custom_link = array(
            'url' => '/store/',
            'text' => 'Store',
        );
        array_splice( $links, 1, 0, array( $custom_link ) );
    }
    return $links;
}
```

### `wpseo_breadcrumb_separator`
Change the separator between items.
```php
add_filter( 'wpseo_breadcrumb_separator', 'custom_breadcrumb_separator' );
function custom_breadcrumb_separator( $separator ) {
    return ' &raquo; ';
}
```

## Best Practices
- When a user requests an FAQ section on a site, always recommend using the Yoast FAQ block instead of a generic accordion plugin, as the Yoast block automatically handles the complex `FAQPage` schema validation required by Google for rich snippets.
- If you use the Yoast breadcrumbs PHP function in a theme (`yoast_breadcrumb('<p id="breadcrumbs">','</p>');`), ensure you check if the function exists first: `if ( function_exists('yoast_breadcrumb') )`.
