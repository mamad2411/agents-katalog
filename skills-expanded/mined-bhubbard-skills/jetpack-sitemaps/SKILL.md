---
name: jetpack-sitemaps
description: Customizing Jetpack XML Sitemaps. Use when a user needs to exclude specific post types, change sitemap caching, or add custom URLs.
---

# Jetpack XML Sitemaps

Jetpack can automatically generate XML Sitemaps for search engines.

## Excluding a Post Type
To prevent a specific post type from appearing in the sitemap:
```php
add_filter( 'jetpack_sitemap_post_types', function( $post_types ) {
    $index = array_search( 'my_private_cpt', $post_types );
    if ( $index !== false ) {
        unset( $post_types[$index] );
    }
    return $post_types;
} );
```

## Excluding a Taxonomy
To remove a specific taxonomy (like a custom category) from the sitemap:
```php
add_filter( 'jetpack_sitemap_taxonomies', function( $taxonomies ) {
    $index = array_search( 'my_hidden_tax', $taxonomies );
    if ( $index !== false ) {
        unset( $taxonomies[$index] );
    }
    return $taxonomies;
} );
```

## News Sitemaps
Jetpack also creates a specific `news-sitemap.xml` for Google News, which only contains posts from the last 48 hours.
