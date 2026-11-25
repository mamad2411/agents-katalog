---
name: perflab-image-prioritizer
description: Guidance on the Image Prioritizer module. Use when troubleshooting LCP (Largest Contentful Paint) optimization or addressing fetchpriority attributes.
---

# Performance Lab: Image Prioritizer

The Image Prioritizer analyzes the page to identify the Largest Contentful Paint (LCP) image and automatically applies the `fetchpriority="high"` attribute to it.

## Dependency
This module requires **Optimization Detective** to analyze the frontend and determine which image is actually the LCP element.

## How it helps CWV
By adding `fetchpriority="high"`, the browser knows to request this image earlier in the network waterfall, significantly improving the LCP score in Core Web Vitals.

## Conflicts
If a theme or another performance plugin (like WP Rocket or Perfmatters) is also trying to inject `fetchpriority="high"`, it may result in duplicate attributes or the wrong image being prioritized. Ensure only one plugin handles LCP prioritization.
