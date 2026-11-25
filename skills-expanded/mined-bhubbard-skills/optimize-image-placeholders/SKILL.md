---
name: optimize-image-placeholders
description: Debug and optimize the display of dominant color image placeholders in WordPress.
---

# Optimize Image Placeholders

## Overview
This skill assists in verifying the dominant color placeholder background that appears while an image is loading.

## Guidelines
1. Check the HTML source of frontend images to verify the dominant color is injected as a background style on the image container.
2. Ensure the background color matches the general hue of the uploaded image.
3. If placeholders are grey or default colors, verify that the color detection logic during the media library upload succeeded.
4. Confirm that the image mime types (e.g., AVIF, WebP) are supported by the color detection algorithm.
