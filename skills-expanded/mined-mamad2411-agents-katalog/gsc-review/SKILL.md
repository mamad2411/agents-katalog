---
name: gsc-review
description: Weekly GSC traffic review and improvement batch for boring-math.com. Site-wide crawl, AI-search and other sites: /seo-review.
disable-model-invocation: true
---

# GSC Review: boring-math.com

Repo: `~/boring-maths/` (Astro 5 static site, Cloudflare Pages auto-deploys master).
Running checkpoint log: memory file `project_boring_maths_gsc_workflow.md`. READ IT FIRST. It holds every prior checkpoint's numbers and rulings. Compare against the newest checkpoint; append this run's checkpoint when done.

## Mode

- Invoked plain (`/gsc-review`): pull, analyze, report ranked levers, then WAIT for "go" before editing anything. Merging deploys production.
- Invoked with "ship" / "go" / "and fix" in the same message: run the full loop including the PR batch without re-asking.

## 1. Pull fresh data

```bash
npm --prefix ~/boring-maths run seo:gsc-pull
```

- OAuth token (`scripts/seo/.gsc-token.json`) expires ~7 days. On auth failure: `npm --prefix ~/boring-maths run seo:gsc-pull -- --reauth` + browser consent (sign in as the Google account that owns the property, `sc-domain:boring-math.com`; consent is clickable via Chrome automation when already signed in).
- The pull prints the REAL totals ("Totals: N clicks / N impressions across N pages"). Use these, not the report summary.
- Step complete when the printed Totals line is captured for the step-3 comparison.

## 2. Analyze

```bash
python scripts/gsc_analysis.py          # writes docs/gsc-analysis-<date>.md
python scripts/gsc_region_analysis.py   # writes docs/gsc-region-analysis-<date>.md
```

Data gotchas (these bite every time):
- The report's Summary covers only visible queries (~42% of impressions are anonymized). Page-level totals from the pull output are the truth.
- Query-level clicks are mostly anonymized to 0. Use query positions/impressions as signal; use page-level rows for click truth.
- Page positions are impression-weighted averages; always check query-level before optimizing a page.
- Country splits suppress clicks (country totals reliable, splits are impression/position signal only).
- Read exports with `encoding='utf-8'` in Python (cp1252 default chokes).
- Top pages by clicks, direct from export:
  `gsc-export/<date>/gsc-pages-28d.json`, sort by clicks desc.

## 3. Compare vs checkpoint

Against the newest checkpoint in the memory file: totals, top click pages, the tracked clusters (UK money, activation set, machining, event/party, cooking), and any pages the last run touched. Note: consecutive weekly 28d windows overlap ~21/28 days, so deltas are damped; call trends directional, not proven.

## 4. Measured laws

1. **Instant-answer queries: never invest.** discount-calculator (~25% of ALL site impressions), percentage-calculator, "X% off $Y": Google answers inline, 0 clicks at pos 9-15. Proven repeatedly.
2. **Title-tuning striking-distance pages (pos 8-20) does not add clicks without links** (raise-calculator, proven Aug-8). Title changes are only for adding missing RELEVANCE terms to deep pages (pos 25-60), with modest expectations.
3. **UK money cluster + activation set + SMP are authority-bound** (parked pos 40-85, 0 clicks). Only backlinks move them. Every report must restate the pitch-table status (`REVENUE.md` + `docs/outreach/2026-07-pitches.md`), empty since mid-Jul 2026, Phase 4 open since Feb.
4. **Before proposing a build: grep the registry** (`src/lib/calculators.ts`). Coverage is essentially complete; every "gap" so far already had a page (phantom-build lesson, twice).
5. **Before proposing internal links: grep actual inbound sources** (`grep -rl "<slug>" src/pages --include="*.astro"`). contractor-vs-employee looked link-starved but had 11 inbounds; its stall is authority.
6. **Cannibalization: fix at the root.** Usually one page's title claims an intent its content doesn't own (e.g. generic mortgage page claiming "PMI & Taxes"). Differentiate titles to match actual content; cross-link the pair.

## 5. Lever hunt, in priority order

1. New winner pages (clicks appeared without work), reinforce with editorial links if genuinely under-linked (law 5).
2. Cannibalized queries with an intent mismatch at the root (law 6).
3. Orphans WITH demand: cross-check `scripts/seo/known-orphans.json` against page impressions; de-orphan via `relatedCalculators` entries on topically-close pages.
4. Relevance title adds for deep pages (law 2), missing high-impression query words (report section "Content Gaps").
5. Worked-example FAQs for long question/word-problem queries already ranking pos ≤12 (homework niche: coffee-spend, event-seating class). Verify every number in the answer by hand.
6. Genuinely new demand: only after law 4's registry check, and only if it passes CLAUDE.md rule 5 (real problem, not SEO bait).

## 6. Execute the batch (only in ship mode or after "go")

1. `git checkout -b seo/gsc-<date>-batch` (check `git branch` first).
2. Make the edits. For every new editorial link: add the edge to `scripts/seo/expected-link-edges.json` AND remove de-orphaned pages from `scripts/seo/known-orphans.json` (shrink-only ratchet).
3. Gates, all must pass before commit:
   ```bash
   npm run build     # includes postbuild: trailing-slash, link edges, orphan guard
   npx vitest run
   ```
4. Commit: message via Write tool to a file + `git commit -F <file>` (PowerShell pipes prepend a BOM). No em dashes in the message. Grep the file to confirm. Stage specific files, never `git add -A`. Commit the new `docs/gsc-*.md` reports too.
5. `git push -u origin <branch>`, `gh pr create`, `gh pr merge <N> --squash --delete-branch`.
6. Live-verify: poll `https://boring-math.com/<changed page>` for a changed string every 20s (CF Pages deploy ≈ 200s), then spot-check one new link + one new FAQ in the served HTML.
7. Writeback: append an EXECUTED/CHECKPOINT stanza to memory file `project_boring_maths_gsc_workflow.md` (numbers, PR, what shipped, what was dropped and why, still-gated items) and `hippo remember` any new lesson.

## 7. Report format

Lead with totals vs last checkpoint. Then: winners, cluster movement, ranked levers (with the do-not-invest list applied), what shipped (if ship mode) with gate results and live-verify proof, and ALWAYS the Keith-gated items: the backlink pitch sends first, until the table in REVENUE.md has entries.
