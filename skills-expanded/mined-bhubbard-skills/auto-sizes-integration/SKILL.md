---
name: auto-sizes-integration
description: Ensure sizes="auto" is applied correctly for lazy-loaded images.
---

# Auto Sizes Integration

## Overview
This skill covers debugging the `sizes="auto"` implementation for lazy-loaded images, a feature introduced by the Enhanced Responsive Images plugin and merged into WP 6.7.

## Guidelines
1. Verify `sizes="auto"` is correctly appended or replaces existing sizes when `loading="lazy"` is present.
2. If `sizes="auto"` is missing, check if it's being properly handled by the HTML Tag Processor.
3. Note that as of WP 6.7+, this behavior may be handled natively by WordPress core. If using older WP versions, ensure the plugin correctly prevents duplicate `sizes="auto"` keywords.
4. If testing in conjunction with Image Prioritizer, check that sizes logic successfully delegates or integrates without conflict.
