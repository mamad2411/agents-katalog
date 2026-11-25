---
name: wordpress-sitemaps
description: WordPress core XML sitemaps (since 5.5) — wp-sitemap.xml and the sitemap registry. Use when adding a custom sitemap provider for a CPT or other object, disabling core sitemaps, customizing the URL list output, changing the per-sitemap URL count, or troubleshooting sitemap indexing. Covers WP_Sitemaps_Provider, wp_sitemaps_add_provider, wp_sitemaps_max_urls, and the wp-sitemap.xml index.
---

# WordPress Core XML Sitemaps

Since WP 5.5, WordPress ships XML sitemaps natively at `/wp-sitemap.xml`. The default providers cover **posts**, **pages**, **users**, and **taxonomies**. Custom post types and taxonomies registered with `public => true` and `has_archive => true` are picked up automatically.

The system is pluggable: write a `WP_Sitemaps_Provider` subclass for any object type, register it, and a new sitemap appears in the index.

## What the URLs look like

- `/wp-sitemap.xml` — the index, links to all sub-sitemaps.
- `/wp-sitemap-posts-post-1.xml` — posts, page 1.
- `/wp-sitemap-posts-page-1.xml` — pages, page 1.
- `/wp-sitemap-taxonomies-category-1.xml`, `/wp-sitemap-taxonomies-post_tag-1.xml`, etc.
- `/wp-sitemap-users-1.xml` — authors who have published posts.

Each sub-sitemap holds up to 2,000 URLs by default (`wp_sitemaps_max_urls` filter).

## Disabling core sitemaps

If you use Yoast/RankMath/AIOSEO, you almost certainly want to disable core's:

```php
add_filter( 'wp_sitemaps_enabled', '__return_false' );

// Or remove just a specific provider:
add_filter( 'wp_sitemaps_add_provider', function ( $provider, $name ) {
    if ( 'users' === $name ) {
        return false;
    }
    return $provider;
}, 10, 2 );
```

## Limiting which post types and taxonomies are included

```php
// Skip a specific post type:
add_filter( 'wp_sitemaps_post_types', function ( $post_types ) {
    unset( $post_types['attachment'] );
    return $post_types;
} );

add_filter( 'wp_sitemaps_taxonomies', function ( $taxonomies ) {
    unset( $taxonomies['post_format'] );
    return $taxonomies;
} );

// Exclude specific items from a query:
add_filter( 'wp_sitemaps_posts_query_args', function ( $args, $post_type ) {
    if ( 'post' === $post_type ) {
        $args['post__not_in'] = array( 42, 99 );    // Hide these IDs.
    }
    return $args;
}, 10, 2 );

// Same for taxonomy terms and users:
add_filter( 'wp_sitemaps_taxonomies_query_args', fn( $args, $tax ) => $args, 10, 2 );
add_filter( 'wp_sitemaps_users_query_args',      fn( $args )      => $args, 10, 1 );
```

## Changing URL count per sitemap

Default is 2,000 URLs per page. Search engines accept up to 50,000:

```php
add_filter( 'wp_sitemaps_max_urls', function ( $max, $object_type ) {
    return 5000;
}, 10, 2 );
```

Smaller numbers mean more sub-sitemaps but each is faster to generate. Don't go too small — index lookup overhead adds up.

## Adding a custom sitemap provider

For something WordPress doesn't already index — e.g., a "products" external feed, an extra entity stored outside `wp_posts`:

```php
class MyPlugin_Products_Sitemap_Provider extends WP_Sitemaps_Provider {

    public function __construct() {
        $this->name        = 'products';        // Slug — used in the URL.
        $this->object_type = 'product';         // Logical object type.
    }

    /**
     * Returns the URL list for the requested page.
     *
     * @return array<int, array<string, mixed>> List of arrays each with `loc` (required), optional `lastmod`.
     */
    public function get_url_list( $page_num, $object_subtype = '' ) {
        $per_page = wp_sitemaps_get_max_urls( $this->object_type );
        $offset   = ( $page_num - 1 ) * $per_page;

        global $wpdb;
        $rows = $wpdb->get_results( $wpdb->prepare(
            "SELECT slug, updated_at FROM {$wpdb->prefix}myplugin_products
             ORDER BY id ASC LIMIT %d OFFSET %d",
            $per_page, $offset
        ) );

        return array_map( fn( $r ) => array(
            'loc'     => home_url( '/products/' . $r->slug . '/' ),
            'lastmod' => mysql2date( DATE_W3C, $r->updated_at, false ),
        ), $rows );
    }

    /**
     * Total number of pages needed to list all products.
     */
    public function get_max_num_pages( $object_subtype = '' ) {
        global $wpdb;
        $total = (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}myplugin_products" );
        $per_page = wp_sitemaps_get_max_urls( $this->object_type );
        return (int) ceil( $total / $per_page );
    }
}

add_filter( 'wp_sitemaps_add_provider', function ( $provider, $name ) {
    if ( 'products' === $name ) {
        return new MyPlugin_Products_Sitemap_Provider();
    }
    return $provider;
}, 10, 2 );

// Then register at the right time:
add_action( 'init', function () {
    wp_sitemaps_get_server()->registry->add_provider(
        'products',
        new MyPlugin_Products_Sitemap_Provider()
    );
} );
```

The two abstract methods (`get_url_list`, `get_max_num_pages`) are the contract. Subtypes (think: per-CPT, per-taxonomy) come from `get_object_subtypes()` if your provider has multiple — most don't.

## Subtypes — when one provider covers many object kinds

The built-in "posts" provider has subtypes `post` and `page` and any other public post type. The sub-sitemap URL includes the subtype: `/wp-sitemap-posts-post-1.xml`, `/wp-sitemap-posts-page-1.xml`.

If your provider has subtypes, override `get_object_subtypes()` to return an array of subtype slugs. The base class then calls `get_url_list( $page, $subtype )` for each.

## Customizing entries in the default sitemaps

Add or modify entry attributes (e.g., add `lastmod`):

```php
add_filter( 'wp_sitemaps_posts_entry', function ( $entry, WP_Post $post, $post_type ) {
    $entry['lastmod'] = mysql2date( DATE_W3C, $post->post_modified_gmt, false );
    return $entry;
}, 10, 3 );

add_filter( 'wp_sitemaps_taxonomies_entry', fn( $entry, $term, $tax ) => $entry, 10, 3 );
add_filter( 'wp_sitemaps_users_entry',      fn( $entry, $user )       => $entry, 10, 2 );

// Or the index entry (rarely needed):
add_filter( 'wp_sitemaps_index_entry', fn( $entry, $object_type, $object_subtype, $page ) => $entry, 10, 4 );
```

`lastmod` is the big one — WordPress doesn't emit it by default for posts even though it's helpful for crawlers.

## Robots.txt — automatic

Once the sitemap is enabled, `robots.txt` automatically gets `Sitemap: <url>` appended. To disable just the robots.txt addition (without disabling sitemaps):

```php
add_filter( 'wp_sitemaps_enabled', '__return_true' );
remove_action( 'robots_txt', 'wp_sitemaps_get_robots_txt', 10 );
```

## Where to look in this codebase

- `wp-includes/sitemaps.php` — function API: `wp_sitemaps_get_server`, `wp_get_sitemap_providers`, `wp_sitemaps_get_max_urls`, `get_sitemap_url`.
- `wp-includes/sitemaps/class-wp-sitemaps.php` — bootstrapper.
- `wp-includes/sitemaps/class-wp-sitemaps-registry.php` — `add_provider`, `get_providers`.
- `wp-includes/sitemaps/class-wp-sitemaps-provider.php` — abstract base class. **Read this for the contract.**
- `wp-includes/sitemaps/class-wp-sitemaps-renderer.php` — XML output.
- `wp-includes/sitemaps/class-wp-sitemaps-stylesheet.php` — XSL stylesheet for human-friendly viewing.
- `wp-includes/sitemaps/providers/` — built-in providers (`class-wp-sitemaps-posts.php`, `taxonomies.php`, `users.php`). Use these as templates.

## Common pitfalls

- Generating sitemap entries on every request without caching. Counts and URL lists should come from indexed queries.
- Returning more than the configured per-page count from `get_url_list`. Anything above `wp_sitemaps_get_max_urls()` is silently truncated.
- Forgetting to register the provider on `init` and wondering why `/wp-sitemap-products-1.xml` 404s.
- Mismatched `get_max_num_pages()` and actual data. The index will link to non-existent pages or miss real ones.
- Including private / draft / password-protected items. Filter your queries — sitemaps are public.
- Letting `attachment` post type appear in the sitemap. It usually shouldn't — filter it out.
- Trusting your `$_GET` parameters when implementing custom rendering. The server is hardened against this but your provider isn't automatically.
