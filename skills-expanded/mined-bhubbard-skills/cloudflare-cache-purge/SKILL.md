---
name: cloudflare-cache-purge
description: Managing Cloudflare Automatic Cache Purging. Use when content isn't updating on the frontend or configuring custom purge rules.
---

# Cloudflare Cache Purging

The Cloudflare plugin automatically clears the edge cache when a post is published, edited, or deleted, or when the site appearance is updated.

## Custom Purge Rules
Developers can hook into the purging logic to add custom URLs to be purged when an update occurs.

```php
add_filter( 'cloudflare_purge_by_url', function( $urls, $post_id ) {
    // Add a custom URL to the list of URLs purged when this post is updated
    $urls[] = home_url( '/my-custom-endpoint/' );
    return $urls;
}, 10, 2 );
```

## Troubleshooting
If cache purging fails silently:
- Ensure the API Token has the "Cache Purge" permission.
- Check if the site is using an exotic page builder that does not trigger standard WordPress `transition_post_status` hooks.
- Remember that the plugin automatically ignores purging feed URLs unless overridden.
