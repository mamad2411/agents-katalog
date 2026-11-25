---
name: jetpack-subscriptions
description: Customizing Jetpack Subscriptions and Newsletters. Use when modifying subscription forms, subscriber opt-ins, or post notification emails.
---

# Jetpack Subscriptions & Newsletters

Jetpack Subscriptions allows visitors to sign up to receive notifications of new posts or comments.

## Modifying the Subscription Form
You can alter the text and appearance of the subscription widget and block.
```php
add_filter( 'jetpack_subscriptions_settings', function( $settings ) {
    $settings['subscribe_text'] = 'Join our awesome newsletter!';
    return $settings;
} );
```

## Excluding a Post from Email Notifications
If a user wants to publish a post but *not* send it to their subscribers, they can use the Jetpack Sidebar in the block editor to uncheck the "Send to subscribers" option.
Programmatically, you can intercept the publish action, though it's complex due to the asynchronous nature of the sync process.

## Custom Post Types
To enable subscription emails for a custom post type:
```php
add_filter( 'jetpack_supported_modules', function( $modules, $post_type ) {
    if ( 'my_custom_post_type' === $post_type ) {
        $modules[] = 'subscriptions';
    }
    return $modules;
}, 10, 2 );
```
