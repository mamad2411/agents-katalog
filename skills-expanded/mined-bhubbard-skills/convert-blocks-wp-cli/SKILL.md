---
name: convert-blocks-wp-cli
description: Managing bulk block conversions via WP-CLI. Use when a client requires thousands of legacy posts to be converted to Gutenberg blocks simultaneously.
---

# Convert to Blocks: WP-CLI Bulk Migration

If a site requires mass conversion (e.g., thousands of posts) and the "on-the-fly" manual method is too slow, you can use WP-CLI to trigger a bulk migration.

## The CLI Command
```bash
wp convert-to-blocks start
```

## How the Bulk Migration Executes
Unlike standard WP-CLI commands that run entirely in the terminal, this command leverages an iterative, browser-based execution model. 
- It essentially opens posts in the browser sequentially, clicks the update button to parse the blocks, and moves to the next post.
- Because it relies on this iterative processing, it can be slow on very large databases (e.g., 8,000+ posts) and may require active monitoring to reload the tab if the process hangs due to server spikes or unusual post content.
