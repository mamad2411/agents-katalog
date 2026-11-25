---
name: wordpress-oembed
description: WordPress oEmbed — auto-embedding remote content (YouTube, Twitter/X, Vimeo, etc.) from URLs pasted into posts, and exposing the site's own posts as oEmbed providers. Use when registering a new oEmbed provider, implementing a custom embed handler for a regex pattern, debugging why a URL is embedding (or not), styling embed iframes, or clearing the oEmbed cache stored in post meta.
---

# WordPress oEmbed and Auto-Embeds

oEmbed is a discovery protocol: paste a URL on its own line, WordPress hits the provider's oEmbed endpoint, gets back an HTML snippet (usually an iframe), and renders it inline. Twitter/X, YouTube, Vimeo, Spotify, SoundCloud, TikTok, and dozens of others are wired in by default.

WordPress also acts as an oEmbed *provider* — every public post can be embedded on other sites that consume oEmbed.

## Two-sided system

- **Consumer**: WordPress fetching oEmbed data for URLs in post content. Implemented by `WP_oEmbed` + `WP_Embed`.
- **Provider**: WordPress responding to oEmbed requests for its own URLs. Implemented by `WP_oEmbed_Controller` (REST controller).

## Registering a custom oEmbed provider

If a service publishes an oEmbed endpoint that WordPress doesn't know about:

```php
add_action( 'init', function () {
    wp_oembed_add_provider(
        'https://example.com/posts/*',                       // URL pattern (or regex).
        'https://example.com/oembed/1.0/embed',              // The provider's oEmbed endpoint.
        false                                                 // false = pattern is a wildcard, true = regex.
    );
} );
```

Then any URL matching the pattern dropped on its own line in a post becomes an embed. WordPress fetches `https://example.com/oembed/1.0/embed?url=<URL>&format=json`, expects oEmbed JSON back, and renders the `html` field.

To remove a provider (e.g., to disable Twitter embeds for privacy):

```php
wp_oembed_remove_provider( '#https?://(www\.)?twitter\.com/.+/status(es)?/.+#i' );
```

## Embed handlers — for URLs that don't have an oEmbed endpoint

If a service has predictable URLs but no oEmbed (or oEmbed gives bad HTML), register an embed *handler* instead. Handlers are regex+callback pairs:

```php
add_action( 'init', function () {
    wp_embed_register_handler(
        'gist',                                                       // Handler ID.
        '#https?://gist\.github\.com/([^/]+)/([a-f0-9]+)$#i',          // Regex.
        function ( $matches, $attr, $url, $rawattr ) {
            $user = esc_attr( $matches[1] );
            $id   = esc_attr( $matches[2] );
            return sprintf(
                '<script src="https://gist.github.com/%s/%s.js"></script>',
                $user, $id
            );
        }
    );
} );
```

Handlers run *before* the oEmbed providers, so they can override built-ins. Use them when you need 100% control over the output HTML.

## Fetching an oEmbed manually

```php
// Simple — return the HTML snippet or false:
$html = wp_oembed_get( 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' );

// With size constraints:
$html = wp_oembed_get( $url, array(
    'width'    => 800,
    'height'   => 450,
    'discover' => false,        // Skip auto-discovery on unknown URLs (faster, more predictable).
) );

// Low-level — get the full oEmbed response object:
$oembed = _wp_oembed_get_object();
$data = $oembed->fetch( $oembed->get_provider( $url ), $url, $args );
// $data->html, $data->type, $data->thumbnail_url, $data->width, $data->height, etc.
```

## The cache — stored in post meta

Embed HTML is cached **per-post** as post meta with auto-generated keys (`_oembed_<hash>` and a `_oembed_time_<hash>` companion). This means:

- The same embed in two different posts is fetched twice.
- Updating a post can invalidate stale embeds (controlled by `WP_Embed::cache_oembed`).
- To force a refresh, delete the `_oembed_*` meta keys on the post.

```php
delete_post_meta_by_key( '_oembed_<hash>' );    // Or iterate post meta.

// Tune cache TTL (default 24 hours):
add_filter( 'oembed_ttl', fn( $ttl, $url, $attr, $post_ID ) => DAY_IN_SECONDS * 7, 10, 4 );
```

For non-post-context fetches (`wp_oembed_get` outside a post), results are cached as transients with the `oembed_` prefix.

## WordPress as a provider — disabling

By default, WordPress exposes `/wp-json/oembed/1.0/embed` for every public post. To disable entirely (privacy, performance):

```php
// Don't auto-add the <link rel="alternate" type="application/json+oembed"> tags:
remove_action( 'wp_head', 'wp_oembed_add_discovery_links' );

// Don't expose the host JS (only loads when embedded elsewhere):
remove_action( 'wp_head', 'wp_oembed_add_host_js' );

// Block the REST route entirely:
add_filter( 'rest_endpoints', function ( $endpoints ) {
    unset( $endpoints['/oembed/1.0/embed'] );
    unset( $endpoints['/oembed/1.0/proxy'] );
    return $endpoints;
} );

// Disable client-side iframe resizing/auto-discovery script:
remove_action( 'rest_api_init', 'wp_oembed_register_route' );
```

## Customizing what gets embedded *from* posts

Modify the data returned when other sites embed yours:

```php
add_filter( 'oembed_response_data', function ( $data, $post, $width, $height ) {
    $data['author_name'] = get_user_meta( $post->post_author, 'display_name', true );
    $data['custom']      = get_post_meta( $post->ID, 'featured_attr', true );
    return $data;
}, 10, 4 );

// Modify the iframe markup served when someone embeds:
add_filter( 'embed_html', fn( $html, $post ) => $html, 10, 2 );
```

## The `[embed]` shortcode and auto-embeds

In post content, both work:

```
[embed width="800"]https://www.youtube.com/watch?v=...[/embed]
```

Or just paste the URL on its own line — `WP_Embed::autoembed()` finds bare URLs and converts them.

## Where to look in this codebase

- `wp-includes/embed.php` — function API: `wp_oembed_get`, `wp_oembed_add_provider`, `wp_oembed_remove_provider`, `wp_embed_register_handler`, the default YouTube/audio/video handlers.
- `wp-includes/class-wp-oembed.php` — `WP_oEmbed`. The provider list, fetching, parsing JSON/XML responses.
- `wp-includes/class-wp-embed.php` — `WP_Embed`. The autoembed pipeline that runs against post content.
- `wp-includes/class-wp-oembed-controller.php` — REST controller for WordPress-as-provider (`/wp-json/oembed/1.0/embed`, `/proxy`).
- `wp-includes/embed-template.php` — the template used when serving an embeddable post (`type=link` style).

## Common pitfalls

- The URL must be on its own line for auto-embed to work. Inline URLs are left as text.
- New provider added but old posts still show the bare URL — flush the post's oEmbed cache by re-saving it, or delete its `_oembed_*` meta.
- Calling `wp_oembed_get()` early in the request lifecycle, before `init`. Provider registration happens on `init`; calling earlier may miss custom providers.
- Forgetting that custom providers need their pattern matched exactly. URL trailing slashes, www/non-www, and http/https all matter. Test with the actual URL the user pastes.
- Adding a handler with `wp_embed_register_handler` and expecting it to run for an oEmbed-recognized URL — handlers run first, but only if the regex matches. If the regex misses, oEmbed takes over.
- Using oEmbed for a URL the provider doesn't actually serve oEmbed for. WordPress falls back to no embed, leaving the bare URL. Verify with the provider's docs or hit their `/oembed?url=...` endpoint.
