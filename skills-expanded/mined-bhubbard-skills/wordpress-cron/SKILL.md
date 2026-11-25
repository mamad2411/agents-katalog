---
name: wordpress-cron
description: WordPress's pseudo-cron system — wp_schedule_event, wp_schedule_single_event, custom intervals, and reliable scheduling via system cron. Use when scheduling recurring tasks (daily/hourly jobs), enqueueing one-off background work, building custom recurrence intervals, debugging "my hook never runs," or disabling WP-cron in favor of system cron for reliability. Covers wp-cron.php, the _cron option, and DISABLE_WP_CRON.
---

# WordPress Cron (wp-cron)

WordPress's "cron" is not real cron. It's a queue of `(timestamp, hook, args)` tuples stored in the `cron` option. On every page load, WordPress checks whether any due events exist; if so, it fires off a non-blocking HTTP request to `/wp-cron.php`, which dispatches the events.

This means:

- Events fire approximately on time — only when someone visits the site.
- A site with no traffic is a site with no cron.
- The site has to be able to reach itself over HTTP (often a problem with HTTPS misconfiguration, basic-auth staging sites, or aggressive firewalls).

For reliability, **disable WP-cron and trigger `wp-cron.php` from a real system cron**.

## Scheduling — three patterns

### Recurring event

```php
register_activation_hook( __FILE__, function () {
    if ( ! wp_next_scheduled( 'myplugin_sync_event' ) ) {
        wp_schedule_event( time(), 'hourly', 'myplugin_sync_event' );
    }
} );

register_deactivation_hook( __FILE__, function () {
    wp_clear_scheduled_hook( 'myplugin_sync_event' );
} );

add_action( 'myplugin_sync_event', 'myplugin_run_sync' );
function myplugin_run_sync() {
    // Heavy lifting here.
}
```

Available default recurrences: `hourly`, `twicedaily`, `daily`, `weekly`. Add custom ones via `cron_schedules` filter (see below).

### Single (one-off) future event

```php
// In 5 minutes from now:
wp_schedule_single_event( time() + 5 * MINUTE_IN_SECONDS, 'myplugin_followup', array( $user_id, $context ) );

add_action( 'myplugin_followup', function ( $user_id, $context ) {
    // ...
}, 10, 2 );
```

Use this for "do this thing later" — sending a delayed notification, fetching a slow report, etc. The args you pass through here are uniquely keyed; firing twice with the same args replaces the existing schedule rather than queuing twice.

### Immediate (very-soon) one-off — the "background job" pattern

```php
wp_schedule_single_event( time(), 'myplugin_background_work', array( $payload ) );
```

By scheduling for "now," WP-cron fires it on the next page load. Useful for offloading work from a user-facing request — return the response immediately, do the slow thing on the next request.

## Adding a custom interval

```php
add_filter( 'cron_schedules', function ( array $schedules ) {
    $schedules['every_fifteen_minutes'] = array(
        'interval' => 15 * MINUTE_IN_SECONDS,
        'display'  => __( 'Every 15 Minutes', 'myplugin' ),
    );
    $schedules['every_five_minutes'] = array(
        'interval' => 5 * MINUTE_IN_SECONDS,
        'display'  => __( 'Every 5 Minutes', 'myplugin' ),
    );
    return $schedules;
} );

// Then use:
wp_schedule_event( time(), 'every_fifteen_minutes', 'myplugin_check' );
```

## Inspecting and clearing

```php
// Is this hook scheduled? (returns next timestamp or false)
$next = wp_next_scheduled( 'myplugin_sync_event' );
if ( $next ) {
    echo 'Next run: ' . date_i18n( 'Y-m-d H:i', $next );
}

// What's the recurrence?
$schedule = wp_get_schedule( 'myplugin_sync_event' );      // 'hourly', 'daily', etc., or false.

// Get the full event:
$event = wp_get_scheduled_event( 'myplugin_sync_event' );  // stdClass with hook/timestamp/schedule/args.

// Clear ALL future instances of a hook (regardless of args):
wp_unschedule_hook( 'myplugin_sync_event' );

// Clear a specific instance (must match args exactly):
wp_clear_scheduled_hook( 'myplugin_sync_event', array( $user_id ) );

// Cancel a single one-off:
wp_unschedule_event( $timestamp, 'myplugin_followup', $args );
```

## The reliability problem — replace WP-cron with system cron

In `wp-config.php`:

```php
define( 'DISABLE_WP_CRON', true );
```

This stops WordPress from spawning its own cron on page loads. Now trigger it externally:

```cron
# /etc/cron.d/wordpress — runs every minute
* * * * * www-data wget -qO- https://example.com/wp-cron.php?doing_wp_cron > /dev/null 2>&1
```

Or with curl (preferred — no DNS caching issues):

```cron
* * * * * www-data curl -fsS "https://example.com/wp-cron.php?doing_wp_cron" > /dev/null
```

Or with WP-CLI (avoids the HTTP round-trip):

```cron
* * * * * www-data /usr/local/bin/wp --path=/var/www/html cron event run --due-now --quiet
```

Every minute is the practical minimum and what most production sites use. WordPress checks event timestamps with second resolution but only runs whatever's due at trigger time.

## Avoiding overlap

If your cron job is long-running, two requests can fire it concurrently. Use a transient lock:

```php
add_action( 'myplugin_sync_event', function () {
    if ( get_transient( 'myplugin_sync_lock' ) ) {
        return;   // Already running.
    }
    set_transient( 'myplugin_sync_lock', 1, 10 * MINUTE_IN_SECONDS );

    try {
        myplugin_do_work();
    } finally {
        delete_transient( 'myplugin_sync_lock' );
    }
} );
```

`WP_CRON_LOCK_TIMEOUT` in wp-config (default 60s) controls WP's own internal lock that prevents simultaneous `wp-cron.php` requests from doubling up.

## Debugging cron

Quick checks:

```php
// Dump the entire cron queue:
$cron = _get_cron_array();
print_r( $cron );

// Or via WP-CLI:
// wp cron event list
// wp cron event run myplugin_sync_event
// wp cron event delete myplugin_sync_event
// wp cron test           — verify wp-cron is reachable.
```

The `cron` option is a giant nested array keyed by timestamp → hook → arg-hash → schedule info. If you see hundreds of stale `myplugin_*` entries, you've been scheduling without checking `wp_next_scheduled` first.

A common gotcha: if `wp-cron.php` is blocked by HTTP Basic Auth on staging, you'll see no cron runs at all. The fix is to either allow `/wp-cron.php` through auth, or disable WP-cron and use system cron.

## The Action Scheduler alternative

For high-volume background work (more than a handful of events per minute), WP-cron isn't the right tool. Use [Action Scheduler](https://actionscheduler.org/) — a database-backed queue with proper concurrency, retry logic, and admin UI. It's the engine behind WooCommerce, bundled with most major plugins.

API is similar (`as_schedule_single_action`, `as_schedule_recurring_action`), so migration from `wp_schedule_event` is straightforward.

## Where to look in this codebase

- `wp-includes/cron.php` — entire cron API: `wp_schedule_event`, `wp_schedule_single_event`, `wp_unschedule_event`, `wp_clear_scheduled_hook`, `wp_next_scheduled`, `wp_get_schedules`, `_get_cron_array`, `_set_cron_array`.
- `wp-cron.php` (in the WordPress root) — the script system cron should hit. Reads the `cron` option, runs due events, marks them done.
- `wp-includes/default-filters.php` — where `cron_schedules` defaults are added.
- `wp-includes/load.php` — the `wp_cron()` call that fires off the background HTTP request on each pageload.

## Common pitfalls

- Scheduling on every page load instead of only when not already scheduled. Wrap in `if ( ! wp_next_scheduled( ... ) )`.
- Passing different args each time you schedule. WordPress treats them as different events; you end up with many duplicates.
- Not clearing scheduled events on plugin deactivation. They keep firing into the void.
- Relying on WP-cron precision. On low-traffic sites, "hourly" can stretch to a day. Use system cron.
- Long-running cron handlers without a lock. Concurrent runs corrupt data.
- Heavy work in cron without rate-limiting. WP-cron requests are HTTP — they have a default 5s timeout. Use single-event chains (each callback schedules the next) instead of one giant job.
- Forgetting `add_action( 'myplugin_sync_event', ... )`. Without a listener, the event fires into nothing.
- Trying to schedule from CLI/cron contexts without bootstrapping WP. Use WP-CLI for those (`wp eval "wp_schedule_event(...)"`).
