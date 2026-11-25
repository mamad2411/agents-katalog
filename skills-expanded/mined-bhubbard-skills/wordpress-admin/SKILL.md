---
name: wordpress-admin
description: WordPress site administration, configuration, debugging, security hardening, and performance tuning. Use when editing wp-config.php, setting WP_DEBUG, configuring multisite, hardening file permissions, troubleshooting white-screen-of-death, tuning memory limits, configuring caching/transients, setting up HTTPS, managing users/roles/capabilities, or anything involving how a WordPress install is operated (as opposed to coded against).
---

# WordPress Site Administration

This skill is for operating a WordPress site — installation, configuration, debugging, security, and performance. Code-level extension work belongs in the `wordpress-development` skill.

## wp-config.php — the canonical configuration

`wp-config.php` lives in the WordPress root. It is the only file you should hand-edit for environmental config. Copy `wp-config-sample.php`, fill in DB credentials, generate fresh salts at https://api.wordpress.org/secret-key/1.1/salt/, then add `define()` lines for any of the constants below.

The order matters: custom defines must come **above** `require_once ABSPATH . 'wp-settings.php';` at the bottom of the file.

### Database

```php
define( 'DB_NAME',     'wordpress' );
define( 'DB_USER',     'wp_user' );
define( 'DB_PASSWORD', 'strong-password' );
define( 'DB_HOST',     'localhost' );        // Or 'localhost:3307', 'db.internal:3306', socket path.
define( 'DB_CHARSET',  'utf8mb4' );
define( 'DB_COLLATE',  '' );                  // Leave empty unless you know you need it.
$table_prefix = 'wp_';                        // Use a non-default prefix for slightly better security.
```

### Debugging — the four-constant pattern

The single most important debugging incantation. Use this in development, never on production:

```php
define( 'WP_DEBUG',         true );           // Turns on PHP notices/warnings.
define( 'WP_DEBUG_LOG',     true );           // Writes them to wp-content/debug.log.
define( 'WP_DEBUG_DISPLAY', false );          // Don't show errors in the page output.
@ini_set( 'display_errors', 0 );              // Belt and suspenders.
define( 'SCRIPT_DEBUG',     true );           // Load non-minified JS/CSS, easier to debug.
define( 'SAVEQUERIES',      true );           // Records all DB queries in $wpdb->queries.
```

For production: all of these should be `false` (or unset). Never leave `WP_DEBUG_DISPLAY` on in production — it leaks paths and stack traces.

`WP_DEBUG_LOG` can also be a custom path: `define( 'WP_DEBUG_LOG', '/var/log/wp/debug.log' );`.

### Memory and timeouts

```php
define( 'WP_MEMORY_LIMIT',     '256M' );      // For frontend.
define( 'WP_MAX_MEMORY_LIMIT', '512M' );      // For admin / image processing.
```

WP raises PHP's `memory_limit` automatically using these. Default WP_MEMORY_LIMIT is 40M (single site) or 64M (multisite), which is too low for any real site.

### Security and locking down

```php
define( 'DISALLOW_FILE_EDIT',  true );        // Hides theme/plugin file editor in admin.
define( 'DISALLOW_FILE_MODS',  true );        // Also blocks plugin/theme install/update from UI.
define( 'FORCE_SSL_ADMIN',     true );        // Force HTTPS for /wp-admin/.
define( 'WP_AUTO_UPDATE_CORE', 'minor' );     // 'minor' | 'major' | true | false | 'beta' | 'rc'.
define( 'AUTOMATIC_UPDATER_DISABLED', false );

// Multi-factor: see Application Passwords for API-only access.
define( 'WP_APPLICATION_PASSWORDS_AVAILABLE', true );

// Block PHP execution in uploads — set this at the webserver level, not in PHP.
```

`DISALLOW_FILE_MODS` is the strongest setting: it stops anyone (even admins) from installing plugins, themes, or updates from the dashboard. You then manage code via deployment instead.

### Performance

```php
define( 'WP_CACHE',                true );    // Lets caching plugins (e.g. WP Super Cache) hook early.
define( 'WP_POST_REVISIONS',       10 );      // Limit revisions per post; false = none.
define( 'AUTOSAVE_INTERVAL',       120 );     // Seconds between autosaves.
define( 'EMPTY_TRASH_DAYS',        30 );      // 0 = disable Trash entirely.
define( 'WP_CRON_LOCK_TIMEOUT',    60 );      // Prevents overlapping cron.
define( 'DISABLE_WP_CRON',         true );    // Then trigger wp-cron.php from system cron.
define( 'CONCATENATE_SCRIPTS',     false );   // Disable script concatenation in admin (helps HTTP/2).
define( 'COMPRESS_CSS',            true );
define( 'COMPRESS_SCRIPTS',        true );
```

For real WP cron, after setting `DISABLE_WP_CRON => true`:

```cron
* * * * * curl -fsS https://example.com/wp-cron.php?doing_wp_cron > /dev/null
```

### Multisite

```php
define( 'WP_ALLOW_MULTISITE', true );         // Enable Tools → Network Setup.
// After running the network installer, WP will instruct you to add:
define( 'MULTISITE',          true );
define( 'SUBDOMAIN_INSTALL',  false );
define( 'DOMAIN_CURRENT_SITE', 'example.com' );
define( 'PATH_CURRENT_SITE',   '/' );
define( 'SITE_ID_CURRENT_SITE', 1 );
define( 'BLOG_ID_CURRENT_SITE', 1 );
```

### URLs (use sparingly)

```php
define( 'WP_HOME',    'https://example.com' );
define( 'WP_SITEURL', 'https://example.com' );
// Setting these in wp-config locks them — the UI fields go read-only. Good for environment-specific overrides.
```

### Behind a proxy / load balancer

If `is_ssl()` returns false even though the user is on HTTPS, the SSL terminates at the proxy. Add:

```php
if ( isset( $_SERVER['HTTP_X_FORWARDED_PROTO'] ) && 'https' === $_SERVER['HTTP_X_FORWARDED_PROTO'] ) {
    $_SERVER['HTTPS'] = 'on';
}
```

### Trusted environment switching

```php
define( 'WP_ENVIRONMENT_TYPE', 'staging' );   // 'local' | 'development' | 'staging' | 'production'.
define( 'WP_DEVELOPMENT_MODE', 'theme' );     // 'core' | 'plugin' | 'theme' | 'all' | '' (default).
```

These let plugin code branch on environment (`wp_get_environment_type()`).

## File and directory permissions

The recommendation for shared hosting and most server setups:

- Directories: `755`
- Files: `644`
- `wp-config.php`: `600` (or `640` if your group is the web server only)
- `wp-content/uploads/`: `755`, writable by the web user

Ownership matters more than mode. The web server's user must own the files for automatic updates to work, but ideally not have write permission on PHP files. A common pattern: deploy user owns code, web user is in deploy group, code is `g+r` only.

## Common breakage and diagnostics

**White screen of death.** Almost always a fatal PHP error. Enable debugging (above), tail `wp-content/debug.log`, look for the last `PHP Fatal error`. If you can't reach admin: rename `wp-content/plugins/` via SSH/FTP to disable all plugins, then rename back one at a time to find the culprit.

**"Briefly unavailable for scheduled maintenance" persists.** WP wrote a `.maintenance` file in the root during an update and didn't remove it. Delete `.maintenance`.

**"Error establishing a database connection."** Wrong DB creds, MySQL is down, or `wp_options` is corrupted. Verify with `mysql -u <user> -p<pass> -h <host> <db>`; if that works, check `WP_ALLOW_REPAIR` then visit `/wp-admin/maint/repair.php`.

**Memory exhausted.** Raise `WP_MEMORY_LIMIT` first, then PHP's `memory_limit` in `php.ini` or `.htaccess`. If a single plugin is the cause, find it via Query Monitor or by deactivating.

**Mixed content warnings after HTTPS migration.** Hard-coded `http://` URLs in `wp_options` (`siteurl`, `home`) and in post content. Use the WP-CLI search-replace below — never a raw SQL find/replace, because serialized strings will break.

## WP-CLI essentials

WP-CLI is the canonical admin tool. Install it with the phar download from wp-cli.org. Run from the WordPress root.

```bash
wp core version
wp core update                                    # Update WordPress.
wp plugin list --status=active
wp plugin install woocommerce --activate
wp plugin update --all
wp theme activate twentytwentyfive
wp user list --role=administrator
wp user create alice alice@example.com --role=editor --user_pass='...'
wp user update alice --user_pass='new-pass'

# The one weird trick — serialized-safe search/replace (after migrations):
wp search-replace 'http://staging.example.com' 'https://example.com' --all-tables --skip-columns=guid --dry-run

wp db export backup.sql
wp db import backup.sql
wp db query "SELECT option_name FROM wp_options WHERE option_name LIKE 'transient_%'"

wp cache flush
wp transient delete --all
wp rewrite flush

# Run a one-off PHP snippet inside the WP environment:
wp eval 'echo wp_get_current_user()->ID;'
wp eval-file my-migration.php
```

`--skip-columns=guid` on search-replace is mandatory: GUIDs must never change, even on a domain migration. They're identifiers, not URLs.

## Users, roles, capabilities

WordPress ships six roles: Super Admin (multisite only), Administrator, Editor, Author, Contributor, Subscriber. Each role has a set of capabilities (`edit_posts`, `publish_posts`, `manage_options`, etc.). When code checks permission, it checks capabilities, not roles.

```php
current_user_can( 'edit_post', $post_id );   // Meta cap — maps to primitive caps per post.
current_user_can( 'manage_options' );        // Primitive cap — admin only.
user_can( $user_id, 'edit_others_posts' );

// Add a custom capability to a role:
$role = get_role( 'editor' );
$role->add_cap( 'edit_published_books' );

// Or a whole new role:
add_role( 'book_manager', 'Book Manager', array(
    'read'                => true,
    'edit_books'          => true,
    'publish_books'       => true,
) );
```

`map_meta_cap` is what translates `edit_post` (a meta cap, post-specific) into primitive caps like `edit_others_posts`. Most code should call `current_user_can( 'edit_post', $id )` rather than checking primitives directly.

## Application Passwords

For programmatic REST access without exposing the user's login password:

1. Edit Profile → Application Passwords → New → name it ("Deploy bot") → generate.
2. Use HTTP Basic Auth with the username and the generated password.

```bash
curl -u "alice:xxxx xxxx xxxx xxxx xxxx xxxx" https://example.com/wp-json/wp/v2/posts
```

Disable globally by filtering `wp_is_application_passwords_available` to `false`.

## Security hardening checklist

- Force HTTPS site-wide (`FORCE_SSL_ADMIN`, `WP_HOME`/`WP_SITEURL` on https).
- `DISALLOW_FILE_MODS => true` and deploy code from version control.
- Strong, unique salts in `wp-config.php`. Rotate them to force re-login.
- Limit login attempts (use a plugin — core has no rate limiting).
- 2FA on admin accounts.
- Keep core, plugins, themes updated. Subscribe to wpvulndb / WPScan feeds.
- Run `wp core verify-checksums` periodically to detect modified core files.
- Backup before every update — db + uploads minimum.
- Web server: block direct execution of PHP in `wp-content/uploads/`. Block access to `wp-config.php`, `xmlrpc.php` (unless you actually need it), `readme.html`, `.git/`, `.env`.
- File integrity monitoring (tripwire/osquery) on production.

## Performance tuning checklist

- Object cache: Redis or Memcached with a drop-in (`wp-content/object-cache.php`). Without one, `wp_cache_*` only caches per-request.
- Page cache: WP Super Cache, W3 Total Cache, or server-level (Varnish, Nginx fastcgi cache, Cloudflare).
- `WP_CACHE => true` so cache plugins can hook in early.
- Limit revisions, autosave interval, empty trash schedule.
- Disable XML-RPC if you don't use it (`add_filter( 'xmlrpc_enabled', '__return_false' );`).
- Use a CDN for `wp-content/uploads/`.
- PHP OPcache enabled and sized appropriately.
- `mysqltuner.pl` to check `innodb_buffer_pool_size`.
- Disable WP cron, run system cron.
- Audit autoloaded options: `wp db query "SELECT option_name, LENGTH(option_value) FROM wp_options WHERE autoload='yes' ORDER BY LENGTH(option_value) DESC LIMIT 20"` — anything over ~1MB is a red flag.

## Where to look in this codebase

- `wp-includes/default-constants.php` — every constant WP defines and its default. Read this when something in `wp-config.php` doesn't seem to do anything.
- `wp-includes/load.php` — the boot sequence (`wp_initial_constants`, `wp_check_php_mysql_versions`).
- `wp-settings.php` — the orchestrator that loads everything in order.
- `wp-admin/includes/upgrade.php` — db schema, install routines.
- `wp-admin/network/` — multisite network admin.
