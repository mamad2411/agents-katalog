---
name: yoast-woocommerce-seo-schema
description: "Understanding how Yoast replaces WooCommerce schema."
---

# Yoast WooCommerce SEO Schema

The Yoast WooCommerce SEO plugin provides a crucial bridge between WooCommerce and Yoast SEO. Without it, WooCommerce outputs its own isolated JSON-LD blocks, which conflict with Yoast's graph. This plugin disables WooCommerce's default schema and integrates it seamlessly into the Yoast `@graph`.

## Reference
[WooCommerce SEO Schema](https://developer.yoast.com/features/schema/plugins/#yoast-woocommerce-seo)

## Schema Modifications

1. **WebPage to ItemPage**: The plugin changes the main `WebPage` piece to `ItemPage` on single products.
2. **Product Piece**: It generates a robust `Product` schema piece, linking it to the `ItemPage`.
3. **Offers / AggregateRating**: It correctly nests pricing and review data inside the `Product` piece.

### Modifying the Product Schema
You can hook into the product output using the specific piece filter.

```php
add_filter( 'wpseo_schema_product', 'modify_woocommerce_product_schema' );
function modify_woocommerce_product_schema( $data ) {
    global $product;
    
    // Add a custom brand property if you have a custom taxonomy
    $brand = get_term_by( 'id', $product->get_meta( '_custom_brand_id' ), 'product_brand' );
    if ( $brand ) {
        $data['brand'] = array(
            '@type' => 'Brand',
            'name'  => $brand->name
        );
    }
    
    return $data;
}
```

## Best Practices
- If you install this plugin, you do not need to manually disable WooCommerce's default schema output (`add_filter('woocommerce_structured_data_product', '__return_empty_array')`); the Yoast plugin handles that automatically to prevent duplication.
