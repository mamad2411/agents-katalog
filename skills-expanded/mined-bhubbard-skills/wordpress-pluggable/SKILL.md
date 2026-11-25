---
name: wordpress-pluggable
description: WordPress pluggable functions — functions in wp-includes/pluggable.php that plugins can completely replace by defining them first. Use when you need to override authentication, email sending, password hashing, redirect validation, nonces, or notification emails. Covers the load order trick, the canonical list (wp_mail, wp_authenticate, wp_new_user_notification, wp_password_change_notification, wp_redirect, wp_safe_redirect, wp_verify_nonce, wp_create_nonce, wp_hash, etc.), and why most overrides should be a filter instead.
---

# WordPress Pluggable Functions

`wp-includes/pluggable.php` is a special file: every function in it is wrapped in `if ( ! function_exists( 'foo' ) )`. That means **a plugin loaded earlier can define the function with its own implementation**, and WordPress will skip defining its version.

This is the original WordPress extension mechanism, predating actions/filters. It still has uses, but for most cases a filter is the right tool — overriding a pluggable function is heavy and conflicts with other plugins that override the same function.

## How the override works

```php
// In a Must-Use plugin (mu-plugins/, loaded before regular plugins) OR a regular plugin
// that loads before WordPress requires pluggable.php.
//
// In practice: define these in an mu-plugin so they're loaded reliably before any
// other plugin (and before WordPress's own pluggable.php load).

if ( ! function_exists( 'wp_mail' ) ) {
    function wp_mail( $to, $subject, $message, $headers = '', $attachments = array() ) {
        // Your replacement.
        return true;
    }
}
```

When `wp-settings.php` later `require`s `pluggable.php`, the existing `wp_mail` already passes `function_exists()` and WordPress's version is skipped.

The "must come first" requirement is why mu-plugins (`wp-content/mu-plugins/`) are the canonical location — they always load before regular plugins.

## The full list (current as of WP 7.x)

The most commonly overridden:

| Function | Purpose |
| --- | --- |
| `wp_mail` | Send email. Override to route through an HTTP API. |
| `wp_authenticate` | Authenticate user with username/password. Override for SSO/SAML/LDAP. |
| `wp_logout` | End the user session. |
| `wp_set_current_user`, `wp_get_current_user` | Current user state. |
| `wp_set_auth_cookie`, `wp_clear_auth_cookie`, `wp_validate_auth_cookie`, `wp_parse_auth_cookie`, `wp_generate_auth_cookie` | Auth cookie machinery. |
| `wp_password_change_notification`, `wp_new_user_notification`, `wp_notify_postauthor`, `wp_notify_moderator` | The various "send notification" emails. |
| `wp_redirect`, `wp_safe_redirect`, `wp_validate_redirect`, `wp_sanitize_redirect` | Redirects. |
| `check_admin_referer`, `check_ajax_referer` | Nonce verification helpers for admin/AJAX. |
| `wp_create_nonce`, `wp_verify_nonce`, `wp_nonce_tick` | Nonce generation/validation. |
| `wp_salt`, `wp_hash` | Hashing primitives. |
| `wp_hash_password`, `wp_check_password`, `wp_set_password` | Password hashing (uses phpass by default). |
| `wp_generate_password` | Generate random passwords. |
| `get_currentuserinfo` | (Deprecated alias of `wp_get_current_user`.) |
| `cache_users`, `get_userdata`, `get_user_by` | User loading shortcuts. |
| `is_user_logged_in` | Quick check. |
| `auth_redirect` | "Redirect to login" helper for auth-required pages. |

For the canonical current list, scan `pluggable.php` for `if ( ! function_exists(`.

## When to override vs filter

**Filter first.** Overriding a pluggable is a last resort. Examples:

| Goal | Don't override... | Instead use... |
| --- | --- | --- |
| Change the From address of `wp_mail` | `wp_mail` | `wp_mail_from`, `wp_mail_from_name` filters. |
| Route email via HTTP API | `wp_mail` | `phpmailer_init` action — set `isSMTP()` or hook in a custom Sender. |
| Add a custom auth provider | `wp_authenticate` | `authenticate` filter — register a higher-priority callback. |
| Custom new-user welcome email | `wp_new_user_notification` | `wp_new_user_notification_email` filter (modifies the email contents). |
| Redirect users post-login | `wp_redirect` | `login_redirect` filter. |
| Logout cleanup | `wp_logout` | `wp_logout` action. |
| Custom password hash | `wp_hash_password`, `wp_check_password` | `wp_password_salt`, `random_password` filters; or override only if you're integrating a vault. |

Override when:

- You genuinely need to replace the entire mechanism (e.g., redirect ALL mail through Mailgun's HTTP API regardless of headers).
- The filter coverage isn't sufficient (e.g., adding cryptographic verification to nonces).
- You're implementing custom session storage that requires replacing the cookie functions.

## Override caveats

1. **Only one plugin can override a function.** If two plugins try to override `wp_mail`, the second one's `if ( ! function_exists( ... ) )` returns false and its replacement never registers. There's no priority system. Conflicts are silent and frustrating.

2. **No fallback.** When your override is active, the core implementation is dormant. If your override has a bug, you can't easily call through to core's version.

3. **Updates can break you.** If core changes the signature or behavior of `wp_mail` between versions, your override still has the old logic. Plugins that override pluggables need to track core changes.

4. **mu-plugins must contain the override directly.** Even if you register the override via an action hook in a regular plugin, it loads too late — `pluggable.php` is required from `wp-settings.php` before regular plugins are loaded for all hooks except a few specific early ones.

## The "must run first" mu-plugin pattern

```php
<?php
// wp-content/mu-plugins/00-overrides.php
// The "00-" prefix sorts it first alphabetically (mu-plugins load in alpha order).

if ( ! function_exists( 'wp_mail' ) ) {
    function wp_mail( $to, $subject, $message, $headers = '', $attachments = array() ) {
        $resp = wp_remote_post( 'https://api.postmarkapp.com/email', array(
            'headers' => array(
                'X-Postmark-Server-Token' => getenv( 'POSTMARK_TOKEN' ),
                'Content-Type'            => 'application/json',
                'Accept'                  => 'application/json',
            ),
            'body' => wp_json_encode( array(
                'From'     => 'no-reply@example.com',
                'To'       => is_array( $to ) ? implode( ',', $to ) : $to,
                'Subject'  => $subject,
                'HtmlBody' => $message,
            ) ),
        ) );
        return ! is_wp_error( $resp ) && 200 === wp_remote_retrieve_response_code( $resp );
    }
}
```

mu-plugins must be a flat file in `wp-content/mu-plugins/` — subdirectories aren't auto-loaded. They have no activation/deactivation lifecycle (they're always on as long as the file is present).

## Detecting overrides

```php
// At runtime — has someone replaced wp_mail?
$reflection = new ReflectionFunction( 'wp_mail' );
$file = $reflection->getFileName();
$is_custom = false === strpos( $file, '/wp-includes/' );
```

Useful for Site Health diagnostics or debug pages.

## Where to look in this codebase

- `wp-includes/pluggable.php` — every pluggable function. Read the top of each one for its `@since` and the filter hooks it calls — those are usually the safer extension point.
- `wp-includes/pluggable-deprecated.php` — pluggables removed/deprecated in recent versions.
- `wp-includes/class-phpass.php` — the password hashing library used by `wp_hash_password` / `wp_check_password`.
- `wp-includes/load.php` — `wp_get_active_and_valid_plugins()` and the loader sequence; shows where mu-plugins fit.

## Common pitfalls

- Putting the override in a regular plugin and wondering why it doesn't work. Regular plugins load too late.
- Two plugins both overriding `wp_mail` and silently fighting. The first one wins; the second one's functionality is gone.
- Overriding `wp_redirect` and forgetting to `exit` after sending headers. Code keeps executing.
- Overriding a pluggable for a behavior change that's available via filter. More fragile, no benefit.
- Overriding a pluggable and not handling the cases the original handles — e.g., your `wp_mail` ignores `$attachments`, breaking forms with file uploads.
- Overriding the auth cookie functions without keeping the underlying cookie schema compatible. Users get logged out and can't log back in.
- Calling `wp_get_current_user()` super-early (before `pluggable.php` is loaded). Use the `set_current_user` action or wait for `init`.
