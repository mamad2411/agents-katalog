---
name: perflab-responsive-images
description: Guidance on the Enhanced Responsive Images feature in Performance Lab. Use when addressing inaccurate `sizes` attributes or layout shifts caused by responsive images.
---

# Performance Lab: Enhanced Responsive Images

This module aims to improve upon WordPress core's native responsive images by generating more accurate `sizes` attributes for `<img>` tags.

## Inaccurate Sizes
Native WordPress tries to guess the `sizes` attribute based on the image's layout width, but it's often inaccurate for complex layouts (e.g., CSS Grid). This module provides a more accurate calculation, helping the browser download the perfectly sized image earlier.

## Developer Hooks
If a theme developer wants to override the calculated sizes for a specific image block, they can hook into standard `wp_calculate_image_sizes` filters, though this module usually handles it automatically.
