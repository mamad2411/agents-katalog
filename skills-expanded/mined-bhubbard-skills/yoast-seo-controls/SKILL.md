---
name: yoast-seo-controls
description: "Extending or modifying the Yoast SEO meta box and sidebar controls."
---

# Yoast SEO Controls

Yoast SEO provides UI controls in the WordPress backend (the Meta Box beneath the post editor and the Gutenberg Sidebar) where users can enter custom titles, descriptions, and social images.

## Reference
[Controls Documentation](https://developer.yoast.com/features/controls/overview/)

## Modifying the UI

### Moving the Meta Box
By default, the Yoast meta box sits at the bottom of the classic editor (priority 'high'). Some users prefer it lower.
```php
add_filter( 'wpseo_metabox_prio', 'move_yoast_metabox_down' );
function move_yoast_metabox_down() {
    return 'low';
}
```

### Disabling the Meta Box for Specific Roles
You might want to hide the SEO controls from Authors or Contributors.
```php
function hide_yoast_from_authors() {
    if ( ! current_user_can( 'manage_options' ) ) {
        remove_meta_box( 'wpseo_meta', 'post', 'normal' );
        remove_meta_box( 'wpseo_meta', 'page', 'normal' );
    }
}
add_action( 'add_meta_boxes', 'hide_yoast_from_authors', 99 );
```

## Modifying Saved Values
When a user types into the Yoast meta box, the values are saved as post meta (e.g., `_yoast_wpseo_title`).

### Setting Defaults Programmatically
If you want to set a default fallback title format, it is usually better to configure this in the Yoast SEO Settings UI (Search Appearance). However, to do it programmatically:
```php
add_filter( 'wpseo_title', 'my_custom_default_title' );
function my_custom_default_title( $title ) {
    $custom_title = get_post_meta( get_the_ID(), '_yoast_wpseo_title', true );
    if ( empty( $custom_title ) ) {
        return 'My Hardcoded Fallback Title';
    }
    return $title;
}
```

## Best Practices
- The Yoast Gutenberg Sidebar is built in React. Modifying its fields requires advanced JavaScript knowledge and hooking into the `@yoast/app-components` registry. PHP `remove_meta_box` calls generally only affect the Classic Editor meta box, though Yoast does respect capability checks (like `wpseo_manage_options`) to hide the sidebar.
