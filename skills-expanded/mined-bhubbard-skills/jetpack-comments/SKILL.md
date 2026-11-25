---
name: jetpack-comments
description: Customizing the Jetpack Comments module. Use when altering the comment form UI, allowing social logins for comments, or changing comment color schemes.
---

# Jetpack Comments Customization

Jetpack Comments replaces the default WordPress comment form with a system that allows users to log in via WordPress.com, Twitter, Facebook, or Google.

## Changing the Color Scheme
Jetpack Comments comes in a `light` and `dark` color scheme. It usually auto-detects based on the theme, but you can force it:
```php
add_filter( 'jetpack_comments_allow_oembed', '__return_true' );

add_filter( 'jetpack_comments_color_scheme', function() {
    return 'dark'; // 'light' or 'transparent'
} );
```

## Changing the Greeting Text
To change the "Leave a Reply" heading:
```php
add_filter( 'jetpack_comment_form_prompt', function( $prompt ) {
    return 'Share your thoughts!';
} );
```

## Limitations
Because the Jetpack Comment form is loaded via an iframe (to securely handle social authentications), you cannot heavily modify its internal CSS directly from your theme's stylesheet.
