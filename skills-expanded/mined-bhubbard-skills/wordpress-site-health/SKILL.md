---
name: wordpress-site-health
description: WordPress Site Health — the dashboard at Tools → Site Health that runs diagnostic tests and reports environment info. Use when adding a custom Site Health test (e.g., "verify my API key works"), adding to the Info tab's debug data, building async tests for slow checks, or surfacing plugin-specific health signals. Covers the site_status_tests, site_status_test_result, and debug_information filters.
---

# WordPress Site Health

Site Health (introduced in WP 5.2, expanded since) gives admins a one-screen view of "is this install healthy?" It has two tabs:

- **Status** — pass/fail/recommended tests with status indicators.
- **Info** — a tree of environment data useful for debugging or pasting into support requests.

Plugins extend both via filters. This is a great place to surface "my plugin needs PHP 8.1+", "my API key is invalid", "my Redis connection is broken" — without inventing a new admin page.

## Adding a Status test

Tests come in two flavors:

- **Direct** — synchronous, run when Site Health is loaded. Should be cheap.
- **Async** — fired via AJAX after the page loads. Use for anything that hits the network or runs queries.

### Direct test

```php
add_filter( 'site_status_tests', function ( $tests ) {
    $tests['direct']['myplugin_api_key'] = array(
        'label' => __( 'MyPlugin API key', 'myplugin' ),
        'test'  => 'myplugin_test_api_key',
    );
    return $tests;
} );

function myplugin_test_api_key() {
    $key = get_option( 'myplugin_api_key' );
    if ( $key ) {
        $result = array(
            'label'       => __( 'API key is set', 'myplugin' ),
            'status'      => 'good',                    // 'good' | 'recommended' | 'critical'.
            'badge'       => array(
                'label' => __( 'MyPlugin', 'myplugin' ),
                'color' => 'blue',                       // 'blue' | 'orange' | 'red' | 'gray'.
            ),
            'description' => sprintf(
                '<p>%s</p>',
                esc_html__( 'Your API key is configured.', 'myplugin' )
            ),
            'actions'     => '',                         // Action HTML, e.g., a settings link.
            'test'        => 'myplugin_api_key',         // Echo the test name back.
        );
    } else {
        $result = array(
            'label'       => __( 'API key is missing', 'myplugin' ),
            'status'      => 'critical',
            'badge'       => array(
                'label' => __( 'MyPlugin', 'myplugin' ),
                'color' => 'red',
            ),
            'description' => sprintf(
                '<p>%s</p>',
                esc_html__( 'No API key configured — MyPlugin features are disabled.', 'myplugin' )
            ),
            'actions'     => sprintf(
                '<p><a href="%s">%s</a></p>',
                esc_url( admin_url( 'admin.php?page=myplugin-settings' ) ),
                esc_html__( 'Configure now', 'myplugin' )
            ),
            'test'        => 'myplugin_api_key',
        );
    }
    return $result;
}
```

### Async test (preferred for anything network-bound)

```php
add_filter( 'site_status_tests', function ( $tests ) {
    $tests['async']['myplugin_api_reachable'] = array(
        'label'             => __( 'MyPlugin API reachable', 'myplugin' ),
        'test'              => rest_url( 'myplugin/v1/health' ),  // Hit a REST endpoint async.
        'has_rest'          => true,
        'async_direct_test' => 'myplugin_async_direct_callback',  // Optional sync fallback for direct AJAX.
    );
    return $tests;
} );

// REST callback (registered separately on rest_api_init):
function myplugin_rest_health( WP_REST_Request $req ) {
    $reachable = ( bool ) wp_safe_remote_get( 'https://api.myplugin.com/ping', array( 'timeout' => 5 ) );
    return rest_ensure_response( array(
        'label'       => $reachable ? 'API reachable' : 'API unreachable',
        'status'      => $reachable ? 'good' : 'critical',
        'badge'       => array( 'label' => 'MyPlugin', 'color' => $reachable ? 'blue' : 'red' ),
        'description' => '<p>' . ( $reachable ? 'OK' : 'Could not reach the API.' ) . '</p>',
        'test'        => 'myplugin_api_reachable',
    ) );
}
```

## Status values

- **good** — green, ✓.
- **recommended** — orange, ⚠. Used for "this would be better but isn't critical."
- **critical** — red, ✗. Counts toward the failing-tests headline number.

Use them honestly. If everything's `critical`, nothing's critical.

## Adding to the Info tab

The Info tab is the place to drop debug data — versions, config, environment. It's read-only.

```php
add_filter( 'debug_information', function ( $info ) {
    $info['myplugin'] = array(
        'label'       => __( 'MyPlugin', 'myplugin' ),
        'description' => __( 'Configuration and status of MyPlugin.', 'myplugin' ),
        'show_count'  => true,                          // Show item count in section header.
        'fields'      => array(
            'version' => array(
                'label' => __( 'Plugin version', 'myplugin' ),
                'value' => MYPLUGIN_VERSION,
            ),
            'api_key' => array(
                'label'   => __( 'API key', 'myplugin' ),
                'value'   => get_option( 'myplugin_api_key' )
                                ? '••• (set)'
                                : __( 'Not set', 'myplugin' ),
                'private' => true,                       // Redact when "Copy to clipboard" is clicked.
            ),
            'cache_backend' => array(
                'label' => __( 'Cache backend', 'myplugin' ),
                'value' => wp_using_ext_object_cache() ? 'persistent' : 'runtime',
            ),
        ),
    );
    return $info;
} );
```

The `private` flag is important for anything secret — when the admin clicks "Copy to clipboard" to share with support, private fields are redacted.

## Built-in tests to look at for examples

`wp-admin/includes/class-wp-site-health.php` ships these (every method is a test you can read as a reference):

- `get_test_wordpress_version` — core out-of-date.
- `get_test_plugin_version`, `get_test_theme_version` — extension updates.
- `get_test_php_version`, `get_test_php_extensions` — PHP environment.
- `get_test_sql_server` — DB version.
- `get_test_https_status`, `get_test_ssl_support`.
- `get_test_dotorg_communication` — can WP reach .org.
- `get_test_loopback_requests` — can WP make HTTP requests to itself (critical for WP-cron).
- `get_test_persistent_object_cache` — is a drop-in installed.
- `get_test_page_cache` — is a page cache plugin active.
- `get_test_authorization_header` — is the `Authorization` header reaching PHP (Application Passwords).
- `get_test_scheduled_events` — anything stuck in the cron queue.

These are all worth skimming when writing your own — same shape, lots of patterns to copy.

## When to use Site Health vs an admin notice

Site Health is for **stable diagnostics** that an admin checks deliberately. Notices are for **urgent, current-action issues** ("settings saved", "your trial expires Friday").

If your check would be loud as a notice ("API key missing!"), but the admin has already seen it and dismissed it, Site Health is where it should live thereafter — quiet, available when looked for.

## Where to look in this codebase

- `wp-admin/includes/class-wp-site-health.php` — the main `WP_Site_Health` class, every built-in test, the filter hooks.
- `wp-admin/includes/class-wp-site-health-auto-updates.php` — auto-update-specific tests.
- `wp-includes/rest-api/endpoints/class-wp-rest-site-health-controller.php` — REST endpoints under `/wp-json/wp-site-health/v1/`.
- `wp-admin/site-health.php` and `wp-admin/site-health-info.php` — the two admin pages.

## Common pitfalls

- Putting a slow check in `direct` instead of `async`. The Status page hangs until your test returns.
- Forgetting to set `'test'` in the result array — JS uses it to attach the result to the right row.
- Returning HTML in `description` without escaping — XSS in your own admin.
- Treating Info tab fields as secret. The whole tab is copyable in plaintext; mark sensitive fields `'private' => true`.
- Async tests that don't honor a short timeout. Site Health waits on them and the page feels broken if they take 30s.
- Showing every value as `critical` so it stands out. The headline number is "all critical-status tests," so spamming critical erodes the signal.
- Using Site Health as a settings UI. It's read-only diagnostics — link from `actions` to a real settings page.
