---
name: troubleshoot-dominant-color-extraction
description: Fix issues with dominant color extraction in the WordPress Media Library.
---

# Troubleshoot Dominant Color Extraction

## Overview
This skill helps debug issues that arise when the Image Placeholders plugin attempts to extract the dominant color from uploaded images.

## Guidelines
1. Ensure the server has the necessary image processing libraries installed (e.g., GD or Imagick) and they are functioning properly.
2. Test uploading different file formats (JPEG, PNG, WebP, AVIF) to isolate mime-type specific parsing errors.
3. If partial transparency is present in PNGs/WebPs, check if Imagick or GD is correctly identifying the non-transparent dominant color.
4. Verify that the plugin is only attempting to get the dominant color for valid image mime types, ignoring non-images.
