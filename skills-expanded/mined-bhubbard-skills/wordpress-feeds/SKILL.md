---
name: wordpress-feeds
description: WordPress RSS/Atom feed generation (outbound) and SimplePie-based feed consumption (inbound). Use when adding a custom feed type, modifying the contents of the default feeds (RSS2/Atom/RDF), generating a CPT-specific feed, fetching and parsing external feeds via fetch_feed(), or disabling feeds entirely. Covers add_feed, feed_content_type, do_feed, and SimplePie integration.
---

# WordPress Feeds (RSS/Atom + SimplePie)

WordPress generates feeds at `/feed/`, `/feed/atom/`, `/feed/rdf/`, `/comments/feed/`, plus per-author/category/tag/post variants. It also includes SimplePie for *consuming* feeds — fetching, parsing, and displaying remote RSS/Atom.

## Built-in feed URLs

| URL | What it is |
| --- | --- |
| `/feed/` or `/feed/rss2/` | RSS 2.0 of posts (the default). |
| `/feed/atom/` | Atom 1.0 of posts. |
| `/feed/rdf/` | RDF (RSS 1.0). |
| `/feed/rss/` | RSS 0.92. |
| `/comments/feed/` | RSS 2.0 of all comments. |
| `/?p=<id>&feed=rss2` or `/post-name/feed/` | Per-post comments feed. |
| `/author/<slug>/feed/` | Author archive feed. |
| `/category/<slug>/feed/` | Category archive feed. |
| `/tag/<slug>/feed/` | Tag archive feed. |
| `/feed/<custom-name>/` | Custom feed (see below). |

The default feed type is set in Settings → Reading. Override programmatically:

```php
add_filter( 'default_feed', fn() => 'atom' );
```

## Customizing what goes into the default feeds

The feed templates (`feed-rss2.php`, `feed-atom.php`, etc.) call standard loop functions but with feed-aware helpers (`the_title_rss`, `the_content_feed`, `the_excerpt_rss`). Filter them to modify output:

```php
// Append a footer to every feed item:
add_filter( 'the_content_feed', function ( $content, $feed_type ) {
    $content .= "\n\n— Read more at " . get_permalink();
    return $content;
}, 10, 2 );

// Change feed item title:
add_filter( 'the_title_rss', fn( $title ) => '[Blog] ' . $title );

// Filter what queries appear in the main posts feed:
add_action( 'pre_get_posts', function ( WP_Query $q ) {
    if ( $q->is_feed() && $q->is_main_query() ) {
        $q->set( 'post_type', array( 'post', 'announcement' ) );
        $q->set( 'posts_per_rss', 20 );
    }
} );
```

The `posts_per_rss` option (Settings → Reading) controls item count.

## Adding a custom feed type

```php
add_action( 'init', function () {
    add_feed( 'json', 'myplugin_render_json_feed' );    // Now /feed/json/ works.
    // Remember to flush rewrite rules on plugin activation.
} );

function myplugin_render_json_feed() {
    $posts = get_posts( array( 'posts_per_page' => 20 ) );
    header( 'Content-Type: application/json; charset=' . get_option( 'blog_charset' ) );
    echo wp_json_encode( array(
        'version' => 'https://jsonfeed.org/version/1.1',
        'title'   => get_bloginfo( 'name' ),
        'home_page_url' => home_url(),
        'feed_url'      => home_url( '/feed/json/' ),
        'items'   => array_map( function ( $p ) {
            return array(
                'id'             => (string) $p->ID,
                'url'            => get_permalink( $p ),
                'title'          => get_the_title( $p ),
                'content_html'   => apply_filters( 'the_content', $p->post_content ),
                'date_published' => mysql2date( DATE_ATOM, $p->post_date_gmt, false ),
            );
        }, $posts ),
    ) );
}
```

Flush rewrite rules on activation so the `/feed/json/` URL maps to your callback.

## Disabling feeds

Useful for sites that don't syndicate (private intranets, single-page sites):

```php
function myplugin_disable_feeds() {
    wp_die( __( 'No feed available, please visit the homepage.', 'mytheme' ) );
}
add_action( 'do_feed',      'myplugin_disable_feeds', 1 );
add_action( 'do_feed_rdf',  'myplugin_disable_feeds', 1 );
add_action( 'do_feed_rss',  'myplugin_disable_feeds', 1 );
add_action( 'do_feed_rss2', 'myplugin_disable_feeds', 1 );
add_action( 'do_feed_atom', 'myplugin_disable_feeds', 1 );

// Also remove the <link> tags from <head>:
remove_action( 'wp_head', 'feed_links',       2 );
remove_action( 'wp_head', 'feed_links_extra', 3 );
```

## Consuming feeds with fetch_feed()

WordPress bundles SimplePie for parsing remote feeds:

```php
// fetch_feed lives in wp-includes/feed.php and is not autoloaded — pull it in:
include_once ABSPATH . WPINC . '/feed.php';

$feed = fetch_feed( 'https://wordpress.org/news/feed/' );

if ( is_wp_error( $feed ) ) {
    return $feed;
}

$max_items   = $feed->get_item_quantity( 5 );
$feed_items  = $feed->get_items( 0, $max_items );

foreach ( $feed_items as $item ) {
    /** @var SimplePie_Item $item */
    echo '<h3><a href="' . esc_url( $item->get_permalink() ) . '">' . esc_html( $item->get_title() ) . '</a></h3>';
    echo '<p>' . esc_html( $item->get_date( 'F j, Y' ) ) . '</p>';
    echo wp_kses_post( $item->get_description() );
}
```

`fetch_feed()` caches responses via `WP_Feed_Cache_Transient` — by default 12 hours, controllable via the `wp_feed_cache_transient_lifetime` filter:

```php
add_filter( 'wp_feed_cache_transient_lifetime', fn() => HOUR_IN_SECONDS );
```

The transient lifetime is independent of the feed's own TTL; for high-traffic embeds, set a short cache and a long HTTP timeout.

To force a refresh, delete the transient or pass `$force_feed = true` (not exposed via `fetch_feed`, but you can construct a `SimplePie` instance directly).

## Where feed templates live

The `/feed/` URL resolves to `do_feed()` in `wp-includes/functions.php`, which `include`s one of these from `wp-includes/`:

- `feed-rss2.php` — RSS 2.0 (default).
- `feed-atom.php` — Atom.
- `feed-rdf.php` — RDF.
- `feed-rss.php` — RSS 0.92.
- `feed-rss2-comments.php` — Comments-only RSS.
- `feed-atom-comments.php` — Comments-only Atom.

A theme can override any of these by placing a same-named file in its directory.

## Where to look in this codebase

- `wp-includes/feed.php` — function API: `fetch_feed`, `get_default_feed`, `feed_content_type`, `the_content_feed`, `the_title_rss`, `rss_enclosure`, `atom_enclosure`, `do_feed_*`.
- `wp-includes/feed-rss2.php`, `feed-atom.php`, `feed-rdf.php` — the feed templates.
- `wp-includes/class-feed.php` — `WP_Feed_Cache` (bridge from SimplePie to WP_Cache).
- `wp-includes/class-wp-feed-cache-transient.php` — transient-backed feed cache.
- `wp-includes/class-wp-simplepie-file.php` — WP_HTTP-based HTTP layer for SimplePie.
- `wp-includes/SimplePie/` — the vendored SimplePie library.
- `wp-includes/atomlib.php` — Atom parsing helpers used by the XML-RPC server.

## Common pitfalls

- Adding a custom feed via `add_feed` and not flushing rewrite rules — `/feed/json/` 404s.
- Modifying feeds via `the_content` filter directly — this also affects post pages. Use `the_content_feed` so the change is feed-only.
- Caching `fetch_feed` results aggressively and serving stale data hours after the source changed. Tune via `wp_feed_cache_transient_lifetime`.
- Forgetting that the comments feed (`/comments/feed/`) is separate. Disabling only the posts feed leaves comment syndication open.
- Using `posts_per_page` in a feed query — the right knob is `posts_per_rss`. WordPress will use `posts_per_rss` regardless.
- Outputting HTML in a JSON feed callback without setting the correct `Content-Type` header.
- Treating SimplePie items' content as safe HTML. Always `wp_kses_post()` or stricter — remote feeds are untrusted.
