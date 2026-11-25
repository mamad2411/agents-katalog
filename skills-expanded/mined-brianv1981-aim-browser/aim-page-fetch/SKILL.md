---
name: aim-page-fetch
description: >
  Open a URL in headed Chromium and extract title, meta, main text, and links.
  Markdown + JSON. Use when page content must be live, not invented.
---

# aim-page-fetch

```bash
npm run page-fetch -- "https://example.com"
npm run page-fetch -- --screenshot /tmp/page.png --url "https://example.com"
```

**Defaults:** minimized, stop after session (`--keep-open` to chain).

**JSON fields:** `title`, `url`, `canonical`, `description`, `meta`, `mainText`, `links[]`, `rawLength`, optional `screenshot`, optional `cached`.

Parse markdown, then `---JSON---`. Prefer this over guessing page text.
