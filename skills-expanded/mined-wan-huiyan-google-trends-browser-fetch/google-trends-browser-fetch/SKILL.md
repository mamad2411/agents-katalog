---
name: google-trends-browser-fetch
description: "Fetch Google Trends data (search interest over time) via Claude-in-Chrome browser automation, including the multi-chunk daily-resolution stitching trick for date ranges longer than 90 days. Produces calibrated daily time series with provenance files. Use this skill whenever the user wants Google Trends data, search interest data, trend_category or trend_brand_share covariates, or mentions pytrends, trends.google.com, multiTimeline.csv, or search volume for modeling. Also triggers when the user needs daily-resolution Trends beyond a 90-day window (the Google Trends UI silently downgrades to weekly for longer ranges — this skill handles the chunking + stitching). Not appropriate when the user already has a live Google Trends API credential; use that directly instead."
---

# Google Trends Browser Fetch

Download Google Trends search-interest data via the [Claude in Chrome](https://claude.ai/chrome) browser extension, then stitch multiple ~75-day chunks into a single calibrated daily time series.

## Why this skill exists

`pytrends` was archived in April 2025 after Google's anti-scraping measures. The official Google Trends API launched July 2025 is alpha-gated with no guaranteed access. For most users, **browser-driven CSV export is the only reliable path** today. This skill codifies the workflow so you don't reinvent it.

There's also a non-obvious wrinkle: Google Trends returns **weekly** resolution for ranges ≥90 days and **daily** for ranges <90 days. To get daily data over a longer window (e.g., 18 months) you have to download overlapping chunks and stitch them — which is fiddly because each chunk is independently normalized to its own 0-100 scale. This skill handles that.

## When to use

Trigger when the user wants Google Trends / search-interest data, especially:
- As a covariate in a time-series or causal-inference model
- For ranges longer than 90 days where daily resolution matters
- When `pytrends` came up and you need to explain the alternative

Skip when:
- User has live Google Trends API credentials (use those)
- The analysis only needs weekly resolution AND range <5 years (single download suffices)

## Prerequisites

Confirm a browser-automation path is in place before proceeding. The stitching logic is universal, but the navigate/click/download calls differ by harness. Pick one:

### Path A: Claude in Chrome (Anthropic-first-party)

Preferred when available. Tools named `mcp__Claude_in_Chrome__*` (`navigate`, `left_click`, `read_page`, `javascript_tool`, `read_network_requests`).

Requirements (as of April 2026, per [official docs](https://code.claude.com/docs/en/chrome)):
- Google Chrome or Microsoft Edge (not Brave, Arc, other Chromium; not WSL)
- [Claude in Chrome extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) v1.0.36+
- Claude Code v2.0.73+ — launch with `claude --chrome` or run `/chrome` in session
- **A direct Anthropic paid plan (Pro, Max, Team, or Enterprise).** API key / pay-as-you-go / Bedrock / Vertex / Foundry are explicitly excluded.
- Known gotcha: if the Claude desktop app is also running, it may grab the native-messaging-host registration and the CLI errors with "extension not connected." Close desktop, or run `/chrome` → Reconnect.

### Path B: third-party browser MCP (Cursor, Windsurf, other IDEs)

If the user is on Cursor or another non-Anthropic harness — or on an Anthropic API-key account that doesn't qualify for Claude in Chrome — use a generic browser MCP:
- [Browser MCP](https://browsermcp.io/) — works with Cursor, VS Code, Claude Desktop
- [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) — Chrome DevTools Protocol, works with most MCP hosts

Tool names differ but all provide some variant of navigate / click / eval-JS / wait. Adapt the workflow below to whichever is available.

### Path C: manual human download

Always works as a fallback. The human navigates + clicks CSV download themselves; Claude only plans the URLs and runs the stitching script. Slower but has no compatibility constraints.

### Common requirements (all paths)

- Chrome signed into a Google account. Trends is public, but anonymous sessions rate-limit faster on multi-chunk fetches.
- User knows their browser's Downloads folder (default `~/Downloads/`). Files land as `multiTimeline.csv`, `multiTimeline (1).csv`, etc.
- **Allow multiple downloads from `trends.google.com`.** Chrome blocks the 2nd download onward from the same site by default. Without this, only the first chunk arrives and the rest silently fail. One-time fix:
  - **Global setting**: Chrome → `Settings → Privacy and security → Site settings → Additional permissions → Automatic downloads → "Sites can ask to automatically download multiple files"`
  - **Per-site allowlist** (tighter): the first time Chrome blocks a download you'll see a small icon in the URL bar — click it and choose "Always allow trends.google.com to download multiple files"
- Python 3.9+ with pandas and numpy for the stitching step.

## Decision: weekly vs daily

Ask the user (or decide from context) which is needed:

| Need | Ranges | Approach |
|---|---|---|
| **Weekly** is enough | Any | 1 download covering the full range. Skip to [Weekly path](#weekly-path). |
| **Daily** resolution, range < 90 days | Single chunk | 1 download. Skip to [Weekly path](#weekly-path) — the CSV will already be daily. |
| **Daily** resolution, range ≥ 90 days | Needs stitching | Multi-chunk workflow. Use [Daily stitched path](#daily-stitched-path). |

Daily is worth the extra work when: (a) the model uses daily data and (b) the signal is weakly correlated with the target. For a signal that's already highly correlated, weekly-interpolated-to-daily adds nothing the model can't get from weekly seasonality.

## Weekly path

Simple single-download flow.

1. Build the URL:
   ```
   https://trends.google.com/trends/explore?date=YYYY-MM-DD%20YYYY-MM-DD&geo=<COUNTRY>&q=<TERM1>,<TERM2>&hl=en-GB
   ```
   - `date` takes two ISO dates separated by `%20` (URL-encoded space)
   - `geo` is an ISO country code (e.g., `GB`, `US`, `DE`) — omit for worldwide
   - `q` takes up to 5 comparison terms, comma-separated
   - For comparison/co-normalization (e.g., brand vs category), put both terms in `q`

2. Navigate and wait for the chart to render. With Claude in Chrome:
   ```
   mcp__Claude_in_Chrome__navigate(url=<url>)
   mcp__Claude_in_Chrome__read_page()   # confirm "Interest over time" section loaded
   ```
   With Browser MCP, chrome-devtools-mcp, or similar, use that tool's `navigate` + `snapshot`/`read` equivalent.

3. Click the download button on the "Interest over time" card. The button is a small CSV-download icon in the top-right of that specific card (not the page-wide one). If a simple click doesn't start the download, fall back to evaluating JS: query the card's download link by its aria-label or SVG icon and click it programmatically.

4. The file lands in `~/Downloads/` as `multiTimeline.csv` (or `multiTimeline (N).csv` if that name is taken). Move/rename it with a descriptive name.

5. Write a provenance file — see [Provenance](#provenance).

## Daily stitched path

Multi-chunk workflow. Overall plan:

1. **Plan the chunks** — generate overlapping ~75-day windows covering the full range (target ~15-day overlaps for cross-normalization).
2. **Also download a single weekly reference** covering the whole range (used for global calibration).
3. **Download each chunk** via the browser (same steps as weekly path, one URL per chunk).
4. **Stitch** via chain cross-normalization on overlaps, then **calibrate** against the weekly reference.
5. **Write provenance** capturing every chunk's date range and the stitching quality.

### Step 1: plan chunks

Run the helper:

```bash
python scripts/plan_chunks.py --start 2024-09-29 --end 2026-03-15 \
  --chunk-days 75 --overlap-days 15 \
  --geo GB --terms nike,running shoes \
  > chunks.json
```

Output is a JSON array of `{url, start, end, filename}` objects. Review with the user — they may want to adjust chunk boundaries around known events (e.g., don't split across a known-volatile week like Black Friday unless you have to).

### Step 2: download the weekly reference

Download once covering the full range:
```
https://trends.google.com/trends/explore?date=<FULL_START>%20<FULL_END>&geo=<GEO>&q=<TERMS>
```
Save as `reference_weekly.csv`.

### Step 3: download every chunk

For each chunk in `chunks.json`:
- `mcp__Claude_in_Chrome__navigate(url=chunk.url)`
- Wait briefly (Trends has rendering delay and occasionally throttles — if the chart fails to load, try again after a few seconds; if throttled repeatedly, pause for ~30s between chunks)
- Trigger the CSV download
- Rename `~/Downloads/multiTimeline*.csv` → the target name from `chunks.json`

**Rate-limit guidance**: spacing ~10–20s between downloads is usually fine. If you see "You're not a robot?" captchas, the signed-in session gives more headroom than anonymous.

### Step 4: stitch and calibrate

```bash
python scripts/stitch_daily.py --chunks chunks.json \
  --reference-weekly reference_weekly.csv \
  --out trends_daily_stitched.csv
```

The script:
1. Loads every chunk CSV, aligns to a common date index
2. Chain cross-normalizes via **median ratio** on each pair's overlap region (robust to outliers; preserves relative levels)
3. Globally calibrates stitched-daily against reference-weekly using a single median-ratio scalar per term
4. Reports stitching quality: per-term median ratio and stddev across chunk joins, plus daily-vs-weekly correlation

See `references/stitching-math.md` for the algorithm detail and why median-ratio beats OLS fits for this use case.

### Step 5: sanity-check

Before declaring done, look at:
- **Stitching ratio std dev** — if >0.15 for any term, the chunks disagree enough that the joined series is noisy; consider narrower chunks or check that overlap windows actually overlap
- **Daily-weekly correlation** — should be in the 0.5–0.8 range. If >0.95, daily is just a smoother weekly (no new info). If <0.3, something is wrong — probably a misaligned chunk.
- **Visual inspection** — plot daily and weekly on the same axes; join points should be smooth, not stair-stepped.

## Provenance

Every downloaded CSV is useless without provenance. Write a companion `.provenance.md` file. See `references/provenance-template.md` for the exact template.

Minimum required fields:
- Source URL (including exact `date=`, `geo=`, `q=` params)
- Download date
- Method (which browser, which tool)
- Geography and search terms
- Exact date range
- Processing steps (especially any stitching / interpolation)
- For stitched files: chunk-to-filename mapping table and quality metrics

## Pitfalls to avoid

1. **Don't recommend `pytrends`.** Archived April 2025. Explain this to the user if they bring it up.
2. **Don't generate synthetic data that looks real.** If the download fails, report the failure — don't make up plausible numbers. Every Trends CSV must trace to an actual browser download.
3. **Don't mix date formats.** Google Trends URLs use ISO `YYYY-MM-DD`. The CSV header sometimes uses regional formats (`DD/MM/YYYY` for some locales). Parse with pandas' `parse_dates` with explicit `dayfirst` where needed.
4. **Don't forget that Trends indices are relative, not absolute.** Every download is normalized 0–100 within its own query. You cannot compare two independent downloads without a calibration step.
5. **Don't interpret a weekly-interpolated-to-daily signal as true daily data.** It has autocorrelation ~0.99 (flat within each week) and adds nothing to a model that already has weekly seasonality.
6. **Don't rely on clicking the page-wide download menu.** Click the CSV icon on the specific "Interest over time" card; the page-wide menu exports a multi-sheet zip that's harder to parse.
7. **Rate limiting is real and gets worse with anonymous sessions.** Sign in first; space downloads; retry on failure.
8. **Chrome blocks multiple downloads from the same site by default.** If only the first chunk arrives and later ones silently fail with no error, check Chrome's automatic-downloads setting (see prerequisites). This is the single most common first-run failure mode.

## Bundled resources

- `scripts/plan_chunks.py` — generate overlapping chunk date ranges and URLs
- `scripts/stitch_daily.py` — chain-normalize chunks and calibrate to a weekly reference
- `references/stitching-math.md` — the median-ratio algorithm and why it beats alternatives
- `references/provenance-template.md` — provenance file template
- `references/url-examples.md` — worked URL examples for common query shapes
