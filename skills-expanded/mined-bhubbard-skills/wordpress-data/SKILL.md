---
name: wordpress-data
description: Querying and manipulating WordPress data — posts, users, terms, options, transients, post/user/term/comment meta, and direct database access via $wpdb. Use when you need to write WP_Query / WP_User_Query / WP_Term_Query / WP_Comment_Query, work with the Options API, set up transients for caching, register or read custom meta, run raw SQL safely via wpdb's prepare() method, or build queries that join custom tables.
---

# WordPress Data & Queries

WordPress stores almost everything in a handful of MySQL tables: `wp_posts` (and `wp_postmeta`), `wp_terms` / `wp_term_taxonomy` / `wp_term_relationships` / `wp_termmeta`, `wp_users` / `wp_usermeta`, `wp_comments` / `wp_commentmeta`, `wp_options`. Almost all data access goes through query classes that wrap these tables.

## Read the right way: use the API, not raw SQL

If you can answer the question with a query class, do that — it triggers caching, hooks, and security checks. Drop to `$wpdb` only when there's no alternative.

## WP_Query — posts

```php
$q = new WP_Query( array(
    'post_type'      => 'book',
    'post_status'    => 'publish',
    'posts_per_page' => 20,
    'orderby'        => 'date',
    'order'          => 'DESC',
    'no_found_rows'  => true,      // Skip SQL_CALC_FOUND_ROWS when you don't need pagination totals.
    'update_post_meta_cache' => false,    // If you won't read meta.
    'update_post_term_cache' => false,    // If you won't read terms.
) );

if ( $q->have_posts() ) {
    while ( $q->have_posts() ) {
        $q->the_post();
        the_title();
    }
    wp_reset_postdata();           // Restore the global $post.
}
```

In the **main loop** (i.e., the query WP runs automatically), use `have_posts()` / `the_post()` without instantiating WP_Query. To filter the main query, hook `pre_get_posts`:

```php
add_action( 'pre_get_posts', function ( WP_Query $q ) {
    if ( is_admin() || ! $q->is_main_query() ) { return; }
    if ( $q->is_post_type_archive( 'book' ) ) {
        $q->set( 'posts_per_page', 50 );
    }
} );
```

### Tax queries

```php
'tax_query' => array(
    'relation' => 'AND',
    array(
        'taxonomy' => 'genre',
        'field'    => 'slug',
        'terms'    => array( 'sci-fi', 'fantasy' ),
    ),
    array(
        'taxonomy' => 'post_tag',
        'field'    => 'term_id',
        'terms'    => array( 42, 99 ),
        'operator' => 'NOT IN',
    ),
),
```

### Meta queries

Meta queries are slow — they join `wp_postmeta` once per clause. Avoid them when you can; if you can't, index your `meta_key`.

```php
'meta_query' => array(
    'relation' => 'AND',
    'price_clause' => array(
        'key'     => 'price',
        'value'   => 10,
        'type'    => 'NUMERIC',
        'compare' => '>=',
    ),
    array(
        'key'     => 'in_stock',
        'value'   => '1',
        'compare' => '=',
    ),
),
'orderby' => array( 'price_clause' => 'ASC', 'date' => 'DESC' ),
```

Named clauses (`'price_clause' => array(...)`) let you reference them in `orderby`.

### Date queries

```php
'date_query' => array(
    array(
        'after'     => '2025-01-01',
        'before'    => '2025-12-31',
        'inclusive' => true,
    ),
),
```

### Performance flags worth knowing

- `no_found_rows => true` — saves a second query just for counting. Use when you don't need pagination.
- `update_post_meta_cache => false`, `update_post_term_cache => false` — skip prefetching meta/terms when you only need the post objects.
- `fields => 'ids'` — return just post IDs, much smaller.
- `posts_per_page => -1` is **unbounded**. Never use on user-influenced queries.

## WP_User_Query

```php
$users = new WP_User_Query( array(
    'role'        => 'editor',
    'orderby'     => 'registered',
    'order'       => 'DESC',
    'number'      => 50,
    'meta_query'  => array(
        array( 'key' => 'opted_in', 'value' => '1' ),
    ),
    'fields'      => array( 'ID', 'user_email' ),
) );

foreach ( $users->get_results() as $user ) {
    // $user is a stdClass with the requested fields, or WP_User if fields is 'all'.
}
```

## WP_Term_Query and WP_Comment_Query

```php
$terms = get_terms( array(
    'taxonomy'   => 'genre',
    'hide_empty' => false,
    'parent'     => 0,                        // Only top-level.
    'meta_key'   => 'featured',
    'meta_value' => '1',
) );

$comments = get_comments( array(
    'post_id' => 42,
    'status'  => 'approve',
    'type'    => 'comment',
    'number'  => 10,
) );
```

## Options API

For sitewide settings. Backed by `wp_options`. Autoloaded options are loaded on every page request, so be careful.

```php
add_option(    'my_setting', 'default', '', 'no' );   // 'no' = don't autoload.
update_option( 'my_setting', $new_value );
$val = get_option( 'my_setting', 'fallback' );
delete_option( 'my_setting' );

// Multiple at once (more efficient — single primed cache):
$vals = get_options( array( 'siteurl', 'home', 'blogname' ) );

// Toggle autoload after the fact:
wp_set_option_autoload( 'my_setting', 'no' );          // Or 'yes'.
```

**Autoload rule of thumb:** if it's read on every request (a setting, a cached configuration), autoload yes. If it's only read in a specific admin page or scheduled task, autoload no. Large values (>1MB) should never autoload.

## Transients — short-lived cache

Use transients for anything you compute but want to keep cheap. Stored in `wp_options` by default, but if an object cache is installed (Redis, Memcached) they go there transparently.

```php
$key = 'mysite_top_posts';
$data = get_transient( $key );
if ( false === $data ) {
    $data = expensive_computation();
    set_transient( $key, $data, HOUR_IN_SECONDS );
}

delete_transient( $key );

// Network-wide variant in multisite:
set_site_transient( $key, $data, DAY_IN_SECONDS );
```

Time constants you can use: `MINUTE_IN_SECONDS`, `HOUR_IN_SECONDS`, `DAY_IN_SECONDS`, `WEEK_IN_SECONDS`, `MONTH_IN_SECONDS`, `YEAR_IN_SECONDS`.

Don't rely on a transient existing — they can be evicted at any time. The `false === $val` recompute path must be cheap to fall back to.

## Meta APIs (post, user, term, comment)

```php
add_post_meta(    $post_id, 'rating', 5 );
update_post_meta( $post_id, 'rating', 5 );        // Creates if missing.
$rating = get_post_meta( $post_id, 'rating', true );    // true = single value.
$all    = get_post_meta( $post_id, 'rating', false );   // All values for the key.
delete_post_meta( $post_id, 'rating' );

// Same shape exists for users, terms, comments:
update_user_meta( $user_id, 'last_login', time() );
get_term_meta(    $term_id, 'icon', true );
update_comment_meta( $comment_id, 'flagged', '1' );
```

### Register meta so it shows up in REST

```php
register_post_meta( 'book', 'rating', array(
    'type'              => 'integer',
    'description'       => 'Book rating, 1-5',
    'single'            => true,
    'default'           => 0,
    'show_in_rest'      => true,
    'sanitize_callback' => 'absint',
    'auth_callback'     => fn( $allowed, $key, $post_id ) => current_user_can( 'edit_post', $post_id ),
) );
```

Without `show_in_rest`, meta is invisible to Gutenberg and the REST API.

## $wpdb — direct SQL

`$wpdb` is the global WordPress database wrapper. Reach for it when you need joins, aggregations, or a custom table.

```php
global $wpdb;

// ALWAYS use prepare() for any variable — it placeholders and escapes.
$rows = $wpdb->get_results( $wpdb->prepare(
    "SELECT ID, post_title FROM {$wpdb->posts}
     WHERE post_type = %s AND post_status = %s AND post_date > %s
     ORDER BY post_date DESC LIMIT %d",
    'book', 'publish', '2025-01-01', 50
) );

// Placeholders: %s string, %d integer, %f float, %i identifier (table/column name, since WP 6.2).
// NEVER concatenate user input. NEVER call prepare() with no placeholders (it warns).

// Helpers:
$count   = $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->posts}" );
$one_row = $wpdb->get_row( $wpdb->prepare( "SELECT * FROM {$wpdb->posts} WHERE ID = %d", $id ) );
$ids_col = $wpdb->get_col( "SELECT ID FROM {$wpdb->posts}" );

// Mutating helpers — safer than raw INSERT/UPDATE/DELETE:
$wpdb->insert( $wpdb->posts, array(
    'post_title'  => $title,
    'post_status' => 'draft',
), array( '%s', '%s' ) );           // Formats.
$inserted_id = $wpdb->insert_id;

$wpdb->update( $wpdb->postmeta,
    array( 'meta_value' => $new ),  // SET
    array( 'meta_id'    => 42 ),    // WHERE
    array( '%s' ),                   // SET formats
    array( '%d' )                    // WHERE formats
);

$wpdb->delete( $wpdb->postmeta, array( 'meta_id' => 42 ), array( '%d' ) );

// Read last query when debugging:
echo $wpdb->last_query;
echo $wpdb->last_error;

// Transactions: $wpdb->query("START TRANSACTION"), then COMMIT/ROLLBACK. InnoDB only.
```

### Table prefix and the magic properties

`$wpdb->posts`, `$wpdb->postmeta`, `$wpdb->users`, `$wpdb->usermeta`, `$wpdb->terms`, `$wpdb->term_taxonomy`, `$wpdb->term_relationships`, `$wpdb->termmeta`, `$wpdb->comments`, `$wpdb->commentmeta`, `$wpdb->options`. Always interpolate these — never hardcode `wp_posts` because the site might use a different prefix.

For custom tables: `$wpdb->prefix . 'my_table'`.

### Creating a custom table

```php
register_activation_hook( __FILE__, function () {
    global $wpdb;
    $charset_collate = $wpdb->get_charset_collate();
    $table = $wpdb->prefix . 'myplugin_events';

    $sql = "CREATE TABLE $table (
        id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT(20) UNSIGNED NOT NULL,
        event_type VARCHAR(50) NOT NULL,
        payload LONGTEXT,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY  (id),
        KEY user_id (user_id),
        KEY event_type (event_type)
    ) $charset_collate;";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );          // dbDelta is forgiving and idempotent — call it on every version bump.
} );
```

`dbDelta` has strict syntax quirks: two spaces after `PRIMARY KEY`, uppercase keywords, no backticks around table names, columns one per line.

## Object cache and groups

`wp_cache_*` functions write to the runtime cache. Without a persistent cache drop-in (`wp-content/object-cache.php` from Redis/Memcached plugin), they're per-request only.

```php
$val = wp_cache_get( 'my_key', 'my_group' );
if ( false === $val ) {
    $val = compute();
    wp_cache_set( 'my_key', $val, 'my_group', HOUR_IN_SECONDS );
}
wp_cache_delete( 'my_key', 'my_group' );
```

Use distinct **groups** so your cache doesn't collide with core's, and so you can flush a logical chunk.

## High-level helpers worth knowing

```php
$post     = get_post( $id );                   // Single post.
$id_arr   = get_posts( array(...) );           // Like WP_Query but returns an array.
$user     = get_user_by( 'email', 'a@b.com' );
$current  = wp_get_current_user();
$terms    = wp_get_post_terms( $post_id, 'genre' );
$inserted = wp_insert_post( array( 'post_title' => '...', 'post_status' => 'publish' ), true );  // true = return WP_Error on fail.
$ok       = wp_update_post( array( 'ID' => $id, 'post_status' => 'draft' ) );
$ok       = wp_delete_post( $id, $force = true );
$attach   = wp_insert_attachment( ... );
```

## Where to look in this codebase

- `wp-includes/class-wp-query.php` — WP_Query, parse_query, get_posts.
- `wp-includes/class-wp-user-query.php` — user queries.
- `wp-includes/class-wp-term-query.php`, `class-wp-tax-query.php`, `class-wp-meta-query.php`, `class-wp-date-query.php` — composable query helpers.
- `wp-includes/class-wpdb.php` — $wpdb, prepare, dbDelta-related plumbing.
- `wp-includes/option.php` — options + transients.
- `wp-includes/meta.php` — generic meta API; `register_meta`.
- `wp-includes/cache.php` — wp_cache_* runtime cache.
- `wp-includes/post.php` — `wp_insert_post`, `get_posts`, `register_post_type`.

## Common pitfalls

- Forgetting `wp_reset_postdata()` after a custom WP_Query loop — the global `$post` stays at the last item.
- Using `posts_per_page => -1` on a user-influenced query and OOMing.
- Calling `$wpdb->query( "... $user_input ..." )` instead of `prepare`. This is a SQL injection.
- Storing huge arrays as autoloaded options — every request loads them.
- Relying on a transient existing. Always implement the recompute path.
- `meta_query` against an unindexed `meta_key` on a large `postmeta` table — full table scan.
- Forgetting `'fields' => 'ids'` when you only need IDs and ending up hydrating thousands of WP_Post objects.
