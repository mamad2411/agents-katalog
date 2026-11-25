---
name: regenerate-thumbnails-troubleshooting
description: Troubleshooting issues with the Regenerate Thumbnails plugin. Use when dealing with AJAX errors, timeouts, or unsupported file formats like SVGs.
---

# Regenerate Thumbnails: Troubleshooting

## Skipping Correctly Sized Images
By default, the plugin includes a checkbox to "Skip regenerating existing correctly sized thumbnails". 
- If a client complains that regeneration was "too fast" and didn't fix a specific blurry image, ensure they uncheck this box to force WordPress to recreate the file from the original upload.

## Unsupported Formats
- **SVGs**: The plugin intentionally skips SVG files. SVGs are vector graphics that scale infinitely and do not require bitmap thumbnails.
- **PDFs**: Depending on the server's ImageMagick configuration, PDF thumbnail generation may fail.

## AJAX / Timeout Errors
If the progress bar halts with a red error:
1. The original uploaded image might be too large for the server's PHP memory limit to process (e.g., trying to resize a 15MB, 6000x4000px raw photo).
2. The server's `max_execution_time` is killing the PHP process.
- **Fix**: Advise the user to process fewer images at a time via the Media Library bulk actions, or switch to WP-CLI (`wp media regenerate`).
