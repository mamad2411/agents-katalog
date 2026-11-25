---
name: yoast-seo-social-tags
description: "Customizing OpenGraph (Facebook) and X (Twitter) meta tags."
---

# Yoast SEO Social Tags

Yoast SEO automatically generates OpenGraph tags (`og:title`, `og:image`, etc.) and X (formerly Twitter) card tags based on the post's content or the user's manual overrides in the Yoast meta box.

## Reference
- [OpenGraph Tags Documentation](https://developer.yoast.com/features/opengraph/)
- [X Tags Documentation](https://developer.yoast.com/features/twitter/functional-specification/)

## Key Filters for OpenGraph

### `wpseo_opengraph_title`
Modify the `og:title`.
```php
add_filter( 'wpseo_opengraph_title', 'modify_og_title' );
function modify_og_title( $title ) {
    return 'Awesome: ' . $title;
}
```

### `wpseo_opengraph_desc`
Modify the `og:description`.

### `wpseo_opengraph_image`
Modify the `og:image`. This is very common when you want to enforce a programmatic fallback image based on a custom taxonomy or author if no featured image exists.
```php
add_filter( 'wpseo_opengraph_image', 'modify_og_image' );
function modify_og_image( $image_url ) {
    if ( empty( $image_url ) && is_singular( 'product' ) ) {
        return 'https://example.com/default-product.jpg';
    }
    return $image_url;
}
```

## Key Filters for X (Twitter)

### `wpseo_twitter_title`
Modify the `twitter:title`.

### `wpseo_twitter_description`
Modify the `twitter:description`.

### `wpseo_twitter_image`
Modify the `twitter:image`.

## Best Practices
- If you modify the `wpseo_title` or `wpseo_metadesc` using filters, the OpenGraph and X tags **do not** automatically inherit those filtered values. If you want social tags to match your custom SEO title, you must also apply the filter to `wpseo_opengraph_title` and `wpseo_twitter_title`.
- You can disable OpenGraph entirely using `add_filter( 'wpseo_opengraph', '__return_false' );`.
