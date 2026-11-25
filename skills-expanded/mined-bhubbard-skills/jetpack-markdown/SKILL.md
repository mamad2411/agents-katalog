---
name: jetpack-markdown
description: Utilizing Jetpack Markdown support. Use when rendering markdown content or applying markdown parsing to custom fields or post types.
---

# Jetpack Markdown

Jetpack allows writing in Markdown format, which is then compiled into HTML.

## Enabling Markdown for Custom Post Types
By default, Jetpack Markdown works on Posts and Pages. To enable it for a Custom Post Type:
```php
add_action( 'init', function() {
    add_post_type_support( 'my_custom_post_type', 'wpcom-markdown' );
} );
```

## Parsing Markdown Manually
If you have raw Markdown text (e.g., from a custom field) and want to parse it into HTML on the frontend, you can use Jetpack's Markdown parser function if the module is active.
```php
if ( class_exists( 'WPCom_Markdown' ) ) {
    $markdown = WPCom_Markdown::get_instance();
    $html = $markdown->transform( $raw_markdown_text );
}
```

## Caveats
Jetpack Markdown converts the Markdown to HTML upon saving the post. Therefore, disabling the module does not revert the posts to raw Markdown.
