---
name: jetpack-search
description: Configuring and customizing the Jetpack Search experience. Use when a user wants to customize Elasticsearch algorithms, filter results, or modify the Search UI overlay.
---

# Jetpack Search Customization

Jetpack Search leverages WordPress.com's Elasticsearch infrastructure.

## Modifying the Search Query
You can tweak the underlying Elasticsearch query using the `jetpack_search_es_wp_query_args` filter. This is useful for boosting certain post types or altering sorting.

```php
add_filter( 'jetpack_search_es_wp_query_args', function( $es_args, $query ) {
    // Example: Boost the 'product' post type
    // Modify $es_args to add weighting
    return $es_args;
}, 10, 2 );
```

## Excluding Content
To prevent specific posts or post types from being indexed by Jetpack Search, you exclude them from Jetpack Sync. If they aren't synced, they aren't searchable.

## Customizing the Overlay UI
The Jetpack Search overlay UI is built with React. You can customize its appearance via CSS (targeting `.jetpack-instant-search__overlay`), or by utilizing specific PHP filters that modify the configuration JSON passed to the React app.

```php
add_filter( 'jetpack_search_overlay_color_theme', function() {
    return 'dark'; // 'light' or 'dark'
} );
```
