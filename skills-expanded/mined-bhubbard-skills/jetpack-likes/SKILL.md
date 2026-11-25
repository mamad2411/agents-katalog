---
name: jetpack-likes
description: Customizing Jetpack Post and Comment Likes. Use when modifying the placement or styling of the WordPress.com Like button.
---

# Jetpack Likes

Jetpack Likes allows logged-in WordPress.com users to "Like" posts and comments on self-hosted sites.

## Moving the Likes Button
By default, the Like button appears at the bottom of the post content. To move it, you must remove the filter from `the_content` and place the shortcode or function where desired.

```php
function remove_jetpack_likes() {
    remove_filter( 'the_content', array( 'Jetpack_Likes', 'post_likes' ), 30, 1 );
}
add_action( 'init', 'remove_jetpack_likes' );
```

Then in a template:
```php
if ( class_exists( 'Jetpack_Likes' ) ) {
    $custom_likes = new Jetpack_Likes;
    echo $custom_likes->post_likes( '' );
}
```

## Likes iFrame
The Likes button is loaded via an iframe from WordPress.com to handle authentication. This means you cannot heavily customize the CSS of the button itself, only the container around it.
