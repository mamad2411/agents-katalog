---
name: jetpack-widgets
description: Utilizing and customizing Jetpack's Extra Sidebar Widgets. Use when working with the Top Posts, Social Icons, or Authors widgets.
---

# Jetpack Extra Sidebar Widgets

Jetpack adds several legacy widgets and blocks.

## Top Posts & Pages Widget
This widget displays the most popular posts based on Jetpack Stats.
- You can filter the query used to fetch these posts via `jetpack_widget_top_posts_args`.

```php
add_filter( 'jetpack_widget_top_posts_args', function( $args ) {
    $args['post_type'] = array( 'post', 'page' ); // Include pages
    return $args;
} );
```

## Social Icons Widget
You can add custom social icons to the widget by filtering the supported icons array:
```php
add_filter( 'jetpack_social_media_icons_widget_array', function( $icons ) {
    $icons['custom-network'] = 'https://custom-network.com/icon.png';
    return $icons;
} );
```

## Widget Visibility
Jetpack's Widget Visibility module allows users to conditionally hide/show widgets. As a developer, if a widget isn't appearing, check the widget settings to ensure no visibility rules are conflicting.
