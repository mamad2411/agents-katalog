---
name: yoast-woocommerce-seo-filters
description: "Modifying product gallery image outputs, pricing metadata, and SKU/GTIN injection."
---

# Yoast WooCommerce SEO Filters

Beyond schema, the Yoast WooCommerce SEO plugin handles how products look when shared on social media by injecting WooCommerce data into OpenGraph and X (Twitter) tags.

## OpenGraph Enhancements
The plugin automatically pulls product prices, currency, and gallery images to enrich the Facebook OpenGraph tags.

### Product Gallery Images
By default, it outputs all WooCommerce product gallery images as `og:image` tags so users can select an image when sharing. If a product has 50 images, this bloats the `<head>`.

```php
add_filter( 'wpseo_woocommerce_og_image', 'limit_woocommerce_og_images' );
function limit_woocommerce_og_images( $images ) {
    // Only return the first 3 images from the gallery
    return array_slice( $images, 0, 3 );
}
```

### Product Identifiers (GTIN, ISBN, MPN)
The plugin adds fields to the WooCommerce inventory tab for global identifiers (GTIN, ISBN, etc.). If you already use a custom field or another plugin for these identifiers, you can map them so Yoast uses your data.

```php
add_filter( 'wpseo_woocommerce_global_identifier_values', 'map_custom_gtin_to_yoast', 10, 2 );
function map_custom_gtin_to_yoast( $identifier_values, $product ) {
    // Retrieve your custom GTIN
    $custom_gtin = get_post_meta( $product->get_id(), '_my_custom_gtin', true );
    
    if ( ! empty( $custom_gtin ) ) {
        $identifier_values['gtin'] = $custom_gtin;
    }
    
    return $identifier_values;
}
```

## Best Practices
- Always ensure global identifiers (GTIN/UPC) are populated correctly. They are strictly required by Google Merchant Center and heavily weighted in organic shopping results. Yoast's integration makes injecting these into the schema very easy.
