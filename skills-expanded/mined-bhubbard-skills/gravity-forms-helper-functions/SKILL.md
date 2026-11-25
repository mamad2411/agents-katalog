---
name: gravity-forms-helper-functions
description: "Usage of built-in Gravity Forms PHP helper functions."
---

# Gravity Forms Helper Functions

Gravity Forms provides several helper functions to make common tasks easier when writing custom code or working within a theme.

## Reference
[Helper Functions Documentation](https://docs.gravityforms.com/helper-functions/)

## Commonly Used Functions

### `gravity_form()`
Embeds a Gravity Form programmatically via PHP, often used in theme template files.
```php
// gravity_form( $id_or_title, $display_title, $display_description, $display_inactive, $field_values, $ajax, $tabindex, $echo );
gravity_form( 1, false, false, false, '', true, 1 );
```

### `rgpost()`
Safely retrieves a value from the `$_POST` array. It is a wrapper for `isset( $_POST[$name] ) ? $_POST[$name] : ''` with optional sanitation.
```php
$value = rgpost( 'input_1' );
```

### `rgar()`
Safely retrieves a value from an array.
```php
$array = array( 'key1' => 'value1', 'key2' => 'value2' );
$value = rgar( $array, 'key1' ); // Returns 'value1'
```

### `rgget()`
Safely retrieves a value from the `$_GET` array.
```php
$value = rgget( 'my_query_param' );
```

## Best Practices
- Use `rgar()` and `rgars()` instead of direct array access to avoid "Undefined index" PHP notices.
- Use `rgpost()` and `rgget()` for clean input retrieval.
