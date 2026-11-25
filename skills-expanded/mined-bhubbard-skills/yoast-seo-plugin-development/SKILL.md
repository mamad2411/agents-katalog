---
name: yoast-seo-plugin-development
description: "General best practices for building plugins that extend Yoast SEO."
---

# Yoast SEO Plugin Development

If you are building a WordPress plugin that relies on or extends Yoast SEO, you need to ensure proper integration architecture.

## Reference
[Plugin Development Documentation](https://developer.yoast.com/development/)

## Best Practices

### Checking if Yoast SEO is Active
Before executing any code that calls Yoast functions or filters, always verify the plugin is active to prevent fatal errors.
```php
if ( defined( 'WPSEO_VERSION' ) ) {
    // Yoast SEO is active
}
```

### Loading Order
If your plugin defines custom Schema pieces or modifies Yoast settings during initialization, ensure your hooks fire at the right time. Yoast typically initializes on `plugins_loaded` or `init`.
```php
add_action( 'plugins_loaded', 'my_custom_yoast_integration', 20 );
function my_custom_yoast_integration() {
    if ( defined( 'WPSEO_VERSION' ) ) {
        // Safe to hook into Yoast
        add_filter( 'wpseo_schema_graph_pieces', 'my_custom_schema' );
    }
}
```

### Extending the Schema
As detailed in the `yoast-seo-schema-api` skill, if your plugin creates a Custom Post Type (e.g., 'Recipe'), you should write a custom Schema piece class that implements `Abstract_Schema_Piece` and ties your `Recipe` JSON-LD into Yoast's main `@graph`.

### Presenting Plugin Settings
If your plugin has settings related to SEO (e.g., "Default Recipe Image"), consider whether it's better to place them in your own settings panel, or hook into the Yoast SEO settings pages using standard WordPress Settings API hooks targeting the `wpseo_` pages.
