---
name: yoast-seo-schema-api
description: "Adding, removing, or modifying pieces in Yoast's Schema.org graph."
---

# Yoast SEO Schema API

Yoast SEO outputs a single, cohesive, interconnected Schema.org graph (using `@graph`) rather than isolated schema blocks. The Schema API allows you to hook into this graph to add, remove, or modify Schema pieces.

## Reference
[Schema API Documentation](https://developer.yoast.com/features/schema/api/)

## Core Filters

### `wpseo_schema_graph_pieces`
Allows you to add new custom pieces (classes) to the Schema graph or remove existing ones.

```php
add_filter( 'wpseo_schema_graph_pieces', 'add_custom_schema_piece', 11, 2 );

function add_custom_schema_piece( $pieces, $context ) {
    // $context contains information about the current page
    if ( $context->indexable->object_type === 'post' && $context->indexable->object_sub_type === 'product' ) {
        // You must include your custom class file
        require_once 'class-my-custom-schema-piece.php';
        $pieces[] = new My_Custom_Schema_Piece( $context );
    }
    return $pieces;
}
```

### Custom Schema Piece Class
When adding a new piece to the array in `wpseo_schema_graph_pieces`, it must be an object implementing `Yoast\WP\SEO\Generators\Schema\Abstract_Schema_Piece`.

```php
class My_Custom_Schema_Piece extends \Yoast\WP\SEO\Generators\Schema\Abstract_Schema_Piece {
    public function is_needed() {
        return true;
    }

    public function generate() {
        return array(
            '@type' => 'Product',
            '@id'   => $this->context->site_url . '#product',
            'name'  => 'My Awesome Product'
        );
    }
}
```

### Modifying Existing Output
If you just want to tweak the array output of an existing Schema piece (like the WebPage or Article piece), use the piece-specific filters: `wpseo_schema_{class_name}`.

```php
add_filter( 'wpseo_schema_article', 'modify_schema_article' );
function modify_schema_article( $data ) {
    $data['headline'] = 'Modified Headline for Schema';
    return $data;
}
```
Available filters include: `wpseo_schema_webpage`, `wpseo_schema_article`, `wpseo_schema_organization`, `wpseo_schema_person`, etc.

## Best Practices
- Always tie your custom Schema pieces into the main graph using the `@id` reference. For example, if adding a "Product" piece to a page, link it to the main WebPage piece using `mainEntityOfPage` or similar properties referencing the WebPage `@id`.
