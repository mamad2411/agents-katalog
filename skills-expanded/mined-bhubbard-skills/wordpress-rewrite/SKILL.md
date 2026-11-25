---
name: wordpress-rewrite
description: WordPress URL rewriting — pretty permalinks, custom rewrite rules, endpoints, and query vars. Use when adding a custom URL pattern (e.g., /api/foo/123), exposing a custom query var, adding an endpoint to a post type (/post-name/version/2), changing the permalink structure, or debugging "404 on a URL that should work" issues. Covers add_rewrite_rule, add_rewrite_endpoint, add_rewrite_tag, add_permastruct, flush_rewrite_rules, and query_vars.
---

# WordPress Rewrite API

The rewrite system turns pretty URLs like `/2024/05/my-post/` into the equivalent query (`?year=2024&monthnum=05&name=my-post`). It's two pieces: regex rules that match URLs to query strings, and a query-var registry that tells WordPress which query keys are legal.

Plugins extend it to add custom URL patterns (RESTful-style routes that aren't actual REST endpoints, vanity URLs, version-suffixed permalinks like `/post/feedback/`, etc.).

## The core mental model

1. WordPress reads the URL.
2. `WP_Rewrite` compares it against an ordered list of regexes.
3. The first match's "query" string (`index.php?page_id=$1`) becomes the parsed query.
4. `WP_Query` runs against those query vars and selects content.

If no rule matches, WordPress falls through to a `404`. Rewrite rules are stored in the `rewrite_rules` option as a serialized array — when you change them, you must **flush**, otherwise the cached rules still win.

## Adding a custom rewrite rule

```php
add_action( 'init', function () {
    add_rewrite_rule(
        '^api/items/([0-9]+)/?$',          // The URL regex (after the home_url root).
        'index.php?my_item_id=$matches[1]', // The "query" — what WP_Query will see.
        'top'                               // 'top' to insert before built-ins, 'bottom' after.
    );
} );

add_filter( 'query_vars', function ( $vars ) {
    $vars[] = 'my_item_id';
    return $vars;
} );

add_action( 'template_redirect', function () {
    $id = (int) get_query_var( 'my_item_id' );
    if ( $id > 0 ) {
        header( 'Content-Type: application/json' );
        echo wp_json_encode( my_item_data( $id ) );
        exit;
    }
} );
```

Three pieces — every custom URL needs all three:

1. **The rule** (regex → query string).
2. **The query var registration** (otherwise WP strips it as unknown).
3. **The handler** (typically `template_redirect`, or `parse_request` for earlier intercept).

## The flushing dance — the #1 source of "but I added the rule!" bugs

`add_rewrite_rule()` only runs at request time. It doesn't persist anywhere. WordPress caches the *generated* ruleset in the `rewrite_rules` option, and only regenerates on flush.

**Right way:** flush exactly once, on plugin activation:

```php
register_activation_hook( __FILE__, function () {
    // Re-register your rules so they're known...
    myplugin_register_rewrite_rules();
    // ...then flush so they get baked into the option.
    flush_rewrite_rules();
} );

register_deactivation_hook( __FILE__, function () {
    flush_rewrite_rules();          // Clean up.
} );
```

**Never** call `flush_rewrite_rules()` on every request — it's a disk-flushing op that rewrites `.htaccess` and the `rewrite_rules` option. You'll tank performance.

If you're hacking and need to manually flush, go to Settings → Permalinks and click "Save" without changing anything. That's the equivalent.

## Endpoints — append a segment to existing URLs

`add_rewrite_endpoint()` lets you add suffixes like `/post-name/version/2/` or `/products/widget/reviews/`:

```php
add_action( 'init', function () {
    add_rewrite_endpoint( 'version', EP_PERMALINK | EP_PAGES, $query_var = 'version' );
} );

// Now URLs like /hello-world/version/3/ work, with get_query_var( 'version' ) = '3'.
add_action( 'template_redirect', function () {
    $v = get_query_var( 'version' );
    if ( $v !== '' ) {
        // We're on a versioned post.
    }
} );
```

The `$places` bitmask says which contexts the endpoint applies to: `EP_PERMALINK` (single posts), `EP_PAGES` (pages), `EP_CATEGORIES`, `EP_TAGS`, `EP_AUTHORS`, `EP_DATE`, `EP_ROOT`, `EP_ALL`, etc. (See `wp-includes/class-wp-rewrite.php` for the full list.)

Endpoints are far more reliable than hand-rolled rewrite rules for "append a thing to a URL" — WordPress maintains them across permalink structure changes.

## Rewrite tags — make `%foo%` valid in permalinks

If you want `%book_genre%` to be substitutable in the permalink structure (e.g., the user sets `/books/%book_genre%/%postname%/`), register the tag:

```php
add_rewrite_tag( '%book_genre%', '([^/]+)', 'book_genre=' );
```

`add_rewrite_tag` does two things: makes the tag legal in permastructs, and registers the regex + query mapping.

Combine with a permastruct (custom permalink structure for a CPT):

```php
add_action( 'init', function () {
    add_rewrite_tag( '%book_genre%', '([^/]+)', 'book_genre=' );
    add_permastruct( 'book', '/books/%book_genre%/%book%', array( 'with_front' => false ) );
} );
```

The `register_post_type` `rewrite` arg generally handles this for you — `add_permastruct` is the lower-level API.

## Debugging — see what rules WordPress actually has

```php
global $wp_rewrite;

// All current rules (regex => query):
$rules = $wp_rewrite->wp_rewrite_rules();

// Or grouped by source:
$rules = $wp_rewrite->rewrite_rules();

// Try a URL manually:
$matched = url_to_postid( 'https://example.com/2024/05/hello-world/' );
```

A handy snippet to dump current rules in `wp-admin`:

```php
add_action( 'admin_init', function () {
    if ( current_user_can( 'manage_options' ) && isset( $_GET['dump_rules'] ) ) {
        global $wp_rewrite;
        echo '<pre>'; print_r( $wp_rewrite->wp_rewrite_rules() ); exit;
    }
} );
```

## Permalink structure

The `permalink_structure` option controls the global pretty-URL format. Default (since WP 5.0) is `/%year%/%monthnum%/%day%/%postname%/`. Available tags: `%year% %monthnum% %day% %hour% %minute% %second% %postname% %post_id% %category% %author%` (and registered custom tags).

Changing the option in `wp-config.php` is **not** how to do this — set it in Settings → Permalinks, or via `update_option( 'permalink_structure', '/%postname%/' )` followed by `flush_rewrite_rules()`.

## Rewriting the front and category bases

```php
update_option( 'category_base', 'topic' );          // /topic/ instead of /category/.
update_option( 'tag_base',      'label' );          // /label/ instead of /tag/.
// Then flush.
```

## The init/template_redirect/parse_request order

When a URL hits WordPress, the order is:

1. `parse_request` — earliest, `$wp->query_vars` has just been populated. Override here to bypass `WP_Query` entirely.
2. `pre_get_posts` — before the main query runs.
3. `template_redirect` — query is done, before any template loads. The usual spot to intercept and emit a custom response.
4. `template_include` — last chance to swap the template file.

For custom JSON-emitting routes, `template_redirect` is the conventional intercept point.

## Where to look in this codebase

- `wp-includes/rewrite.php` — function-level API: `add_rewrite_rule`, `add_rewrite_endpoint`, `add_rewrite_tag`, `add_permastruct`, `flush_rewrite_rules`, `url_to_postid`.
- `wp-includes/class-wp-rewrite.php` — `WP_Rewrite` class. Look at `generate_rewrite_rules()` to see how custom post-type permalinks get composed, and `wp_rewrite_rules()` for the cached structure.
- `wp-includes/class-wp.php` — `WP::parse_request()` is what actually applies the rules.
- `wp-includes/canonical.php` — `redirect_canonical()`, the function that 301s typo'd URLs to the right one.

## Common pitfalls

- Forgetting to flush after registering a rule. The rule simply doesn't apply.
- Flushing on every page load. Catastrophic for performance.
- Forgetting the `query_vars` filter. WordPress strips any query var it doesn't recognize, so your rule's `$matches[1]` ends up in a dead var.
- Putting custom rules at `'bottom'` and being shadowed by a more general built-in rule. Use `'top'` for specificity wins.
- Using `add_rewrite_rule()` inside `template_redirect` or another late hook — must be `init`.
- Regex that's too permissive — e.g., `^api/(.+)$` will swallow `/api/foo/bar/baz`. Anchor and constrain (`[0-9]+`, `[a-z-]+`).
- Forgetting that on nginx, `.htaccess` isn't read — pretty permalinks need server-level `try_files $uri $uri/ /index.php?$args;` in the nginx config. WordPress can't fix that with `flush_rewrite_rules`.
