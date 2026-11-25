---
name: wordpress-development
description: WordPress plugin and theme development. Use when writing PHP that runs inside WordPress — registering hooks (actions/filters), custom post types and taxonomies, shortcodes, REST API routes, admin pages, plugin/theme headers, enqueueing scripts and styles, or anything that calls add_action/add_filter/register_post_type/register_rest_route. Also use when reading WordPress source under wp-includes/ or wp-admin/ to understand how core extends itself.
---

# WordPress Development

This skill covers the day-to-day APIs you reach for when extending WordPress: hooks, post types, REST routes, shortcodes, enqueueing, and the plugin/theme manifest files. It assumes WordPress 6.x or later (this repo is 7.1-alpha).

## Plugin and theme bootstrapping

A plugin is any PHP file in `wp-content/plugins/` (or a subdirectory) that starts with a header comment block. WordPress reads only the headers — the file itself is loaded on every request once the plugin is active.

```php
<?php
/*
Plugin Name: My Plugin
Plugin URI:  https://example.com/my-plugin
Description: One-line description.
Version:     1.0.0
Author:      Your Name
License:     GPL v2 or later
Text Domain: my-plugin
Domain Path: /languages
Requires at least: 6.7
Requires PHP: 7.4
*/

// Always guard against direct access.
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
```

Themes use `style.css` for the equivalent header (Theme Name, Author, Version, Text Domain, Requires at least, Tested up to, etc.) and `functions.php` for behavior. Block themes also need `theme.json` and `templates/index.html`.

Never write directly to the database from a plugin header — that file is loaded every request. Use the `register_activation_hook`/`register_deactivation_hook` callbacks instead, and `add_action( 'plugins_loaded', ... )` to defer real work until WordPress is ready.

## Hooks: actions and filters

WordPress's extension model is hooks. Actions fire events; filters transform values. Every callback hooks via `add_action`/`add_filter` and runs later when core (or another plugin) calls `do_action`/`apply_filters`.

```php
// Action: do something at a WP lifecycle point.
add_action( 'init', 'myplugin_register_things' );
function myplugin_register_things() { /* ... */ }

// Filter: receive a value, return a (maybe modified) value.
add_filter( 'the_content', 'myplugin_append_signature' );
function myplugin_append_signature( $content ) {
    return $content . '<p class="sig">— signed</p>';
}

// Priority (default 10) controls order. Lower runs earlier.
// $accepted_args MUST match how many args the callback declares.
add_filter( 'wp_nav_menu_items', 'myplugin_modify_menu', 10, 2 );
function myplugin_modify_menu( $items, $args ) { /* ... */ }
```

Common action hooks worth knowing: `plugins_loaded`, `init`, `wp_loaded`, `wp_enqueue_scripts`, `admin_enqueue_scripts`, `admin_menu`, `admin_init`, `rest_api_init`, `template_redirect`, `save_post`, `wp_footer`, `wp_head`.

To remove someone else's hook, use `remove_action`/`remove_filter` with the **same callback identity and priority** that was originally registered. Anonymous closures cannot be unhooked without holding a reference to them.

## Custom post types and taxonomies

Register on `init`, never earlier:

```php
add_action( 'init', function () {
    register_post_type( 'book', array(
        'labels'       => array( 'name' => __( 'Books', 'my-plugin' ), 'singular_name' => __( 'Book', 'my-plugin' ) ),
        'public'       => true,
        'show_in_rest' => true,             // Required for Gutenberg + REST.
        'supports'     => array( 'title', 'editor', 'thumbnail', 'custom-fields', 'revisions' ),
        'has_archive'  => true,
        'menu_icon'    => 'dashicons-book',
        'rewrite'      => array( 'slug' => 'books' ),
    ) );

    register_taxonomy( 'genre', 'book', array(
        'hierarchical' => true,             // true = category-like, false = tag-like.
        'show_in_rest' => true,
        'rewrite'      => array( 'slug' => 'genres' ),
    ) );
} );
```

After registering or changing rewrite rules, the user must visit Settings → Permalinks once (or you can call `flush_rewrite_rules()` on activation only — never on every request, it's expensive).

`show_in_rest => true` is what unlocks the block editor and exposes the type at `/wp-json/wp/v2/<post_type>`. Without it, the type uses the legacy editor and stays out of REST.

## REST API routes

Always register on `rest_api_init`. `permission_callback` is required since WP 5.5 — omitting it triggers a `_doing_it_wrong` notice. Use `__return_true` only for genuinely public endpoints.

```php
add_action( 'rest_api_init', function () {
    register_rest_route( 'my-plugin/v1', '/items/(?P<id>\d+)', array(
        'methods'             => 'GET',
        'callback'            => 'myplugin_get_item',
        'permission_callback' => function ( $request ) {
            return current_user_can( 'read' );
        },
        'args' => array(
            'id' => array(
                'required'          => true,
                'validate_callback' => fn( $v ) => is_numeric( $v ),
                'sanitize_callback' => 'absint',
            ),
        ),
    ) );
} );

function myplugin_get_item( WP_REST_Request $request ) {
    $id = (int) $request['id'];
    $item = get_post( $id );
    if ( ! $item || 'item' !== $item->post_type ) {
        return new WP_Error( 'not_found', 'Item not found', array( 'status' => 404 ) );
    }
    return rest_ensure_response( array( 'id' => $item->ID, 'title' => $item->post_title ) );
}
```

Namespace REST routes with `vendor/v1` to avoid collision. Return `WP_Error` for failures — REST converts it to the right HTTP status. To add fields to existing object types (post, term, comment, user), use `register_rest_field` instead of a new route.

## Shortcodes

```php
add_shortcode( 'greeting', function ( $atts, $content = null ) {
    $atts = shortcode_atts( array( 'name' => 'world' ), $atts, 'greeting' );
    return '<p>Hello, ' . esc_html( $atts['name'] ) . '</p>';
} );
// Usage in post content: [greeting name="Brandon"]
```

Always return a string from a shortcode — never echo, or it appears in the wrong place. Always sanitize/escape user-supplied attributes.

## Enqueueing scripts and styles

Never `<link>` or `<script>` tags directly into templates — use the enqueue API so dependencies, versions, and async/defer work correctly.

```php
add_action( 'wp_enqueue_scripts', function () {
    wp_enqueue_style(
        'my-plugin-style',
        plugins_url( 'assets/style.css', __FILE__ ),
        array(),                                         // deps
        '1.0.0'                                          // version (cache bust)
    );

    wp_enqueue_script(
        'my-plugin-app',
        plugins_url( 'assets/app.js', __FILE__ ),
        array( 'wp-element' ),                           // deps
        '1.0.0',
        array( 'in_footer' => true, 'strategy' => 'defer' )
    );

    // Pass server data to JS safely:
    wp_localize_script( 'my-plugin-app', 'MyPluginData', array(
        'restUrl' => esc_url_raw( rest_url( 'my-plugin/v1/' ) ),
        'nonce'   => wp_create_nonce( 'wp_rest' ),
    ) );
} );

// Admin assets use a separate hook:
add_action( 'admin_enqueue_scripts', 'myplugin_admin_assets' );
```

For block editor assets, use `enqueue_block_editor_assets` or (preferred) the `editorScript`/`viewScript` entries in `block.json`.

## Admin pages

```php
add_action( 'admin_menu', function () {
    add_menu_page(
        __( 'My Plugin', 'my-plugin' ),    // Page title.
        __( 'My Plugin', 'my-plugin' ),    // Menu title.
        'manage_options',                  // Capability.
        'my-plugin',                       // Slug.
        'myplugin_render_admin_page',      // Callback.
        'dashicons-admin-generic',         // Icon.
        80                                 // Position.
    );
} );

function myplugin_render_admin_page() {
    if ( ! current_user_can( 'manage_options' ) ) { return; }
    // Render form. Use settings_fields() + do_settings_sections() for Settings API.
}

// Register settings (Settings API):
add_action( 'admin_init', function () {
    register_setting( 'myplugin_group', 'myplugin_option', array(
        'type'              => 'string',
        'sanitize_callback' => 'sanitize_text_field',
        'default'           => '',
        'show_in_rest'      => true,       // Exposes at /wp-json/wp/v2/settings.
    ) );
} );
```

## Cron (scheduled events)

WordPress cron fires on page loads — it is **not** a real cron. For reliability, disable WP cron and trigger `wp-cron.php` from a real system cron every minute.

```php
// Schedule on activation:
register_activation_hook( __FILE__, function () {
    if ( ! wp_next_scheduled( 'myplugin_daily_event' ) ) {
        wp_schedule_event( time(), 'daily', 'myplugin_daily_event' );
    }
} );
register_deactivation_hook( __FILE__, function () {
    wp_clear_scheduled_hook( 'myplugin_daily_event' );
} );

add_action( 'myplugin_daily_event', 'myplugin_do_daily_work' );
```

## Activation, deactivation, uninstall

- `register_activation_hook( __FILE__, $callback )` — runs once when the user activates. Use for creating custom tables, default options.
- `register_deactivation_hook( __FILE__, $callback )` — runs once when deactivated. Clean up scheduled events here, **not** options (the user might reactivate).
- `uninstall.php` in the plugin root — runs on full deletion. This is where to drop tables and delete options.

## Where to read the source

When you need to know exactly how a function behaves, search the actual files:

- `wp-includes/plugin.php` — `add_action`, `add_filter`, `apply_filters`, `do_action`, `has_action`, priorities.
- `wp-includes/post.php` — `register_post_type`, `register_post_status`, `get_post`, `wp_insert_post`.
- `wp-includes/taxonomy.php` — `register_taxonomy`, `wp_set_object_terms`.
- `wp-includes/rest-api.php` — `register_rest_route`, `register_rest_field`, `rest_ensure_response`.
- `wp-includes/blocks.php` and `wp-includes/blocks/` — block registration and core blocks.
- `wp-includes/class-wp-hook.php` — the hook implementation itself.

## Common pitfalls

- Registering on the wrong hook. CPTs/taxonomies on `init`, REST routes on `rest_api_init`, admin menu on `admin_menu`, scripts on `wp_enqueue_scripts` (front) or `admin_enqueue_scripts` (admin).
- Forgetting `permission_callback` on REST routes. WP will emit notices and best practice is to set it explicitly even for public endpoints (`__return_true`).
- Forgetting `show_in_rest => true` and then wondering why Gutenberg won't load.
- Calling `flush_rewrite_rules()` on every request instead of activation.
- Echoing from a shortcode callback instead of returning.
- Storing closures in `add_action` and then trying to `remove_action` them later.
