---
name: debug-bfcache-failures
description: Troubleshoot scenarios where bfcache might be failing, such as plugins emitting Cache-Control no-store.
---

# Debug BFCache Failures

Even with the Instant Back/Forward plugin active, some pages may not be eligible for bfcache.

## Troubleshooting Steps

1. Open Chrome DevTools.
2. Go to the **Application** tab.
3. In the left sidebar, click on **Back/forward cache**.
4. Test navigating away from and back to a page.
5. Look for failure reasons such as:
   - `MainResourceHasCacheControlNoStore`: Another plugin or theme might be sending `Cache-Control: no-store` (e.g., WooCommerce cart/checkout pages, or a server-level configuration like Pantheon's MU plugin).
   - `JsNetworkRequestReceivedCacheControlNoStoreResource`: JavaScript on the page makes a request to an endpoint with `no-store` (like `admin-ajax.php` or the REST API).
   - `CacheControlNoStoreCookieModified`: JavaScript on the page modifies cookies.

### Fixing Server/Plugin conflicts
If a plugin or host (like Pantheon) is forcing `no-store`, you may need to override it. For example, for Pantheon:

```php
add_filter( 'pantheon_skip_cache_control', static function (): bool {
    return is_admin() || is_user_logged_in();
} );
```
