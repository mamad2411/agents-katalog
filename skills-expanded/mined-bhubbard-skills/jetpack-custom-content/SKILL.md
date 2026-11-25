---
name: jetpack-custom-content
description: Customizing Jetpack Custom Content Types (Portfolios, Testimonials). Use when modifying custom post type slugs or adding theme support for CPTs.
---

# Jetpack Custom Content Types

Jetpack can register standard Custom Post Types (CPTs) for Portfolios and Testimonials.

## Adding Theme Support
To use these features, the site owner must enable them in Settings > Writing, or the theme can declare support:
```php
add_action( 'after_setup_theme', function() {
    add_theme_support( 'jetpack-portfolio' );
    add_theme_support( 'jetpack-testimonial' );
} );
```

## Changing the CPT Slug
If a user wants their Portfolio URL to be `/projects/` instead of `/portfolio/`:
```php
add_filter( 'jetpack_portfolio_rewrite_params', function( $params ) {
    $params['slug'] = 'projects';
    return $params;
} );
```
*Note: The user must flush permalinks (visit Settings > Permalinks) after changing the slug.*

## Displaying Portfolios
Portfolios use `archive-portfolio.php` and `single-portfolio.php` theme templates if they exist. Otherwise, they fall back to `archive.php` and `single.php`.
