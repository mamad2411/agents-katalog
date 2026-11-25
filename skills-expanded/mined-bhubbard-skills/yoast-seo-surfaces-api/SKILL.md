---
name: yoast-seo-surfaces-api
description: "Interacting with the Surfaces API (PHP) to retrieve Yoast SEO data efficiently within WordPress."
---

# Yoast SEO Surfaces API

The Surfaces API is the official, stable PHP API for interacting with Yoast SEO data. It is the recommended way to retrieve SEO metadata for posts, terms, and the site, avoiding direct database queries or unstable internal functions.

## Reference
[Surfaces API Documentation](https://developer.yoast.com/customization/apis/surfaces-api/)

## Usage

Access the Surfaces API via the `YoastSEO()` global function.

```php
$surfaces = YoastSEO();
```

### 1. The Meta Surface
The Meta surface is used to retrieve SEO metadata for specific objects.

**Get Meta for a Post:**
```php
$meta = YoastSEO()->meta->for_post( $post_id );

// Retrieve the SEO title
$title = $meta->title;

// Retrieve the Schema graph
$schema = $meta->schema;

// Retrieve social tags
$og_title = $meta->open_graph_title;
```

**Get Meta for a Term:**
```php
$meta = YoastSEO()->meta->for_term( $term_id );
```

**Get Meta for the Homepage:**
```php
$meta = YoastSEO()->meta->for_home_page();
```

### 2. The Helpers Surface
The Helpers surface provides utility functions.

```php
// Check if a specific plugin module is enabled
$is_enabled = YoastSEO()->helpers->options->get( 'breadcrumbs-enable' );

// Get the canonical URL for the current page
$canonical = YoastSEO()->helpers->current_page->get_canonical_url();
```

## Best Practices
- **Never** use internal `WPSEO_*` classes or direct `get_post_meta()` calls to retrieve Yoast SEO data, as the internal architecture changes frequently. The `YoastSEO()` Surfaces API is guaranteed to remain stable.
- The `$meta` object returned by `for_post()` pulls data from Yoast's optimized Indexables tables, making it extremely fast.
