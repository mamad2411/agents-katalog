---
name: perflab-image-placeholders
description: Guidance on the Image Placeholders (Dominant Color) module. Use when addressing issues with background colors on loading images or analyzing dominant color generation.
---

# Performance Lab: Image Placeholders

Formerly known as "Dominant Color", the Image Placeholders module calculates the dominant color of an image when it is uploaded and applies it as a background color while the image is loading on the frontend.

## How it works
When an image is uploaded, WordPress's image editor analyzes the pixels to find the most prominent color. It saves this as a hex code in the image metadata. On the frontend, it injects a small inline CSS style to the `<img>` tag (e.g., `background-color: #f45b69`).

## Disabling for Specific Images
If a user wants to disable the background color for a specific image (e.g., a transparent PNG where the background color bleeds through incorrectly), you can filter the output:
```php
// Example: disabling dominant color if image has transparency
// The module attempts to handle transparency, but edge cases exist.
```

## Performance Impact
This improves Perceived Performance and helps stabilize layout shifts during Largest Contentful Paint (LCP) rendering.
