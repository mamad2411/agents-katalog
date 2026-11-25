---
name: perflab-modern-images
description: Guidance on the Modern Image Formats module. Use when addressing WebP/AVIF generation or issues with image formats upon upload.
---

# Performance Lab: Modern Image Formats

Formerly known as "WebP Uploads", this module handles the automatic conversion of uploaded JPEG images into modern, highly compressed formats like WebP or AVIF.

## Format Selection
By default, the plugin will attempt to generate WebP. If AVIF is supported by the server's image processing library (ImageMagick or GD), it may generate AVIF, which offers even better compression.

## Fallback Generation
When a WebP/AVIF is generated, the original JPEG is kept as a fallback. The frontend will serve the modern format, but the original is retained for compatibility with older browsers or systems that don't support modern formats.

## Controlling Output
You can use the `webp_uploads_prefer_smaller_image_file` filter to dictate whether WordPress should always prefer the smaller file size between the generated WebP and the original JPEG.
