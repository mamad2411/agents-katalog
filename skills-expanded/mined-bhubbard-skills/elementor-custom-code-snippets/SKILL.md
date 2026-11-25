---
name: elementor-custom-code-snippets
description: Developer guidelines for managing and implementing custom code snippets in Elementor.
---

# Elementor Custom Code Snippets Guide

## Overview
This skill provides developer-focused guidelines for managing, implementing, and optimizing custom code snippets within Elementor and Elementor Pro environments. It covers best practices for injecting custom CSS, JavaScript, and PHP without bloating the site or causing conflicts.

## Key Principles

1. **Native over Custom:** Always prioritize Elementor's native features (e.g., Global Custom CSS, widget-level Custom CSS) over injecting external snippets when possible.
2. **Elementor Custom Code Feature:** For site-wide scripts (analytics, meta tags, global JS), utilize the built-in *Elementor > Custom Code* interface instead of editing theme files or using third-party plugins.
3. **Performance First:** Ensure custom JavaScript is deferred or loaded asynchronously unless strictly required in the `<head>`.
4. **Child Themes:** For custom PHP functions, always use a child theme's `functions.php` or a site-specific utility plugin. Never edit the parent theme or Elementor core files.

## Implementing Custom CSS

### Widget Level
Use the Advanced > Custom CSS tab on individual widgets for isolated styling.
*   **Selector Keyword:** Always use the `selector` keyword to target the specific widget wrapper.
    ```css
    selector .elementor-widget-container {
        /* Your styles here */
    }
    ```

### Page Level
Use the Page Settings (gear icon) > Advanced > Custom CSS for styles that apply only to the current page but affect multiple widgets.

### Site-wide Level
Use Site Settings > Custom CSS for global utility classes or site-wide overrides.

## Implementing Custom JavaScript

### Using Elementor Custom Code
1. Navigate to *Elementor > Custom Code*.
2. Add a new snippet.
3. Choose the Location: `<head>`, `<body> - Start`, or `<body> - End`.
4. **Best Practice:** Place non-critical JS in `<body> - End` to prevent render-blocking.
5. Apply conditional display conditions (e.g., Entire Site, Specific Pages).

### Enqueuing Scripts (PHP)
For complex scripts or dependencies, enqueue them properly via `functions.php`:
```php
add_action( 'wp_enqueue_scripts', 'my_custom_elementor_scripts' );
function my_custom_elementor_scripts() {
    wp_enqueue_script( 'my-custom-js', get_stylesheet_directory_uri() . '/js/custom.js', array('jquery'), '1.0.0', true );
}
```

## Creating Custom Elementor Hooks (PHP)

Elementor provides numerous hooks for developers. Common use cases:

*   **Before/After Rendering a Widget:**
    ```php
    add_action( 'elementor/widget/before_render_content', function( $widget ) {
        if ( 'heading' === $widget->get_name() ) {
            // Do something
        }
    } );
    ```

## Troubleshooting
*   **Safe Mode:** If custom code breaks the editor, enable Elementor Safe Mode to isolate the issue.
*   **Console Errors:** Always check the browser developer console for JS conflicts originating from custom snippets.
