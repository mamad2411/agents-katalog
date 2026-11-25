---
name: yoast-seo-metadata-api
description: "Interacting with the Metadata API (Indexables) for fetching and saving SEO data."
---

# Yoast SEO Metadata API

The Metadata API provides the infrastructure underlying the Surfaces API. It is built on "Indexables"—custom database tables that store all SEO metadata for posts, terms, users, and custom URLs in a flat, heavily optimized format.

## Reference
[Metadata API Documentation](https://developer.yoast.com/customization/apis/metadata-api/)

## Core Concepts

### Indexables
Yoast SEO 14.0 introduced Indexables. Instead of joining multiple meta tables on every page load to calculate SEO tags, Yoast calculates the data once when a post is saved and stores it in the `wp_yoast_indexable` table.

### Retrieving Data
For simply reading data, you should **always** use the Surfaces API (`YoastSEO()->meta->for_post()`). The Metadata API documentation is primarily for understanding the underlying architecture.

### Modifying Data Programmatically
If you need to programmatically update Yoast SEO data for a post (e.g., during a bulk import), you should still update the standard WordPress post meta (e.g., `_yoast_wpseo_title`). Yoast will detect the change and automatically rebuild the Indexable in the background or on the next page load.

Example of programmatic update:
```php
update_post_meta( $post_id, '_yoast_wpseo_title', 'My Custom Title %%sep%% %%sitename%%' );
```
*Note: After updating the post meta directly, the Indexable for that post might be outdated until it is rebuilt.*

## Best Practices
- Do not write direct SQL queries to `wp_yoast_indexable`. Treat it as a read-only cache maintained by the plugin.
- If a site's SEO data is out of sync, recommend that the user run the "SEO Data Optimization" tool under Yoast SEO -> Tools, which clears and rebuilds the Indexables tables.
