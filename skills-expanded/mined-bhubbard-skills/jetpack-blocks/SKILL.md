---
name: jetpack-blocks
description: Guidance for extending or interacting with Jetpack's custom Gutenberg blocks. Use when a user wants to customize Tiled Galleries, Forms, or other Jetpack blocks.
---

# Jetpack Blocks Development

When assisting users with Jetpack Blocks, adhere to the following principles:

## Block Styles and Variations
Jetpack provides several blocks like Tiled Gallery, Form, Subscribe, and Map. You can register custom styles for these blocks using standard WordPress block APIs in JavaScript or PHP.

### Example: Adding a style to Jetpack Form
```javascript
wp.blocks.registerBlockStyle( 'jetpack/contact-form', {
    name: 'custom-outline',
    label: 'Custom Outline'
} );
```

## Filtering Block Output
You can filter the frontend output of specific Jetpack blocks using PHP filters. 
For example, to filter the Form block's HTML:
```php
add_filter( 'jetpack_contact_form_html', function( $html ) {
    // Modify $html
    return $html;
} );
```

## Disabling Specific Blocks
If the user wants to remove certain Jetpack blocks from the inserter, you can use the `jetpack_set_available_blocks` filter.

```php
add_filter( 'jetpack_set_available_blocks', 'my_custom_jetpack_blocks' );
function my_custom_jetpack_blocks( $blocks ) {
    // Remove the map block
    $blocks = array_diff( $blocks, array( 'jetpack/map' ) );
    return $blocks;
}
```
