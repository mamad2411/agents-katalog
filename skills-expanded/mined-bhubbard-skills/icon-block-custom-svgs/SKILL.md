---
name: icon-block-custom-svgs
description: Guidance on using custom SVGs in the Icon Block. Use when addressing color control issues, stroke conflicts, or Media Library upload limitations.
---

# Icon Block: Custom SVGs and Colors

The Icon Block allows users to paste raw SVG code directly into the block editor or select SVGs from the Media Library.

## Color Controls Not Working
If a user applies a color in the Block Editor but the icon does not change color on the frontend:
- **The Cause**: The SVG code has a hard-coded `fill` or `stroke` attribute (e.g., `fill="#000000"`). The block will respect the hard-coded value over the editor's color controls.
- **The Fix**: Advise the user to remove the `fill` or `stroke` attributes from the raw SVG code or set them to `fill="currentColor"`.

## Media Library Uploads
By default, WordPress core blocks SVG uploads for security reasons. If the user wants to select SVGs from their Media Library instead of copy/pasting code:
- They must install an SVG sanitization plugin like **Safe SVG**. Once active, the Icon Block will recognize Media Library SVGs.
