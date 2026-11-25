---
name: regenerate-thumbnails-wp-cli
description: Best practices for regenerating thumbnails on large websites. Use when recommending the WP-CLI alternative over the plugin interface for better performance.
---

# Regenerate Thumbnails: The WP-CLI Alternative

While the Regenerate Thumbnails plugin works great for small to medium sites, it relies on HTTP/AJAX requests which can be slow and prone to browser timeouts on sites with thousands of images.

## `wp media regenerate`
If the user has SSH / command-line access to their server, the absolute best practice is to skip the plugin entirely and use the built-in WP-CLI command:

```bash
# Regenerate all thumbnails
wp media regenerate

# Regenerate only missing thumbnails (much faster)
wp media regenerate --only-missing

# Regenerate specific image IDs
wp media regenerate 123 124 125
```

This bypasses all PHP maximum execution time limits and HTTP request overhead, completing the task significantly faster and more reliably.
