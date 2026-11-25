---
name: jetpack-media
description: Customizing Jetpack Carousel and Tiled Galleries. Use when a user wants to alter the behavior of galleries, change the carousel background, or handle image sizes.
---

# Jetpack Carousel & Tiled Galleries

Jetpack enhances WordPress galleries with a full-screen Carousel and a masonry-style Tiled Gallery layout.

## Tiled Galleries Content Width
Tiled Galleries depend on the theme's `$content_width` variable to calculate image sizes. If galleries look incorrectly sized, ensure this variable is set:
```php
if ( ! isset( $content_width ) ) {
    $content_width = 800;
}
```

## Customizing the Carousel
You can customize the appearance of the Carousel using the `jetpack_carousel_css` filter to enqueue a custom stylesheet, or by filtering the default parameters.

### Changing the background color
```php
add_filter( 'jetpack_carousel_display_background_color', function() {
    return 'white'; // default is 'black'
} );
```

### Disabling Carousel for a specific gallery
You can disable the carousel on a per-gallery basis by adding `carousel="false"` to the gallery shortcode or block block properties.
