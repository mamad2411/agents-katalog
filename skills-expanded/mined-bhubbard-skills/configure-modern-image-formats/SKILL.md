---
name: configure-modern-image-formats
description: Set up or modify fallback behavior and select between AVIF and WebP output formats for the Modern Image Formats plugin.
---

# Configure Modern Image Formats

The Modern Image Formats (formerly WebP Uploads) plugin generates WebP or AVIF images for media uploads.

## Usage

1. By default, the plugin generates AVIF if supported by the hosting server, falling back to WebP.
2. Go to **Settings > Media** to change the desired output format when both are available.
3. **Fallback Images**: By default, only the original uploaded file remains as JPEG/PNG, while all generated sub-sizes are WebP/AVIF. 
   - To keep JPEG/PNG sub-sizes as fallbacks, enable the "Output fallback images" (or "Generate JPEG files in addition to WebP") checkbox in **Settings > Media**.

## Technical Details

- The plugin replaces `<img ...>` with a `<picture>` element containing `<source>` elements for the modern formats.
- If images are not generating, ensure they are being uploaded directly to the Media Library, and that the WebP/AVIF version isn't actually larger in file size than the original JPEG.
