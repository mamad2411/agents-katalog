---
name: perflab-performant-translations
description: Guidance on the Performant Translations module. Use when troubleshooting localization performance or missing translated strings.
---

# Performance Lab: Performant Translations

This module optimizes how WordPress loads translation files (`.mo` and `.php` files).

## The Performance Issue
Loading translations in WordPress can be notoriously slow, especially on sites with many plugins and a non-English default language, due to the parsing of heavy `.mo` files.

## The Solution
This plugin converts `.mo` translation files into lightweight PHP files, which can be cached by OPCache, resulting in significantly faster translation lookups and overall page load times for localized sites.

## Troubleshooting
If translations are missing or incorrect after activating:
- Ensure the site has write permissions to the `/wp-content/languages/` directory so the plugin can generate the `.php` files.
- You may need to clear the object cache to force the regeneration of the translation structures.
