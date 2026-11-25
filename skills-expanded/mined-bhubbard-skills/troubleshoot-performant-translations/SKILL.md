---
name: troubleshoot-performant-translations
description: Fix issues with translation files not being regenerated or OPcache invalidation for the Performant Translations plugin.
---

# Troubleshoot Performant Translations

Performant Translations converts `.mo` files into `.php` files (with the `.mo.php` extension) and leverages OPcache to speed up localized WordPress sites.

## Common Issues

1. **Translations not updating after a change:**
   If you updated a plugin or edited a `.mo` file directly (e.g., via Loco Translate), but the frontend still shows old strings:
   - Ensure your PHP environment is configured to allow OPcache invalidation (`opcache_invalidate()`).
   - The plugin attempts to automatically regenerate the `.mo.php` file when Loco Translate updates `.mo` files, but permission issues in `wp-content/languages` can prevent writing the new file.

2. **File Permission Issues:**
   Check the permissions of `wp-content/languages` and its subdirectories. The web server user must have write access for the plugin to generate the `.php` files.

3. **Symlinks:**
   If your translation files are accessed via symlinks, ensure the paths are correctly resolved by PHP, as this can sometimes prevent the plugin from successfully saving the converted files.

4. **Debugging Query Monitor:**
   Performant Translations integrates with Query Monitor. If you're investigating performance issues, check the Query Monitor panels for details on translation load times and whether `.php` translation files were successfully loaded.
