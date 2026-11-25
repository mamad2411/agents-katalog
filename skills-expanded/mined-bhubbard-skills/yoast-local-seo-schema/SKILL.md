---
name: yoast-local-seo-schema
description: "Modifying the injected LocalBusiness schema and tying it into the main Yoast graph."
---

# Yoast Local SEO Schema

The Yoast Local SEO plugin automatically adds `LocalBusiness` (or more specific subtypes like `Restaurant`, `Dentist`) to the Schema graph, ensuring search engines understand your physical locations.

## Reference
[Yoast Local SEO Documentation](https://developer.yoast.com/features/schema/plugins/#yoast-local-seo)

## Core Schema Injection

By default, Yoast Local SEO hooks into the `wpseo_schema_graph_pieces` filter to inject its `LocalBusiness` schema piece. It ties this piece to the main `Organization` and the `WebPage`.

### Modifying the LocalBusiness Output
To modify the attributes of the `LocalBusiness` schema piece, you can use the piece-specific filter:
```php
add_filter( 'wpseo_schema_localbusiness', 'modify_yoast_local_business_schema' );
function modify_yoast_local_business_schema( $data ) {
    // Add custom properties like a specific price range
    $data['priceRange'] = '$$';
    return $data;
}
```

### Disabling LocalBusiness Schema on Specific Pages
If you have multiple locations and the plugin is outputting all locations on the homepage, but you only want the main location:
```php
add_filter( 'wpseo_local_business_schema', '__return_false' );
```
*(Note: Be careful with disabling local business schema globally unless you are generating it manually).*

## Best Practices
- When defining multiple locations, ensure that the individual location pages (the Custom Post Type usually created by the plugin) represent the specific `LocalBusiness` entity for that location. Yoast handles this mapping automatically.
- Do not output your own `LocalBusiness` JSON-LD string if this plugin is active, as it will create duplicated, conflicting schema entities. Use the filter to append your custom fields to Yoast's output.
