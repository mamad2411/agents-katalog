---
name: perflab-speculative-loading
description: Guidance on Speculative Loading (Speculation Rules). Use when configuring prerendering or prefetching to achieve instant page navigations.
---

# Performance Lab: Speculative Loading

This module implements the Speculation Rules API to dramatically speed up user navigation by prefetching or prerendering pages before the user clicks a link.

## Prefetch vs. Prerender
- **Prefetch**: Downloads the HTML document in the background. Fast, but the browser still has to render the CSS/JS.
- **Prerender**: Downloads and actually renders the page invisibly in the background. Clicking the link is instantaneous, but it uses more CPU and bandwidth.

## Configuration
The plugin allows administrators to define which URLs should be speculatively loaded (e.g., all internal links on hover, or specific important pages).

## Potential Issues
Prerendering can cause issues if a page triggers an action merely by being loaded (e.g., an analytics hit or a one-time nonce validation). Developers should ensure that side-effect actions only occur upon user interaction, not page load.
