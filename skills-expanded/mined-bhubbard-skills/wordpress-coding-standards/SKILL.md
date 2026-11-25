---
name: wordpress-coding-standards
description: WordPress coding standards, security best practices, and i18n. Use when writing PHP or JS that will be reviewed against WPCS, when escaping/sanitizing user input or output, when adding internationalization (__/_e/_n/_x), when verifying nonces, or when you need to know whether a value should be sanitized on input vs escaped on output. Covers PHPCS-WordPress rules, the late-escaping discipline, kses, and nonce verification.
---

# WordPress Coding Standards & Security

WordPress has its own coding conventions (WPCS), enforced by PHPCS with the `WordPress-Core` / `WordPress-Extra` / `WordPress-VIP` rulesets. The conventions look idiosyncratic but are consistent throughout the ~2M-line core codebase.

## Cardinal rule: sanitize on input, escape on output

This is the discipline that prevents XSS and most injection issues:

- **Sanitize on input.** Data coming from a user (`$_POST`, `$_GET`, REST request body, options form) gets passed through a sanitize function before storage.
- **Escape on output.** Data going into HTML/attributes/URLs/JS gets escaped at the moment of rendering — even data that was already sanitized.

"Late escaping" — escape at the exact point the value enters the output, not earlier — is the WordPress convention. It means you can look at a single line of template code and verify it's safe.

### Sanitize helpers (input)

```php
$name   = sanitize_text_field( $_POST['name'] ?? '' );      // Strips tags, trims, normalizes whitespace.
$bio    = sanitize_textarea_field( $_POST['bio'] ?? '' );   // Like above but preserves newlines.
$email  = sanitize_email( $_POST['email'] ?? '' );
$url    = sanitize_url( $_POST['url'] ?? '' );              // Validates scheme, returns '' if bad.
$slug   = sanitize_title( $_POST['slug'] ?? '' );           // For URLs.
$key    = sanitize_key( $_POST['key'] ?? '' );              // a-z 0-9 _ - only.
$file   = sanitize_file_name( $_POST['file'] ?? '' );
$int    = absint( $_POST['count'] ?? 0 );
$html   = wp_kses_post( $_POST['content'] ?? '' );          // Allows post-content HTML.
$html2  = wp_kses( $input, $allowed_tags, $allowed_protocols );  // Custom allowlist.
$hex    = sanitize_hex_color( $_POST['color'] ?? '' );
```

`wp_unslash()` is almost always needed first when reading from `$_POST`/`$_GET`/`$_COOKIE`: WordPress historically adds magic-quotes-style escaping to superglobals, so you have to unslash before sanitizing.

```php
$name = sanitize_text_field( wp_unslash( $_POST['name'] ?? '' ) );
```

### Escape helpers (output)

The four you'll use 95% of the time:

```php
echo esc_html( $text );                  // Inside element bodies.
echo esc_attr( $value );                 // Inside HTML attributes (alt="...", title="...").
echo esc_url( $url );                    // For href, src.
echo esc_js( $literal );                 // Inside inline JS strings.

// Translation-aware variants — escape AND translate in one step:
echo esc_html__( 'Welcome', 'my-plugin' );
echo esc_attr__( 'Click me', 'my-plugin' );
esc_html_e( 'Welcome', 'my-plugin' );    // _e equivalent (echoes directly).
esc_attr_e( 'Click me', 'my-plugin' );
```

For HTML that you intentionally want to allow (e.g., a post body, an admin description):

```php
echo wp_kses_post( $content );                              // Allows post-content HTML.
echo wp_kses( $content, array(
    'a'      => array( 'href' => true, 'rel' => true ),
    'strong' => array(),
    'em'     => array(),
), array( 'http', 'https', 'mailto' ) );
```

For SQL — never concat, always `$wpdb->prepare()` (see `wordpress-data` skill).

## Nonces — CSRF protection

Any state-changing request initiated from a form, link, or AJAX/REST call from a logged-in user must include a nonce. WordPress will not check this for you automatically; you have to call `check_admin_referer`, `wp_verify_nonce`, or `check_ajax_referer`.

### Forms

```php
// In the form:
<form method="post">
    <?php wp_nonce_field( 'myplugin_save_settings', '_myplugin_nonce' ); ?>
    <input name="setting" />
    <button>Save</button>
</form>

// In the handler:
if ( ! isset( $_POST['_myplugin_nonce'] ) ||
     ! wp_verify_nonce( wp_unslash( $_POST['_myplugin_nonce'] ), 'myplugin_save_settings' ) ) {
    wp_die( 'Invalid request.' );
}
if ( ! current_user_can( 'manage_options' ) ) {
    wp_die( 'Forbidden.' );
}
```

`wp_verify_nonce` checks the token; you still need a separate `current_user_can` check for authorization. The nonce is for "this request came from the page I expected", not "this user can do this thing."

### URLs (action links)

```php
$url = wp_nonce_url( admin_url( 'admin.php?page=mine&action=delete&id=' . $id ), 'myplugin_delete_' . $id );
// Then in the handler:
check_admin_referer( 'myplugin_delete_' . $id );
```

`check_admin_referer` dies on failure — convenient for admin handlers.

### REST API

The REST API requires the `X-WP-Nonce` header for cookie-authenticated requests. Pass `wp_create_nonce( 'wp_rest' )` to your JS via `wp_localize_script`, then send it in `X-WP-Nonce`. Other auth methods (Application Passwords, OAuth) don't need a nonce.

### AJAX (admin-ajax.php — legacy)

```php
add_action( 'wp_ajax_my_action',        'my_ajax_handler' );    // Logged in.
add_action( 'wp_ajax_nopriv_my_action', 'my_ajax_handler' );    // Anonymous.
function my_ajax_handler() {
    check_ajax_referer( 'my_ajax_nonce', '_nonce' );
    if ( ! current_user_can( 'edit_posts' ) ) wp_send_json_error( 'forbidden', 403 );
    // ...
    wp_send_json_success( array( 'ok' => true ) );
}
```

## Internationalization (i18n)

Every user-facing string in a plugin or theme should be translatable.

```php
__( 'Hello',  'my-plugin' );                       // Returns string.
_e( 'Hello',  'my-plugin' );                       // Echoes.
_x( 'Post',   'noun',   'my-plugin' );             // With context — same English, different meaning.
_ex( 'Post',  'verb',   'my-plugin' );

// Plurals:
_n( '%d item', '%d items', $count, 'my-plugin' );
sprintf( _n( '%d item', '%d items', $count, 'my-plugin' ), $count );

// Plural + context:
_nx( '%d post', '%d posts', $count, 'noun', 'my-plugin' );

// Combined escape + translate:
esc_html__(  'Hello', 'my-plugin' );
esc_attr__(  'Hello', 'my-plugin' );
esc_html_e(  'Hello', 'my-plugin' );
esc_attr_e(  'Hello', 'my-plugin' );

// Translator comments for ambiguous strings — required by WordPress.org for hosting:
/* translators: 1: user name, 2: post title */
sprintf( __( '%1$s wrote %2$s', 'my-plugin' ), $name, $title );
```

Rules WPCS enforces:

- The text domain **must be a literal string**, not a variable. (Translation tools parse the source.)
- Translators comments must use the exact format `/* translators: ... */` immediately above the call.
- Don't concatenate translatable strings — use `sprintf` with positional placeholders (`%1$s`, `%2$s`).
- Don't translate `__( $variable, 'domain' )` — strings must be static literals.

### Loading translations

```php
// In a plugin's main file, on plugins_loaded:
add_action( 'plugins_loaded', function () {
    load_plugin_textdomain( 'my-plugin', false, dirname( plugin_basename( __FILE__ ) ) . '/languages' );
} );

// In a theme's functions.php:
add_action( 'after_setup_theme', function () {
    load_theme_textdomain( 'my-theme', get_template_directory() . '/languages' );
} );
```

Since WP 4.6 you don't have to call these for `.org` repository plugins/themes — WP autoloads translations.

## Naming and style (WPCS quick reference)

- **Functions and variables**: `snake_case`, prefixed with your plugin slug (`myplugin_do_thing`, `$myplugin_setting`). WPCS will flag unprefixed function names in the global scope.
- **Classes**: `Pascal_Snake_Case`, also prefixed (`class MyPlugin_Widget`). Modern code may use namespaces (`namespace MyPlugin\\Widgets;`) but WP core itself doesn't.
- **Constants**: `UPPER_SNAKE`, prefixed.
- **Hooks**: `snake_case`, prefixed: `myplugin_before_save`, `myplugin_filter_message`.
- **CSS classes**: BEM-ish, `kebab-case`: `wp-block-my-plugin-callout__title`.
- Yoda conditions: `if ( null === $foo )` not `if ( $foo === null )`. (Prevents accidental assignment.)
- Spaces inside parentheses, around operators: `if ( $a && $b ) { foo( $x, $y ); }`.
- Tabs for indentation in PHP, spaces alignment within a line. (Yes, both.)
- Always brace `if`/`while`/`for` bodies, even one-liners.
- Use `array()` not `[]` in core (modern plugins may use `[]` freely; PHPCS-WP allows it via the `WordPress-Extra` config).
- Single-line strings: single quotes unless you need interpolation.

## Capability checks

Always pair the security check pattern:

```php
// 1. Authentication: is this request from who it says it is?
check_admin_referer( 'my_action' );        // Or check_ajax_referer / verify the REST nonce.

// 2. Authorization: is this user allowed to do this?
if ( ! current_user_can( 'edit_post', $post_id ) ) {
    wp_die( __( 'Sorry, you are not allowed to edit this.', 'my-plugin' ), 403 );
}

// 3. Sanitization: is the input shaped correctly?
$title = sanitize_text_field( wp_unslash( $_POST['title'] ?? '' ) );
```

Skipping step 2 because you have step 1 is a common mistake. The nonce only proves "this request came from a page on this site by this user" — not "this user is allowed."

## Safe redirects

```php
wp_safe_redirect( admin_url( 'admin.php?page=mine&saved=1' ) );
exit;
```

`wp_safe_redirect` validates that the target is on an allowed host (defaults: current host). Use this instead of `wp_redirect` for any URL that could include user input — it prevents open redirect vulnerabilities.

## Avoiding common pitfalls

- Using `eval`, `extract`, `create_function`, or `assert` with dynamic input. WPCS forbids them outright in plugins for the .org repo.
- `$_REQUEST` — prefer the specific superglobal so you know whether you're reading from GET or POST.
- `serialize`/`unserialize` on user data — leads to PHP object injection. Use `wp_json_encode`/`json_decode` instead.
- Building SQL by concatenation. Always `$wpdb->prepare()`.
- Echoing raw values from the DB. Always escape on output.
- Using session cookies. WordPress doesn't use PHP sessions — they break caching. Use options or user meta.
- Suppressing errors with `@`. WPCS will flag it; if you need to suppress, use a more targeted approach.
- Disabling escaping with `// phpcs:ignore WordPress.Security.EscapeOutput` — sometimes necessary, but every instance should have a comment explaining why the value is already-escaped.

## Tooling

```bash
# PHPCS with WordPress standards:
composer require --dev wp-coding-standards/wpcs dealerdirect/phpcodesniffer-composer-installer
./vendor/bin/phpcs --standard=WordPress src/
./vendor/bin/phpcbf --standard=WordPress src/         # Auto-fix what's auto-fixable.

# Modern alternative (faster, opinionated):
# - PHPStan + szepeviktor/phpstan-wordpress for static analysis.
# - Psalm with humanmade/psalm-plugin-wordpress.

# JavaScript:
npm install --save-dev @wordpress/scripts
npx wp-scripts lint-js src/         # ESLint with WP rules.
npx wp-scripts lint-style src/      # Stylelint.
```

## Where to look in this codebase

- `wp-includes/formatting.php` — all the `esc_*` and `sanitize_*` helpers.
- `wp-includes/kses.php` — HTML allowlisting (`wp_kses`, `wp_kses_post`, allowed tag lists).
- `wp-includes/pluggable.php` — nonces (`wp_create_nonce`, `wp_verify_nonce`), authentication helpers.
- `wp-includes/l10n.php` — `__`, `_e`, `_x`, `_n`, etc.
- `wp-includes/capabilities.php` — `current_user_can`, `user_can`, role/capability mapping.
- `wp-admin/includes/template.php` — `wp_nonce_field`, `wp_referer_field`, `submit_button`.
