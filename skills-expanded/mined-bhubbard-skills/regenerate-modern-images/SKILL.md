---
name: regenerate-modern-images
description: Generate WebP or AVIF versions for existing pre-uploaded images using WP-CLI or plugins.
---

# Regenerate Modern Images

The Modern Image Formats plugin only generates modern formats (AVIF/WebP) for *newly uploaded* images. Existing images in the Media Library must be regenerated.

## Instructions

To regenerate existing images and create modern formats for them, you have two options:

### 1. Using WP-CLI
Run the following WP-CLI command on the server to regenerate all attachments:
```bash
wp media regenerate --yes
```

### 2. Using a Plugin
Install and activate a plugin like **Regenerate Thumbnails**.
1. Go to **Tools > Regenerate Thumbnails**.
2. Click the button to regenerate all thumbnails.

**Warning:** Generating images can be resource-intensive. Perform this during off-peak hours, and ensure you have a backup of your media library before proceeding.
