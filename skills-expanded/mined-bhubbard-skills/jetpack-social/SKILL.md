---
name: jetpack-social
description: Guidance for customizing Jetpack Social (formerly Publicize). Use when customizing social media sharing formats, adding custom post types, or modifying social buttons.
---

# Jetpack Social Customization

Jetpack Social automatically shares published posts to social media networks.

## Enabling for Custom Post Types
By default, Jetpack Social only works for Posts and Pages. To enable it for a custom post type, add `publicize` to the `supports` array when registering the CPT, or use `add_post_type_support()`.

```php
add_action( 'init', function() {
    add_post_type_support( 'my_custom_post_type', 'publicize' );
} );
```

## Customizing the Shared Message
You can filter the message that is sent to social networks.
```php
add_filter( 'publicize_save_meta', 'custom_publicize_message', 10, 4 );
function custom_publicize_message( $submit_post, $post_id, $service_name, $connection ) {
    // Modify $submit_post to alter the text
    return $submit_post;
}
```

## Social Sharing Buttons
To programmatically adjust where the Jetpack Sharing buttons appear, you can remove the default filters and place the `sharing_display()` function directly in your theme templates.
