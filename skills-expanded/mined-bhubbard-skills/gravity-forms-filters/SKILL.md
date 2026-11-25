---
name: gravity-forms-filters
description: "Comprehensive guide on gform_pre_render, validation filters, and modifying HTML."
---

# Gravity Forms Filters

Filters allow you to intercept and modify data (such as the form structure, validation results, or HTML output) before Gravity Forms uses it.

## Reference
[Filters Documentation](https://docs.gravityforms.com/category/developers/hooks/filters/)

## Key Filters

### `gform_pre_render`
Fires before the form is rendered. It passes the `$form` object and expects a `$form` object returned.
**Primary Use Case**: Dynamically populating dropdown choices or modifying field properties before display.

```php
add_filter( 'gform_pre_render_5', 'populate_dropdown' );
function populate_dropdown( $form ) {
    foreach ( $form['fields'] as &$field ) {
        if ( $field->id == 3 ) {
            $field->choices = array(
                array( 'text' => 'Option 1', 'value' => '1' ),
                array( 'text' => 'Option 2', 'value' => '2' )
            );
        }
    }
    return $form;
}
```

### `gform_validation`
Allows you to add custom validation logic to the entire form.
**Primary Use Case**: Complex validation that depends on multiple fields.

```php
add_filter( 'gform_validation_5', 'custom_validation' );
function custom_validation( $validation_result ) {
    $form = $validation_result['form'];
    
    // Check something in $_POST
    if ( rgpost( 'input_1' ) == 'Invalid' ) {
        $validation_result['is_valid'] = false;
        foreach ( $form['fields'] as &$field ) {
            if ( $field->id == 1 ) {
                $field->failed_validation = true;
                $field->validation_message = 'This value is not allowed.';
                break;
            }
        }
    }
    
    $validation_result['form'] = $form;
    return $validation_result;
}
```

### `gform_field_validation`
A simpler alternative to `gform_validation` when you only need to validate a single specific field.

## Best Practices
- Always return the modified data variable (like `$form` or `$validation_result`). Failing to return the variable will break the form.
- Use `add_filter()` targeting the specific form ID whenever possible (e.g., `gform_pre_render_5`).
