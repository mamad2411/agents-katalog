---
name: site-tooling
description: >
  Shared quality assurance, auditing, sitemap parsing, preview lifecycle, and review
  scraping tooling for Astro and modern web applications. Provides canonical implementations
  of with-preview.sh, a11y-scan.mjs, sitemap.mjs, list-sitemap-urls.mjs, and scrape-reviews.py.
---

# Site Tooling

Canonical repository of shared automation, testing, and scraping utilities for Astro and static/SSR web applications. Designed to eliminate script drift between client web properties (such as `calljacob-astro`, `bbdental-astro`, and others).

## Available Tools

The canonical scripts are located in `scripts/`:

### 1. `with-preview.sh`
- **Location**: `scripts/with-preview.sh`
- **Purpose**: Boots `astro preview` (or npm preview server) against the current `dist/` build, verifies the port isn't blocked by stale processes, polls until the server returns HTTP 200, executes the provided test command (e.g. `pa11y`, `unlighthouse`, integration tests), and guarantees teardown via exit/interrupt trap handlers.
- **Usage**:
  ```bash
  ./scripts/with-preview.sh npm run test:a11y
  PREVIEW_PORT=4322 ./scripts/with-preview.sh npx unlighthouse --site http://localhost:4322
  ```

### 2. `sitemap.mjs`
- **Location**: `scripts/lib/sitemap.mjs`
- **Purpose**: Reliably parses production build sitemaps (`dist/client/sitemap-0.xml`, `dist/sitemap-0.xml`, or custom `SITEMAP_PATH`) directly from disk. Extracts page paths using `new URL(loc).pathname` without hardcoding origins or requiring a live HTTP server.
- **Export**: `getSitemapPaths()` returning relative root paths (e.g. `['/services/', '/about/']`).

### 3. `list-sitemap-urls.mjs`
- **Location**: `scripts/list-sitemap-urls.mjs`
- **Purpose**: Streams all sitemap paths rewritten with `PREVIEW_ORIGIN` (default `http://localhost:4321`) to standard output for piping directly into CLI auditors (`xargs pa11y-ci`).
- **Usage**:
  ```bash
  node scripts/list-sitemap-urls.mjs | xargs npx pa11y-ci
  ```

### 4. `a11y-scan.mjs`
- **Location**: `scripts/a11y-scan.mjs`
- **Purpose**: Full dual-theme (Light Mode and Dark Mode) WCAG accessibility auditing using Puppeteer and Pa11y. Emulates `prefers-color-scheme: light` and `prefers-color-scheme: dark` media features per page, ensuring contrast and focus bugs in dark mode do not slip through standard CI.
- **Usage**:
  ```bash
  ./scripts/with-preview.sh node scripts/a11y-scan.mjs
  ```

### 5. `scrape-reviews.py`
- **Location**: `scripts/scrape-reviews.py`
- **Purpose**: Multi-source review scraper for Google Maps and Yelp using Playwright, featuring automated **Thematic Sentiment Analysis & Keyword Clustering**.
- **Capabilities**:
  - **Sentiment Polarity Scoring**: Scores each review from `-1.0` to `+1.0` blending rating polarity and text sentiment heuristics (with negation handling and intensifiers).
  - **Common Praises Extraction**: Clusters positive signals across canonical themes: `"painless"`, `"compassionate"`, `"fast settlement"`, `"responsive"`, `"knowledgeable"`, `"friendly staff"`, `"transparent"`, and `"highly recommend"`.
  - **Common Complaints / Red Flags**: Identifies risk factors across canonical themes: `"wait time"`, `"billing dispute"`, `"unresponsive"`, `"hidden fee"`, `"rushed"`, `"rude"`, `"overcharged"`, and `"cancelled appointment"`.
  - **Export Enrichment**: Injects `sentiment_score`, `praises`, and `complaints` per review, plus a top-level `sentiment_summary: { praises: [...], complaints: [...], average_sentiment: f64 }` in exported JSON and CSV files.
  - **Standalone File Analysis**: Analyze pre-existing scraped JSON/CSV review exports offline via `--input-file`.
- **Command-Line Flags**:
  - `--analyze-sentiment` / `--no-analyze-sentiment`: Enable/disable automated sentiment analysis & keyword clustering (default: `True`).
  - `--sentiment-summary`: Print top 5 praises and top 5 complaints with frequency counts directly to the terminal.
  - `--input-file <path>`: Path to existing JSON/CSV reviews file to analyze sentiment without launching a browser.
- **Usage**:
  ```bash
  # Scrape with sentiment summary printed to terminal and exported to JSON/CSV
  python3 scripts/scrape-reviews.py --source google --google-url "The Law Offices of Jacob Emrani" --sentiment-summary --output reviews/google-reviews

  # Scrape Yelp reviews with min 4-star filter
  python3 scripts/scrape-reviews.py --source yelp --yelp-url "https://www.yelp.com/biz/example" --min-rating 4 --format both

  # Analyze sentiment offline on an existing reviews export
  python3 scripts/scrape-reviews.py --input-file reviews/google-reviews.json --sentiment-summary
  ```


## Adopting in Astro Projects

To sync or update site-tooling into an Astro project:
1. Ensure `package.json` includes required devDependencies (`puppeteer`, `pa11y`, `pa11y-ci` for accessibility).
2. Wire `scripts` in `package.json`:
   ```json
   "test:a11y": "scripts/test/with-preview.sh scripts/test/list-sitemap-urls.mjs",
   "test:a11y:themes": "scripts/test/with-preview.sh node scripts/test/a11y-scan.mjs"
   ```
