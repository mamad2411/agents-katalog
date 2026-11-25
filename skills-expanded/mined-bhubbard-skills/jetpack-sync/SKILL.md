---
name: jetpack-sync
description: Specialized skill for managing the Jetpack Sync module, which mirrors data from a self-hosted WordPress site to WordPress.com. Use when debugging sync issues or whitelisting custom post types/options.
---

# Jetpack Sync Debugging and Configuration

Jetpack Sync is responsible for sending data from the local WordPress site to WordPress.com servers. This data powers features like Stats, Related Posts, and Search.

## Whitelisting Custom Post Types
By default, Jetpack syncs standard post types. To ensure a custom post type is synced, it must be registered with `public => true`, or explicitly added.

## Whitelisting Options
If you need a custom option synced to WordPress.com, use the `jetpack_options_whitelist` filter.
```php
add_filter( 'jetpack_options_whitelist', function( $options ) {
    $options[] = 'my_custom_option';
    return $options;
} );
```

## Whitelisting Post Meta
To sync custom post meta, use the `jetpack_sync_post_meta_whitelist` filter.
```php
add_filter( 'jetpack_sync_post_meta_whitelist', function( $allowed_meta ) {
    $allowed_meta[] = '_my_custom_meta_key';
    return $allowed_meta;
} );
```

## Debugging
- Check Jetpack > Settings > Debug to view sync health.
- Advise the user to trigger a full sync if data appears completely out of date on WordPress.com.
