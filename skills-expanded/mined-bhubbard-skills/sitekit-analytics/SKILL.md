---
name: sitekit-analytics
description: Configuring and debugging the Google Analytics (GA4) integration in Site Kit. Use when troubleshooting missing traffic data or configuring cross-domain tracking.
---

# Site Kit Analytics (GA4)

Site Kit automatically places the GA4 snippet on the site and fetches data for the dashboard.

## Excluding Logged-in Users
By default, Site Kit provides a UI toggle to exclude logged-in users from Analytics tracking. If you need to enforce this programmatically for a specific role:

```php
add_filter( 'googlesitekit_analytics_track_user', function( $track_user, $user ) {
    if ( in_array( 'editor', (array) $user->roles ) ) {
        return false; // Do not track Editors
    }
    return $track_user;
}, 10, 2 );
```

## "Data Gathering" State
When a GA4 property is newly created via Site Kit, it takes 24-48 hours for data to appear. The dashboard will show a "Data Gathering" message during this time.

## Duplicate Tags
If the user's theme or another plugin is already inserting a GA4 tag, Site Kit might detect it. Site Kit can either use the existing tag (if the user has access to that property) or the user must remove the hardcoded tag to let Site Kit place it, preventing double-tracking.
