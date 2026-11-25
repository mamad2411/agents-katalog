---
name: gravity-forms-form-object
description: "Detailed structure of the Form Object and how to manipulate its properties."
---

# Gravity Forms Form Object

The Form Object is an associative array that contains all the properties and settings of a particular form, including its title, fields, notifications, and confirmations.

## Reference
[Form Object Documentation](https://docs.gravityforms.com/form-object/)

## Structure
The Form Object contains both scalar values (like the title) and sub-objects (like fields).

```php
$form = array(
    'id'                   => 5,
    'title'                => 'Contact Us',
    'description'          => 'Please fill out this form.',
    'labelPlacement'       => 'top_label',
    'descriptionPlacement' => 'below',
    'button'               => array( // Button Object
        'type' => 'text',
        'text' => 'Submit'
    ),
    'fields'               => array(), // Array of Field Objects
    'notifications'        => array(), // Array of Notification Objects
    'confirmations'        => array(), // Array of Confirmation Objects
    // ...
);
```

## Common Usage

### Modifying the Form Object
The `$form` object is heavily modified via the `gform_pre_render` filter.

```php
add_filter( 'gform_pre_render_5', 'modify_form_title' );
function modify_form_title( $form ) {
    $form['title'] = 'Dynamically Changed Title';
    return $form;
}
```

### Iterating Over Fields
A very common task is to loop through the `$form['fields']` array to find or modify a specific field.

```php
foreach ( $form['fields'] as &$field ) {
    if ( $field->id == 2 ) { // Found the field
        $field->cssClass = 'my-custom-class';
    }
}
```

## Best Practices
- When modifying the `$form` object in a filter, ensure you return the `$form` object at the end of your function.
- Remember that `$form['fields']` is an array of objects (`GF_Field` instances), not associative arrays.
