---
name: gravity-forms-notifications-object
description: "Manipulating the Notifications object programmatically."
---

# Gravity Forms Notifications Object

The Notifications object is an associative array found within the Form Object. It contains configurations for all the email notifications set up for that form.

## Reference
[Notifications Object Documentation](https://docs.gravityforms.com/notifications-object/)

## Structure
Notifications are stored in `$form['notifications']`. The keys are unique notification IDs (generated hashes), and the values are the notification configuration arrays.

```php
$notifications = array(
    '63f12b7a9c8e1' => array(
        'id'       => '63f12b7a9c8e1',
        'isActive' => true,
        'to'       => 'admin@example.com',
        'name'     => 'Admin Notification',
        'event'    => 'form_submission',
        'toType'   => 'email', // email, field, routing
        'subject'  => 'New Submission',
        'message'  => '{all_fields}',
        'from'     => '{admin_email}',
        'fromName' => 'Website',
        'replyTo'  => '',
        'bcc'      => ''
    )
);
```

## Common Usage

### Modifying a Notification Dynamically
You can modify who receives an email or what the email contains right before it is sent using the `gform_notification` filter.

```php
add_filter( 'gform_notification_5', 'change_notification_routing', 10, 3 );
function change_notification_routing( $notification, $form, $entry ) {
    // Only modify the notification named 'Admin Notification'
    if ( $notification['name'] == 'Admin Notification' ) {
        // Change the recipient based on a field value
        if ( rgar( $entry, '2' ) == 'Sales' ) {
            $notification['to'] = 'sales@example.com';
        } else {
            $notification['to'] = 'support@example.com';
        }
    }
    return $notification;
}
```

## Best Practices
- Use the `gform_notification` filter instead of trying to modify `$form['notifications']` in `gform_pre_submission`. The `gform_notification` filter is specifically designed to safely modify notifications on the fly right before dispatch.
