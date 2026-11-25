---
name: simple-history-advanced-filters
description: Utilizing hooks and filters to control exactly what Simple History records and who can see it.
---

# Simple History Advanced Filters

Sometimes Simple History logs too much information, or information you consider private. Using WordPress filters, developers can fine-tune the logging behavior.

## 1. Excluding Users from the Log
If you have automated service accounts, or specific administrators whose actions shouldn't clutter the log, use the `simple_history/log/do_log` filter to exclude them.

```php
add_filter( 'simple_history/log/do_log', function( $do_log, $level, $message, $context, $logger ) {
    
    // Get the current user
    $current_user = wp_get_current_user();

    // Do not log any actions performed by the user 'automation_bot'
    if ( $current_user->user_login === 'automation_bot' ) {
        $do_log = false;
    }

    return $do_log;

}, 10, 5 );
```

## 2. Filtering by Log Level or Logger
You can also discard events based on their severity or the logger that generated them.

```php
add_filter( 'simple_history/log/do_log', function( $do_log, $level, $message, $context, $logger ) {
    
    // Stop logging failed login attempts to save database space
    if ( isset($logger->slug) && $logger->slug === 'SimpleUserLogger' && $message === 'user_login_failed' ) {
        $do_log = false;
    }

    return $do_log;

}, 10, 5 );
```

## 3. Changing Menu Visibility
By default, administrators can see the Simple History log. If you want to change who can view the log, use the `simple_history/view_history_capability` filter.

```php
// Only allow super admins (multisite) to view the history
add_filter( 'simple_history/view_history_capability', function( $capability ) {
    return 'manage_network';
});
```

## 4. Modifying Log Retention
By default, new installs of Simple History keep logs for 30 days (older installs keep 60 days). You can modify this via a constant or filter.

```php
// In wp-config.php: keep logs for 14 days
define( 'SIMPLE_HISTORY_LOG_INSERT_LIMIT_DAYS', 14 );
```
This ensures the `wp_simple_history` database table does not grow uncontrollably on high-traffic sites.
