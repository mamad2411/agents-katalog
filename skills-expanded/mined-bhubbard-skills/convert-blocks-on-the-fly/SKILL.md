---
name: convert-blocks-on-the-fly
description: Understanding the Convert to Blocks parsing mechanism. Use when migrating older WordPress sites to Gutenberg safely without risking database corruption.
---

# Convert to Blocks: On-The-Fly Parsing

When migrating a legacy WordPress site from the Classic Editor to the Block Editor (Gutenberg), mass database conversions can be incredibly risky. Convert to Blocks solves this via "on-the-fly" parsing.

## How it Works
1. When an editor opens an old post, the plugin intercepts the content and automatically parses it into Block Editor markup in the browser.
2. If the user navigates away, a warning appears because the structure has changed.
3. The new block structure is **only** saved to the database when the user explicitly clicks "Update".

This strategy isolates risk: you are only altering the database values for content that a human is actively reviewing and verifying.

## Limitations
- By default, it will **not** convert custom shortcodes or custom blocks into native blocks.
- Nested/Inner blocks require Gutenberg version 10.9.0 or higher.
