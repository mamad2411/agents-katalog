---
name: block-vis-screen-size
description: Guidance on the Screen Size visibility control. Use when troubleshooting why hidden blocks are still present in the DOM or customizing CSS breakpoints.
---

# Block Visibility: Screen Size Controls

The Screen Size control allows users to hide or show blocks based on the visitor's device (Desktop, Tablet, Mobile).

## Server-Side vs. Client-Side (CSS)
Unlike almost all other visibility controls in this plugin (which evaluate on the server and completely remove the block from the HTML output if hidden), the **Screen Size control relies on CSS**.
- If a block is hidden on Mobile, the HTML *is still rendered and sent to the browser*, but it is visually hidden using CSS `display: none;`.
- Users should not rely on Screen Size controls to hide sensitive data or reduce the page weight of large DOM nodes, as the data is still transmitted to the client.

## Custom Breakpoints
By default, the plugin provides standard breakpoints for Desktop, Tablet, and Mobile. Developers can customize up to 4 different breakpoints in the plugin settings to align the Screen Size controls perfectly with the active theme's media queries.
