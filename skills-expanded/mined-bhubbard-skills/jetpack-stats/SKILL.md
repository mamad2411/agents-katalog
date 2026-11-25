---
name: jetpack-stats
description: Customizing Jetpack Stats tracking. Use when a user wants to track logged-in users, exclude certain roles, or implement custom event tracking.
---

# Jetpack Stats Customization

Jetpack Stats provides lightweight traffic tracking.

## Tracking Logged-in Users
By default, Jetpack Stats does not track visits from logged-in users. You can change this via the UI, or by filtering `jetpack_stats_feature_active`.

## Excluding Specific Roles
If you want to track some users but exclude Administrators from polluting your stats:
```php
add_filter( 'jetpack_stats_roles_to_track', function( $roles ) {
    // Remove administrator from the array of tracked roles
    $roles = array_diff( $roles, array( 'administrator' ) );
    return $roles;
} );
```

## Do Not Track (DNT) Support
Jetpack respects the DNT header, but if you need to alter the tracking behavior for privacy compliance (like GDPR consent), you can conditionally dequeue the stats script or use the `jetpack_stats_track_page_view` filter.
