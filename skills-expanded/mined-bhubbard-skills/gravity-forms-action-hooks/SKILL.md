---
name: gravity-forms-action-hooks
description: "Comprehensive guide on core actions like gform_after_submission."
---

# Gravity Forms Action Hooks

Action hooks allow you to execute custom code at specific points during the Gravity Forms lifecycle, such as after an entry is saved.

## Reference
[Action Hooks Documentation](https://docs.gravityforms.com/category/developers/hooks/actions/)

## Key Action Hooks

### `gform_after_submission`
Fires after a form has been successfully submitted and the entry has been created in the database.
**Primary Use Case**: Sending entry data to a third-party API or triggering a custom email.

```php
// Target a specific form ID (e.g., Form 5)
add_action( 'gform_after_submission_5', 'my_custom_api_call', 10, 2 );
function my_custom_api_call( $entry, $form ) {
    $first_name = rgar( $entry, '1.3' );
    // Send data somewhere
}
```

### `gform_pre_submission`
Fires just before the entry is saved to the database.
**Primary Use Case**: Manipulating the `$_POST` data. Because the entry hasn't been created yet, you modify `$_POST` instead of the `$entry` object.

```php
add_action( 'gform_pre_submission_5', 'modify_post_data' );
function modify_post_data( $form ) {
    $_POST['input_1'] = 'Modified Value';
}
```

### `gform_post_payment_action`
Fires after a payment has been processed and the entry status is updated.
**Primary Use Case**: Fulfilling an order (like creating a user account) only after the payment is marked 'Paid'.

## Best Practices
- Append the form ID to the hook name (e.g., `gform_after_submission_10`) to ensure your code only runs for the specific form, rather than writing an `if ( $form['id'] != 10 ) return;` inside the function.
- Do not attempt to update the `$entry` object directly inside `gform_after_submission` by re-saving it to the database unless absolutely necessary; use `gform_pre_submission` if you just need to modify the saved values.
