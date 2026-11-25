---
name: regenerate-thumbnails-usage
description: Guidance on using the Regenerate Thumbnails plugin. Use when changing themes or registering new image sizes requires updating old media library uploads.
---

# Regenerate Thumbnails: Usage & Cleanup

When you switch WordPress themes or add a new `add_image_size()` to your functions file, WordPress does *not* automatically resize images that were already uploaded to the Media Library.

## When to use Regenerate Thumbnails
- **Theme Changes**: The new theme relies on a 1200x600 featured image, but the old theme used 800x400.
- **New Layouts**: You created a new custom image size for a specific slider or grid layout.

## Freeing up Server Space
When regenerating, the plugin includes a checkbox option to "Delete thumbnail files for old unregistered sizes".
- If you recently moved away from a heavy theme that generated 15 different thumbnail sizes per upload, checking this box during regeneration will purge all those old, unused files from the `wp-content/uploads/` directory, saving massive amounts of disk space.
