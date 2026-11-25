---
name: optimize-lcp-media
description: Debug and optimize Largest Contentful Paint (LCP) using the Image Prioritizer plugin.
---

# Optimize LCP Media

## Overview
This skill helps verify and troubleshoot LCP optimizations applied by the Image Prioritizer plugin to images, videos, and background images.

## Guidelines
1. Verify Optimization Detective is installed and collecting URL metrics across both mobile and desktop viewports.
2. Check if the identified LCP element receives `fetchpriority="high"` and an HTTP `Link: <url>; rel=preload` header.
3. For `PICTURE` elements, ensure the first `<source>` with a type attribute gets preloaded (art-direction is not currently supported).
4. For LCP videos, ensure `preload="auto"` is set and the poster image receives prioritization.
5. Ensure `fetchpriority="high"` is only applied when the element is the LCP across all responsive breakpoints.
