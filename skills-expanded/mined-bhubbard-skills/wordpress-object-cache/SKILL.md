---
name: wordpress-object-cache
description: WordPress Object Cache (wp_cache_*) and persistent cache drop-ins. Use when caching arbitrary values within or across requests, picking between transients and the object cache, building a custom cache layer for an expensive query, installing Redis/Memcached as a persistent backend, working with cache groups (including global groups in multisite), or debugging stale data. Covers the runtime-only default behavior vs object-cache.php drop-ins.
---

# WordPress Object Cache (wp_cache_*)

`wp_cache_*` is WordPress's in-memory key/value cache. By default it's **per-request only** — nothing persists between page loads. Drop a `wp-content/object-cache.php` file (from a Redis or Memcached plugin) and the same API transparently becomes a persistent cache.

Internally it's an instance of `WP_Object_Cache` stored on `$GLOBALS['wp_object_cache']`. Without a drop-in, it's a PHP array; with a drop-in, it's a thin client wrapper.

## The API

```php
// Get / set / delete
$val = wp_cache_get( $key, $group = '', $force = false, &$found = null );
       wp_cache_set( $key, $data, $group = '', $expire = 0 );    // $expire in seconds, 0 = no TTL.
       wp_cache_add( $key, $data, $group = '', $expire = 0 );    // Only if not set; returns false if it was.
       wp_cache_replace( $key, $data, $group = '', $expire = 0 );// Only if set.
       wp_cache_delete( $key, $group = '' );

// Multi
wp_cache_set_multiple( array $data, $group = '', $expire = 0 );
wp_cache_get_multiple( array $keys, $group = '', $force = false );
wp_cache_delete_multiple( array $keys, $group = '' );
wp_cache_add_multiple( array $data, $group = '', $expire = 0 );

// Atomics (rarely needed, persistent backends mostly)
wp_cache_incr( $key, $offset = 1, $group = '' );
wp_cache_decr( $key, $offset = 1, $group = '' );

// Flushing
wp_cache_flush();              // Nuke EVERYTHING. Use sparingly.
wp_cache_flush_runtime();      // Drop in-process arrays without touching persistent backend.
wp_cache_flush_group( $group );// Drop one group (supported by some backends; check wp_cache_supports).

// Capability detection
wp_cache_supports( 'add_multiple' );           // 'flush_group', 'flush_runtime', etc.
```

The canonical lazy-cache pattern:

```php
function myplugin_get_top_authors() {
    $cached = wp_cache_get( 'top_authors', 'myplugin' );
    if ( false !== $cached ) {
        return $cached;
    }
    $authors = expensive_aggregation_query();
    wp_cache_set( 'top_authors', $authors, 'myplugin', 10 * MINUTE_IN_SECONDS );
    return $authors;
}
```

A `false` return from `wp_cache_get` is **ambiguous** — it could mean "miss" or "the cached value is literally `false`." Use the `&$found` byref param when you need to disambiguate:

```php
$found = false;
$val   = wp_cache_get( 'key', 'group', false, $found );
if ( $found ) { /* genuine hit */ }
```

## Cache groups — namespace your keys

Always pass a group. It namespaces the key (so two plugins can both use `'config'` without collision) and lets persistent backends bulk-flush a group:

```php
wp_cache_set( 'top_posts', $data, 'myplugin' );
// Persistent-backed: key becomes 'myplugin:top_posts'.
```

Group names are conventionally a plugin slug.

### Global vs blog-local groups (multisite)

In multisite, the cache is sub-site-scoped by default — a `wp_cache_set( 'k', $v, 'g' )` on site 1 doesn't collide with the same key on site 2. To make a group **global** (shared across sites):

```php
wp_cache_add_global_groups( array( 'myplugin_global' ) );
// Do this on plugins_loaded or earlier.
```

WordPress already registers `users`, `userlogins`, `usermeta`, `useremail`, etc. as global because those tables are network-wide.

### Non-persistent groups

Some data shouldn't outlive the request even with a persistent backend — typically because it's cheap to recompute or invalidates unpredictably. Mark the group:

```php
wp_cache_add_non_persistent_groups( array( 'myplugin_runtime' ) );
```

Now `wp_cache_set( 'k', $v, 'myplugin_runtime' )` always stays in-process.

## Object cache vs transients — which one?

Both have the "cache or compute" shape, but:

| Question | Object cache (`wp_cache_*`) | Transient (`get_transient`) |
| --- | --- | --- |
| Persists without a drop-in? | No | Yes (in `wp_options`) |
| Persists with Redis drop-in? | Yes | Yes (also in Redis) |
| Can flush a single group? | Sometimes | No |
| Cache hit cost on cache-miss path | Fast | Slower (DB lookup) |
| Survives a Redis restart? | No | No (transients also live in cache when a drop-in is installed) |
| Best for | High-frequency cached values | Less frequent cached values that need persistence even without a drop-in |

Practical rule: in plugin code targeting unknown hosts, **prefer transients for caches that absolutely must survive the request** (cache-warmer results, fetched-from-API data, etc.), and use `wp_cache_*` for everything that's frequently accessed within a single request (avoiding repeat DB queries).

When a persistent object cache is installed, transients transparently store *in the object cache* instead of `wp_options`. So with a Redis drop-in, transients and `wp_cache_*` ultimately go to the same place — but transients give you the "without drop-in" safety net.

## Installing a persistent backend

Drop-ins live at `wp-content/object-cache.php`. Major options:

- [Redis Object Cache](https://wordpress.org/plugins/redis-cache/) — activate, then enable the drop-in from the plugin's admin.
- [W3 Total Cache](https://wordpress.org/plugins/w3-total-cache/) — bundled object-cache.php (Redis, Memcached).
- [Memcached Object Cache](https://wordpress.org/plugins/memcached/) — Memcached.
- Hosted: Cloudways, WP Engine, Pantheon, Pressable all install one for you.

Verify it's active:

```php
wp_using_ext_object_cache();    // bool. true = persistent backend present.
```

Or via WP-CLI: `wp cli info` shows the loaded object cache, and `wp cache type` returns the backend name.

## Cache invalidation patterns

The hardest part. A few common patterns:

```php
// 1. Versioned key — bump the version to invalidate all derived caches.
$version = wp_cache_get( 'myplugin_version', 'myplugin' );
if ( false === $version ) {
    $version = (string) microtime( true );
    wp_cache_set( 'myplugin_version', $version, 'myplugin' );
}
$key = "top_authors:{$version}";
// To invalidate everything: wp_cache_delete( 'myplugin_version', 'myplugin' );

// 2. Hook-based invalidation — when an underlying object changes, drop the cache.
add_action( 'save_post', function ( $post_id ) {
    wp_cache_delete( 'top_authors', 'myplugin' );
} );

// 3. Last-modified timestamp in the key.
$timestamp = get_option( 'myplugin_last_modified', 0 );
$key = "top_authors:{$timestamp}";
```

## Where to look in this codebase

- `wp-includes/cache.php` — the public function API: `wp_cache_get`, `wp_cache_set`, `wp_cache_delete`, `wp_cache_flush`, groups helpers.
- `wp-includes/class-wp-object-cache.php` — the default in-memory implementation. Read this to understand what a drop-in needs to implement.
- `wp-includes/cache-compat.php` — backwards-compat shims (legacy global functions).
- Drop-in location: `wp-content/object-cache.php` (not in this repo by default — added by Redis/Memcached plugins).

## Common pitfalls

- Treating `false` as a miss when the cached value can legitimately be `false`. Use the `&$found` parameter.
- Forgetting the group, so two plugins collide on `'config'`. Always pass a group.
- Caching huge structures (megabytes) — slow to serialize, slow to deserialize, can exceed Memcached's 1MB item limit. Cache the small derived view, not the raw input.
- Caching user-specific data without including user ID in the key. One user sees another user's cached page.
- Using `wp_cache_set` with no expiration on a persistent backend and forgetting about it. Set a TTL even when "forever" feels right — protects against backends without LRU eviction.
- Calling `wp_cache_flush()` to invalidate one plugin's cache. It wipes everything globally — including other plugins, transients, and WP core's own caches.
- Assuming `wp_cache_*` is persistent. Without a drop-in, it isn't. Always design for the "this is empty next request" case.
- Storing references / closures / unserializable objects. The backend serializes; you'll get warnings or silent loss.
