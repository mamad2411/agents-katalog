---
name: pagefind
description: Pagefind standards — static build-time search index, indexing attributes, UI vs JS API, build wiring. Load when working with Pagefind.
user-invocable: false
stack: search/pagefind
paths:
  - "**/pagefind*"
  - "**/*{search,Search}*.{astro,tsx,jsx,vue,svelte}"
---

Full standards in [pagefind.md](pagefind.md). Always-on summary:

- **Pagefind is static.** It indexes the built HTML after the site build. No server and no API keys.
- **Wire it into the build**: `astro build && pagefind --site dist` (or the `astro-pagefind` integration). Never run it by hand.
- **Index content, not chrome.** Put `data-pagefind-body` on the main content; add `data-pagefind-ignore` to nav, footer and related-links blocks.
- **Filters and metadata.** Use `data-pagefind-filter` and `data-pagefind-meta` rather than parsing text.
- **Load the UI lazily** on the search page or when the search box opens.
- **Never** commit the generated `pagefind/` folder.
