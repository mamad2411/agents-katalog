---
name: wp-importer-memory
description: Guidance on resolving Out of Memory and timeout errors during WordPress imports. Use when a user encounters a blank screen or fatal error importing a large XML file.
---

# WordPress Importer: Memory & Timeout Issues

The WordPress Importer parses large XML files, which can consume significant server memory and processing time.

## Fatal Error: Allowed Memory Size Exhausted
If the server's PHP `memory_limit` is too low, the import will fail abruptly, often resulting in a blank screen or a 500 error.
- **Solution 1**: Increase the PHP `memory_limit` in `php.ini` or `wp-config.php` (e.g., `define( 'WP_MEMORY_LIMIT', '256M' );`).
- **Solution 2**: Split the WXR (XML) file into smaller, more manageable pieces using a WXR splitter tool before importing.

## Maximum Execution Time
If the import script times out (e.g., "Maximum execution time of 30 seconds exceeded"):
- **Solution**: Increase `max_execution_time` in `php.ini`. If on shared hosting, the user may need to ask their host to temporarily lift the limit or run the import via WP-CLI.

## WP-CLI Alternative
For extremely large sites, the best approach is bypassing the web server entirely and using WP-CLI:
```bash
wp import export.xml --authors=create
```
