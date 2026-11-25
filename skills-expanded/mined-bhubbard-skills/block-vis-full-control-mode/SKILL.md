---
name: block-vis-full-control-mode
description: Enabling Full Control Mode. Use when visibility settings are missing from inner blocks or specific third-party blocks.
---

# Block Visibility: Full Control Mode

By default, the Block Visibility plugin only attaches visibility controls to "top-level" or standard blocks. Inner child blocks (like an individual `Column` within a `Columns` block, or an individual `List Item` within a `List`) do not have visibility settings by default to reduce UI clutter.

## Full Control Mode 🚀
If a user needs to conditionally hide a specific inner block (e.g., hiding one specific column on mobile while leaving the others visible), they must enable **Full Control Mode** in the plugin settings.

- **What it does**: Bypasses the default restrictions and injects the Visibility panel into the block inspector for *every single block* registered on the site, including child blocks and highly specialized third-party blocks.
- **Side effects**: Can make the block inspector feel slightly more cluttered on complex nested layouts.
