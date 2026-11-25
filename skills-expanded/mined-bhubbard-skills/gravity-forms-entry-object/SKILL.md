---
name: gravity-forms-entry-object
description: "Structure of the Entry Object, including accessing specific field values."
---

# Gravity Forms Entry Object

The Entry Object is an associative array that contains all properties of a particular entry, such as the date created, the submitter's IP address, and the actual values submitted for each field.

## Reference
[Entry Object Documentation](https://docs.gravityforms.com/entry-object/)

## Structure

```php
$entry = array(
    'id'           => 123,
    'form_id'      => 5,
    'date_created' => '2023-10-26 14:32:00',
    'is_starred'   => 0,
    'is_read'      => 1,
    'ip'           => '127.0.0.1',
    'source_url'   => 'https://example.com/contact',
    'user_agent'   => 'Mozilla/5.0...',
    'payment_status'=> '',
    
    // Field Values (Keys are field IDs as strings)
    '1'            => 'John Doe',
    '2'            => 'john@example.com',
    '3.1'          => 'Option 1', // Checkbox choice 1
    '3.2'          => 'Option 2', // Checkbox choice 2
);
```

## Common Usage

### Retrieving Field Values
Always use `rgar()` to safely retrieve values from the `$entry` object. The key is always a string representation of the field ID.

```php
add_action( 'gform_after_submission', 'process_entry', 10, 2 );
function process_entry( $entry, $form ) {
    // Standard Field
    $name = rgar( $entry, '1' );
    
    // Multi-input Field (like Checkboxes, Name, Address)
    $first_name = rgar( $entry, '4.3' );
    $last_name  = rgar( $entry, '4.6' );
}
```

### Updating Entry Metadata
Sometimes you want to store internal data along with an entry without creating a visible field.
```php
gform_update_meta( $entry['id'], 'my_custom_key', 'my_custom_value' );
$value = gform_get_meta( $entry['id'], 'my_custom_key' );
```

## Best Practices
- Do not modify the `$entry` array and expect it to automatically save to the database during `gform_after_submission`. If you need to change the saved value of a field, use the `gform_pre_submission` hook to modify `$_POST` instead, or use `GFAPI::update_entry_field( $entry['id'], '1', 'New Value' )`.
