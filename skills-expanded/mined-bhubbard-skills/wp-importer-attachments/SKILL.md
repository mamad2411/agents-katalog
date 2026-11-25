---
name: wp-importer-attachments
description: Troubleshooting issues with importing media and attachments. Use when images are missing, fail to download, or have incorrect URLs after migration.
---

# WordPress Importer: Attachments & Media

Importing media is often the most fragile part of the WordPress import process because it relies on the new server making outbound HTTP requests to the old server.

## Missing Images
If images fail to import:
1. **Source Server Accessibility**: Ensure the old site is still live, publicly accessible, and not behind a password/firewall (like Cloudflare Under Attack mode). The new server must be able to download the images via HTTP.
2. **Download Checkbox**: Ensure the user checked the "Download and import file attachments" box during the import setup step.

## URL Rewriting
The importer automatically attempts to rewrite old site URLs inside post content and block attributes (like `wp:image` blocks or Cover blocks) to the new site's URL. 
- If URLs aren't rewriting properly, ensure the XML export file accurately defines the `wp:base_site_url`.

## Incomplete Downloads
If the server hits its execution limit while downloading a large image, the image might be saved partially or corrupted. Checking the PHP error logs for `cURL` or `allow_url_fopen` timeout errors is the best diagnostic step.
