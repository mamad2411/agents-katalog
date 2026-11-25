---
name: perflab-embed-optimizer
description: Guidance on using the Embed Optimizer from the Performance Lab plugin. Use when troubleshooting oEmbed performance or resolving issues with embedded content not loading.
---

# Performance Lab: Embed Optimizer

The Embed Optimizer improves the performance of oEmbeds (like YouTube or Twitter embeds) by delaying the loading of the heavy iframe until the user interacts with it or scrolls to it.

## How it works
It relies on the **Optimization Detective** dependency to analyze the page and determine which blocks/embeds need optimization. It replaces the iframe with a lightweight placeholder and a "Click to load" or auto-load mechanism on scroll.

## Troubleshooting
If an embed is broken or missing:
1. Ensure **Optimization Detective** is active, as Embed Optimizer requires it to function.
2. Certain themes with aggressive lazy-loading (e.g., using third-party lazy load plugins) might conflict with the Embed Optimizer. Disable third-party lazy loading for iframes to see if the issue resolves.
