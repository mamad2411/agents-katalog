---
name: gravity-forms-conditional-logic-object
description: "Understanding and dynamically applying conditional logic rules."
---

# Gravity Forms Conditional Logic Object

Conditional logic controls the visibility of fields, buttons, notifications, and confirmations based on the choices selected or values entered by the user. 

## Reference
[Conditional Logic Object Documentation](https://docs.gravityforms.com/conditional-logic-object/)

## Structure
The Conditional Logic object is an associative array defining the rules. It usually resides as the `conditionalLogic` property of a Field Object, or inside a notification/confirmation array.

```php
$conditionalLogic = array(
    'actionType' => 'show', // show or hide
    'logicType'  => 'all',  // all or any
    'rules'      => array(
        array(
            'fieldId'  => '3',      // The field ID to check
            'operator' => 'is',     // is, isnot, >, <, contains, starts_with, ends_with
            'value'    => 'Yes'     // The value to match against
        )
    )
);
```

## Common Usage

### Dynamically Adding Conditional Logic
You can programmatically add or modify conditional logic to a field before the form is rendered.

```php
add_filter( 'gform_pre_render_5', 'add_conditional_logic' );
function add_conditional_logic( $form ) {
    foreach ( $form['fields'] as &$field ) {
        if ( $field->id == 5 ) {
            // Make Field 5 only show if Field 2 equals "Business"
            $field->conditionalLogic = array(
                'actionType' => 'show',
                'logicType'  => 'all',
                'rules'      => array(
                    array(
                        'fieldId'  => '2',
                        'operator' => 'is',
                        'value'    => 'Business'
                    )
                )
            );
        }
    }
    return $form;
}
```

## Best Practices
- When defining rules for multi-input fields (like checkboxes or address fields), use the specific input ID as a string (e.g., `'fieldId' => '4.1'`) rather than just the base field ID.
