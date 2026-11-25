---
name: wordpress-scripts-styles
description: WordPress script and style enqueueing — wp_enqueue_script, wp_enqueue_style, wp_register_script, dependencies, in_footer, strategy (async/defer), wp_localize_script, wp_add_inline_script/style, conditional comments, version cache-busting. Use when adding CSS/JS to a plugin/theme, passing PHP data to JS, deferring scripts, fixing dependency ordering, or debugging "my script isn't loading."
---

# WordPress Scripts and Styles (Enqueue API)

`wp_enqueue_script` and `wp_enqueue_style` are how PHP tells WordPress to emit `<script>` and `<link rel="stylesheet">` tags. Never write those tags directly in templates — the enqueue API tracks dependencies, handles versioning for cache-busting, deduplicates, and integrates with the block editor.

Two parallel systems exist: **classic scripts** (`wp_register_script` / `wp_enqueue_script`) and **script modules** (`wp_register_script_module`, since 6.5+, covered in `wordpress-script-modules`).

## The lifecycle

WordPress maintains two registries (`WP_Scripts`, `WP_Styles`) keyed by **handle**. The lifecycle:

1. **Register** — record the asset's metadata (URL, dependencies, version, args). Doesn't emit anything yet.
2. **Enqueue** — mark a registered asset for output on the current request. Also emits any not-yet-registered deps.
3. **Print** — WordPress writes the `<script>`/`<link>` tags at the right place (head, footer, admin head, etc.).

You can skip step 1 and pass the URL directly to `wp_enqueue_script` — but registering first is the right pattern for shared assets used by multiple places.

## The two hooks

```php
// Frontend:
add_action( 'wp_enqueue_scripts', function () {
    wp_enqueue_style(  'mytheme-style', get_stylesheet_uri(), array(), '1.0' );
    wp_enqueue_script( 'mytheme-main', get_template_directory_uri() . '/js/main.js', array( 'jquery' ), '1.0', array(
        'in_footer' => true,
        'strategy'  => 'defer',
    ) );
} );

// Admin:
add_action( 'admin_enqueue_scripts', function ( $hook_suffix ) {
    // $hook_suffix lets you load assets only on specific admin pages.
    if ( 'toplevel_page_myplugin' !== $hook_suffix ) {
        return;
    }
    wp_enqueue_script( 'myplugin-admin', plugins_url( 'js/admin.js', __FILE__ ), array( 'wp-element' ), '1.0', true );
} );

// Block editor (separate from admin):
add_action( 'enqueue_block_editor_assets', function () {
    wp_enqueue_script( 'myplugin-editor', plugins_url( 'js/editor.js', __FILE__ ), array( 'wp-blocks' ), '1.0', true );
} );

// Login screen:
add_action( 'login_enqueue_scripts', /* ... */ );

// Customizer:
add_action( 'customize_preview_init',   /* ... */ );    // Preview iframe.
add_action( 'customize_controls_enqueue_scripts', /* ... */ );    // Parent frame.
```

## The signatures

```php
wp_register_script( $handle, $src, $deps = array(), $ver = false, $args = array() );
wp_enqueue_script(  $handle, $src = '', $deps = array(), $ver = false, $args = array() );
//
// $args is array since 6.3, was bool (in_footer) before. Accepts:
//   array( 'in_footer' => true, 'strategy' => 'defer' | 'async' )
// Legacy: passing true/false for $args still works (= in_footer).

wp_register_style( $handle, $src, $deps = array(), $ver = false, $media = 'all' );
wp_enqueue_style(  $handle, $src = '', $deps = array(), $ver = false, $media = 'all' );
```

`$ver` controls cache-busting:

- `false` (default) — uses WP core version. Bad: every WP update busts your cache.
- `'1.2.3'` — your plugin/theme version. **The right choice.** Bump on release.
- `null` — emits no version query string. Use only when the URL itself contains a hash (e.g., from Webpack).
- Function call like `filemtime( $path )` — file-mtime-based cache busting, automatic.

## Dependencies

Deps are an array of registered handles. WordPress topologically sorts them — your script will print after all of its deps.

```php
wp_enqueue_script( 'mytheme-main', $url, array(
    'jquery',           // Core jQuery, always registered.
    'wp-element',       // React for the block editor.
    'wp-i18n',          // i18n utilities.
    'mytheme-utils',    // Your own previously-registered handle.
), '1.0', true );
```

Common core-provided handles:

- `jquery`, `jquery-core`, `jquery-migrate`, `jquery-ui-core`, `jquery-ui-sortable`, etc.
- `wp-element` (React wrapper), `wp-components` (UI lib), `wp-data` (state), `wp-blocks`, `wp-block-editor`, `wp-i18n`, `wp-api-fetch`, `wp-html-entities`.
- `wp-polyfill`, `wp-hooks`.
- `underscore`, `backbone`.
- `react`, `react-dom`, `lodash`, `moment` (deprecated but still registered).

For the canonical current list, grep `script-loader.php` for `wp_register_script(`.

## In-footer vs in-head

By default scripts go in `<head>`. Setting `in_footer => true` (or the legacy `true` arg) moves them to before `</body>` — better for perceived performance because the HTML can render before the JS evaluates.

`enqueue_block_editor_assets` ignores `in_footer` (block editor scripts are always in head).

## Strategy: async vs defer (WP 6.3+)

```php
wp_enqueue_script( 'analytics', $url, array(), '1.0', array(
    'in_footer' => false,
    'strategy'  => 'async',     // Or 'defer'.
) );
```

- **defer** — script downloads in parallel with HTML parsing, executes after parsing completes, in document order. Use for scripts that depend on DOM but don't block render.
- **async** — script downloads in parallel and executes ASAP, may interrupt parsing, no order guarantee. Use for fire-and-forget telemetry.

A script with deps can use `strategy => 'defer'`; WordPress automatically figures out the correct combination. `async` requires the script to be dependency-free (otherwise it might execute before its deps).

## Passing data to JS — wp_localize_script and wp_add_inline_script

`wp_localize_script` injects a JS object before the target script loads:

```php
wp_localize_script( 'myplugin-app', 'MyPluginData', array(
    'restUrl'   => esc_url_raw( rest_url( 'myplugin/v1/' ) ),
    'nonce'     => wp_create_nonce( 'wp_rest' ),
    'currentId' => get_the_ID(),
    'strings'   => array(
        'confirmDelete' => __( 'Really delete?', 'myplugin' ),
    ),
) );
// In JS: window.MyPluginData.restUrl, window.MyPluginData.strings.confirmDelete
```

Despite the name, this works for any data — not just localization strings. The data is serialized to JSON and emitted as a `<script>` block right before the target.

`wp_add_inline_script` is the more flexible modern API — append (or prepend) raw JS:

```php
wp_add_inline_script( 'myplugin-app',
    'window.MyPluginData = ' . wp_json_encode( $data ) . ';',
    'before'      // Or 'after' (default).
);
```

Same effect, but you control the exact JS. Prefer `wp_add_inline_script` for new code — `wp_localize_script` runs values through `_wp_specialchars`, which corrupts non-string data.

## Inline styles

```php
wp_add_inline_style( 'mytheme-style', "
    body { background: " . sanitize_hex_color( $color ) . "; }
" );
```

Concatenated to the registered style's `<style>` block after it's printed. Useful for dynamic CSS variables generated from user options.

## Deregistering and dequeueing

```php
// Stop a previously-enqueued script:
wp_dequeue_script( 'old-handle' );
wp_deregister_script( 'old-handle' );      // Remove from the registry entirely.

// Check status:
wp_script_is( 'jquery', 'enqueued' );      // 'enqueued' | 'registered' | 'queue' | 'to_do' | 'done'.
```

Useful when a theme or plugin enqueues something you want to replace — dequeue + re-enqueue with your own version.

## Conditional / IE comments (legacy)

```php
$styles = wp_styles();
$styles->add_data( 'mytheme-ie', 'conditional', 'lt IE 9' );
```

Rarely needed in 2026.

## Path helpers

```php
get_stylesheet_uri()                       // The active theme's style.css URL.
get_stylesheet_directory_uri()             // Active theme dir URL (child theme aware).
get_template_directory_uri()               // Parent theme dir URL.
plugins_url( 'js/app.js', __FILE__ )       // Plugin file URL.
includes_url( 'js/wp-emoji-release.min.js' )  // wp-includes URL.
admin_url( 'load-scripts.php' )            // wp-admin URL.
```

Use these helpers instead of hardcoding `/wp-content/themes/...`. They survive folder reorganization and respect `WP_CONTENT_URL` / multisite quirks.

## Debugging "my script isn't loading"

1. View source — is the `<script>` tag emitted at all?
2. If not: are you hooking on the right hook? (`wp_enqueue_scripts` is frontend; nothing on the admin pages.)
3. Is the handle wrong (typos in deps)? An unknown dep silently drops the dependent script.
4. Open the network panel — is the URL right? Many "broken" enqueues are 404s with the wrong path.
5. `wp_script_is( 'my-handle', 'enqueued' )` — quickly diagnose registration vs enqueue state.

## Where to look in this codebase

- `wp-includes/script-loader.php` — registers all core scripts and styles. **Read this** to find the official handles for `jquery-ui-*`, the `wp-*` block editor scripts, etc.
- `wp-includes/functions.wp-scripts.php` — `wp_register_script`, `wp_enqueue_script`, `wp_localize_script`, `wp_add_inline_script`, `wp_script_is`.
- `wp-includes/functions.wp-styles.php` — same for styles.
- `wp-includes/class-wp-scripts.php` — `WP_Scripts` (extends `WP_Dependencies`). The actual scheduler.
- `wp-includes/class-wp-styles.php` — `WP_Styles`.
- `wp-includes/class-wp-dependencies.php` — `WP_Dependencies` base class. The topological-sort logic lives here.
- `wp-includes/class-wp-script-modules.php` — ES module enqueuing (covered in `wordpress-script-modules`).

## Common pitfalls

- Enqueueing from the wrong hook: `wp_enqueue_script` called on `init` runs before WordPress is ready to print. Use `wp_enqueue_scripts` (frontend) or `admin_enqueue_scripts` (admin).
- Passing `false` for `$ver` and getting unintended cache-busting on every WP update. Always set your own version.
- Using `wp_localize_script` for non-string data — booleans and ints come out as strings due to `_wp_specialchars`. Use `wp_add_inline_script` with `wp_json_encode` instead.
- Missing dep — script silently doesn't enqueue. WP doesn't error, it just skips.
- Loading jQuery from a CDN by dequeueing the core one and registering a CDN URL — works, but breaks if any plugin's `wp-` deps need the jQuery version WP ships.
- Using `enqueue_block_editor_assets` for frontend block assets. That hook is editor-only. Frontend assets for blocks should be in `block.json` as `viewScript` / `style`.
- Setting `in_footer => false` for analytics scripts — they download in the head, can block other resources. Use `strategy => 'async'` instead.
- Concatenating user input into `wp_add_inline_script` without escaping. The inline JS is raw — sanitize as if writing JS by hand.
