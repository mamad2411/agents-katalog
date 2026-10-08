# Recon Pipeline

Scoring and analysis engine. Reads scraped data from KV, computes CVS scores,
repo health, lifecycle stages, sentiment, and compiles dossiers.

## Module Map

- `kv-reader.ts` / `kv-writer.ts` — KV access layer (reads consolidated `recon:{slug}`)
- `issue-scorer.ts` — CVS scoring: `repo_score*0.30 + issue_score*0.50 + timing_score*0.20`
- `health-scorer.ts` — Repo health: maintainer, merge accessibility, availability scores
- `lifecycle.ts` — fresh / triaged / accepted / stale / zombie classification
- `sentiment.ts` — Pattern-matched comment sentiment (-1 to 1)
- `quirks.ts` — Detects changesets, CLA, conventional commits requirements
- `dossier-compiler.ts` — 6-section markdown generation
- `issue-brief.ts` — SWE agent execution context per issue
- `comment-digest.ts` — Structured comment thread context
- `related-issues.ts` — Issue relationship detection
- `precompute.ts` — Batch compute + store all analysis for a repo
- `claims.ts` — Claim tracking (vibedispatch reports claims via API)
- `triggers.ts` — Fires POST to scraper API for re-scrapes
- `types.ts` — All Zod schemas and TypeScript types for the recon domain

## CVS Tiers

85-100 = go, 70-84 = likely, 50-69 = maybe, 30-49 = risky, 0-29 = skip

## Kill Signals

Archived repos or no merged PR in 90d: all issues get `cvs: 0`, `cvsTier: 'skip'`, `repoKilled: true`.

## This module does NOT

- Make external API calls except to scraper trigger endpoint (see `triggers.ts`)
- Access filesystem — all data via KV
- Define UI components (see `src/`)
- Handle HTTP routing directly (routes in `issue-routes.ts`, `claim-routes.ts`, `compute-routes.ts`)

## CF Worker Constraints

- 128MB memory, 30s CPU time limit
- Pre-compute pipeline (`precompute.ts`) runs via `waitUntil()` to avoid request timeout
- Dossier / health / scores are cached in KV, not computed per-request
