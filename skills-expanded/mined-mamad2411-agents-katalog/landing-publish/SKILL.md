---
name: landing-publish
description: Use when the user wants to publish a landing page draft to WordPress as a page, typically after it has passed the landing audit.
---

# Landing Publish

Publish a landing page draft after it has passed audit.

## Preconditions

- Landing page score is acceptable
- No critical issues remain
- Required metadata is present
- WordPress credentials are configured

## Command

Use the existing publisher module with page type semantics:

```bash
.venv/bin/python data_sources/modules/wordpress_publisher.py landing-pages/<page-file>.md --type page
```

## Notes

- For PPC pages, set noindex manually in the CMS if your current publisher flow does not expose that flag yet.
- Review the generated draft in WordPress before publishing live.
