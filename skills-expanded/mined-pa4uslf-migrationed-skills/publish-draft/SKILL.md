---
name: publish-draft
description: Use when the user wants to publish a prepared article draft from this repository to WordPress. This skill validates that metadata exists and then calls the WordPress publisher module.
---

# Publish Draft

Publish a prepared article to WordPress through the existing publisher module.

## Preconditions

Before publishing, verify:

- The article file exists
- The draft has usable metadata
- WordPress credentials are configured
- The article has already passed the optimize flow

## Command

```bash
.venv/bin/python data_sources/modules/wordpress_publisher.py <article-file>
```

If the user wants a page or custom post type, use the publisher module's `--type` flag.

## Codex-Specific Notes

- The Codex version uses the same publisher module as the original project.
- Publishing should be explicit and user-directed. Do not publish automatically after writing.
