---
name: mirror-site
description: When you need comprehensive information from a website or documentation site but don't know its structure (so web-search snippets or guessing URLs aren't enough), download the whole site (same domain) into the sandbox and grep/analyze it locally. Use for "read the docs", auditing a site, or gathering everything a site says about a topic.
---

# Download a site, then analyze it locally

When the user wants thorough coverage of a site/docs and you can't tell what
pages exist, don't guess URLs or rely on a few search snippets — mirror the site
into the sandbox and search the real content.

## Procedure

1. **Find the entry point** (the docs root / the relevant section URL). If unsure,
   quickly check the sitemap or robots first:
   ```bash
   curl -s https://example.com/sitemap.xml | head -40
   curl -s https://example.com/robots.txt
   ```

2. **Download the site** with the bundled crawler (same-domain BFS, seeds from
   sitemap, respects robots.txt, saves readable text per page):
   ```bash
   pip install -q requests beautifulsoup4 lxml   # usually already installed
   python scripts/crawl.py https://example.com/docs --out site --max-pages 200 --max-depth 3
   ```
   - It writes `site/pages/0001.txt …` (each = URL + title + readable text) and a
     manifest `site/index.tsv` (file → url → title).
   - Tune `--max-pages` / `--max-depth` to the size you need; add `--same-host` to
     stay on the exact host, `--keep-html` to also save raw HTML.

3. **Explore the download** with tree-structured search (load the
   **explore-codebase** skill) — never read every file:
   ```bash
   grep -rn -i "the thing you care about" site/pages | head -40
   sed -n '1,5p' site/index.tsv          # see what was captured
   ```
   Find the right page(s), then read just the relevant lines.

4. **Answer from what you actually read**, citing the source URLs (from the page's
   `URL:` header or `index.tsv`).

## Notes

- Keep it bounded: a reasonable `--max-pages`, the default delay, and same-domain
  scope keep the crawl fast and focused (and avoid timing out the sandbox).
- The crawler already honors robots.txt and seeds from the sitemap.
- The crawl folder lives in the conversation sandbox and is auto-deleted later.
- If you only need one or two known pages, just `curl` them instead of crawling.
