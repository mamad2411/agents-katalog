---
name: gravity-forms-field-object
description: "Deep dive into the properties of individual Field Objects."
---

# Gravity Forms Field Object

The Field Object (`GF_Field`) contains all settings for a particular field. It is a sub-object found within the `$form['fields']` array.

## Reference
[Field Object Documentation](https://docs.gravityforms.com/field-object/)

## Structure
Unlike the Form and Entry objects, the Field Object is an actual PHP Object (an instance of a class extending `GF_Field`), not an associative array.

```php
// Example properties accessible on a $field object
$field->id;               // (int) The field ID
$field->type;             // (string) e.g., 'text', 'select', 'checkbox'
$field->label;            // (string) The field label
$field->isRequired;       // (bool) Whether the field is required
$field->cssClass;         // (string) Custom CSS class
$field->choices;          // (array) Array of choice arrays for select/radio/checkbox
$field->conditionalLogic; // (array) Conditional logic rules
```

## Common Usage

### Modifying Choices
Often used in the `gform_pre_render` hook to dynamically populate drop downs.

```php
foreach ( $form['fields'] as &$field ) {
    if ( $field->type == 'select' && $field->id == 3 ) {
        $field->choices = array(
            array( 'text' => 'First Choice', 'value' => 'First Choice' ),
            array( 'text' => 'Second Choice', 'value' => 'Second Choice' )
        );
    }
}
```

## Best Practices
- Remember to use object syntax (`$field->property`) instead of array syntax (`$field['property']`). Gravity Forms has backwards compatibility built-in (using `ArrayAccess`), but object syntax is preferred and faster.
- Use the `$field->type` property to reliably identify field types rather than relying on the CSS class or other ambiguous properties.
