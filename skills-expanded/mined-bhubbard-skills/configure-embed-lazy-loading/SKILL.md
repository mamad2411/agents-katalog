---
name: configure-embed-lazy-loading
description: Optimize lazy loading and preload links for embeds using the Embed Optimizer WordPress plugin.
---

# Configure Embed Lazy Loading

## Overview
This skill helps optimize lazy loading and dns-prefetching for embeds (YouTube, TikTok, Twitter) in WordPress.

## Guidelines
1. Embed Optimizer avoids lazy loading for embeds in the initial viewport if Optimization Detective is installed and has collected URL metrics.
2. Verify that above-the-fold embeds have `dns-prefetch` links for known resources (e.g., `https://i.ytimg.com`).
3. For below-the-fold embeds, ensure `loading="lazy"` is correctly applied to `IFRAME` embeds.
4. For `SCRIPT`-based embeds, verify the Intersection Observer correctly injects the script tag before the `FIGURE` container enters the viewport.
