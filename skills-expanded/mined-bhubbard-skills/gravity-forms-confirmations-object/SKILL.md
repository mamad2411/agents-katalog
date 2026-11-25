---
name: gravity-forms-confirmations-object
description: "Manipulating the Confirmations object programmatically."
---

# Gravity Forms Confirmations Object

The Confirmations object is an associative array found within the Form Object. It contains configurations for what happens immediately after a form is successfully submitted (e.g., showing a message, redirecting to a page).

## Reference
[Confirmations Object Documentation](https://docs.gravityforms.com/confirmations-object/)

## Structure
Confirmations are stored in `$form['confirmations']`. The keys are unique confirmation IDs (generated hashes), and the values are the confirmation configuration arrays. The default confirmation is always keyed as `'default'`.

```php
$confirmations = array(
    'default' => array(
        'id'          => 'default',
        'isDefault'   => true,
        'type'        => 'message', // message, page, redirect
        'name'        => 'Default Confirmation',
        'message'     => 'Thanks for contacting us!',
        'disableAutoformat' => false,
        'pageId'      => '',
        'url'         => '',
        'queryString' => ''
    )
);
```

## Common Usage

### Modifying the Confirmation Dynamically
You can intercept the confirmation process and change the message or the redirect URL on the fly using the `gform_confirmation` filter.

```php
add_filter( 'gform_confirmation_5', 'custom_confirmation', 10, 4 );
function custom_confirmation( $confirmation, $form, $entry, $ajax ) {
    
    // Check a field value in the entry
    if ( rgar( $entry, '3' ) == 'Redirect Me' ) {
        // Change from a message to a redirect
        $url = 'https://example.com/thank-you/?user=' . urlencode( rgar( $entry, '1' ) );
        $confirmation = array( 'redirect' => $url );
    } else {
        // Just append to the existing message
        $confirmation .= " We will be in touch soon.";
    }

    return $confirmation;
}
```

## Best Practices
- Note that the `gform_confirmation` filter expects you to return either a string (for a text/HTML message) or an array in the format `array( 'redirect' => 'https://...' )` if you are forcing a redirect. It does *not* expect you to return the full confirmation associative array structure from the Form object.
