---
name: jetpack-infinite-scroll
description: Implementing and customizing Jetpack Infinite Scroll. Use when adding infinite scroll support to a custom theme or changing the scroll behavior (button vs. auto).
---

# Jetpack Infinite Scroll

Infinite Scroll pulls the next set of posts into view automatically when the reader approaches the bottom of the page.

## Adding Theme Support
A theme must declare support for Infinite Scroll.
```php
add_action( 'after_setup_theme', 'my_theme_infinite_scroll_setup' );
function my_theme_infinite_scroll_setup() {
    add_theme_support( 'infinite-scroll', array(
        'container' => 'main',          // ID of the container element
        'render'    => 'my_theme_infinite_scroll_render', // Function to render the posts
        'footer'    => 'page',          // ID of the footer
    ) );
}

function my_theme_infinite_scroll_render() {
    while ( have_posts() ) {
        the_post();
        get_template_part( 'content', get_post_format() );
    }
}
```

## Changing the Trigger
By default, Infinite Scroll loads automatically. You can change this to require a button click:
```php
add_filter( 'infinite_scroll_archive_supported', '__return_false' ); // Force click-to-load on archives
```
Or define it in `add_theme_support`: `'type' => 'click'`.
