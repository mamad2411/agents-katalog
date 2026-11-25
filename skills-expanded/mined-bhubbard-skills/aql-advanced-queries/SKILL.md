---
name: aql-advanced-queries
description: Utilizing advanced taxonomy and meta queries in the Advanced Query Loop block. Use when filtering by multiple taxonomies, custom post types, or ACF data.
---

# Advanced Query Loop: Complex Queries

The Advanced Query Loop block significantly extends the core block's capabilities for querying complex data.

## Multiple Post Types
You can query across multiple post types simultaneously (e.g., displaying Posts, Portfolios, and Case Studies in a single unified grid). Just select them from the "Post Types" dropdown.
*Note: Ensure custom post types have `public` and `show_in_rest` set to `true` to be available in the block.*

## Post Meta Queries & ACF
You can filter posts based on custom field values, seamlessly integrating with plugins like Advanced Custom Fields (ACF).
- Set multiple conditions using `AND`/`OR` logic.
- Use flexible comparison operators (`EXISTS`, `=`, `!=`, `>`, `<`).
- ACF fields will often auto-populate in the meta key dropdown for easier selection.

## Taxonomy Query Builder
Create sophisticated relationships by filtering posts against multiple categories, tags, or custom taxonomies at once.
