---
name: yoast-local-seo-metadata
description: "Interacting with the specialized meta keys storing address and location data."
---

# Yoast Local SEO Metadata

Yoast Local SEO stores location data as standard WordPress post meta. If you have "Multiple Locations" enabled, the plugin creates a Custom Post Type (usually `wpseo_locations`) where each post represents a location.

## Metadata Keys

The plugin stores the address and coordinates using specific meta keys prefixed with `_wpseo_`.

Common keys include:
- `_wpseo_business_address`
- `_wpseo_business_city`
- `_wpseo_business_state`
- `_wpseo_business_zipcode`
- `_wpseo_business_country`
- `_wpseo_business_phone`
- `_wpseo_coordinates_lat`
- `_wpseo_coordinates_long`

## Programmatic Interaction

### Reading Location Data
If you need to retrieve a location's city programmatically in your theme:
```php
$city = get_post_meta( $location_post_id, '_wpseo_business_city', true );
```

### Updating Location Data
If you are writing a script to sync locations from an external API, you update the meta keys directly.
```php
update_post_meta( $location_post_id, '_wpseo_coordinates_lat', '40.7128' );
update_post_meta( $location_post_id, '_wpseo_coordinates_long', '-74.0060' );
```
*Note: If you update address fields programmatically, the plugin might not automatically trigger the geocoding process to fetch lat/long. You may need to manually calculate the coordinates or trigger the plugin's geocoding function.*

## Best Practices
- Rely on the built-in functions (`yoast_get_local_seo_address()`) or Shortcodes/Blocks to output the data whenever possible, as they handle formatting and schema markup automatically.
- Only interact with the raw meta keys if you are performing bulk imports, sync scripts, or building highly custom headless API responses.
