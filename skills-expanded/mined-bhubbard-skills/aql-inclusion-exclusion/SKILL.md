---
name: aql-inclusion-exclusion
description: Managing exact post inclusion and exclusion rules. Use when needing strict curation, hiding the current post, or showing only child pages.
---

# Advanced Query Loop: Inclusion & Exclusion

## Intelligent Post Exclusion
- **Exclude Current Post**: An essential toggle when adding a "Related Posts" or "More Articles" section at the bottom of a single post template. It prevents the post the user is currently reading from duplicating in the suggested grid.
- **Manual Exclusion**: Curate an exact list of Post IDs to strip out of the query results.

## Smart Post Inclusion
- **Manual Curation**: Select exact posts by title or ID to build a hand-picked layout.
- **Child Items Only**: A powerful feature for hierarchical post types (like Pages). This forces the query loop to only display the immediate children of the current page being viewed.
