---
name: freshness-recheck
description: Re-collects, on the collector, the pages a Fetchproof brief rests on before a build starts or a release ships, using research.mjs --refresh-days, so a vendor that changed a limit, price or schema is caught in the corpus before it reaches code. Use before a release, when a brief is older than its refreshDays, when a builder reports behaviour that contradicts the brief, or when the user asks whether the research is still current. Collector only.
---

# Freshness recheck

A capture is true of the day it was fetched. Before the code that depends on it ships,
check the day has not moved on.

## Steps (collector only - a builder refuses to collect)

1. `node "$HOME/.agents/fetchproof/bin/research.mjs" --status` - the budget, and the
   corpus's age.
2. `node "$HOME/.agents/fetchproof/bin/research.mjs" --refresh-days <n> --dry-run` -
   which captures are older than `n` days and would be re-collected. Choose `n` from how
   fast the fact goes stale (the map's D-6 row), not from habit. For the rows a
   **volatile** requirement rests on (a price, rate limit, quota, API or schema version,
   plan or tier boundary - auto-build marks them), `n` is the project's `refreshDays`
   from `research/plan.json`, never longer.

   `--refresh-days 0` does not re-collect a capture made today: it re-collects a capture
   older than `n` days, and today's is 0 days old. For a same-day re-check, use `--force`
   with `--dry-run` first. `--force` re-fetches every page the plan names and runs every
   search again, those for closed unknowns included, keeping up to `perQuery` pages each
   within the run's scrape budget; the dry run lists what it would spend. `--only <text>`
   narrows the searches it runs again, not the plan's pages.
3. Run it without `--dry-run`. Every re-collection spends a credit; when the account runs
   out the run stops and asks - never pass `--fallback` on your own initiative.
4. `node "$HOME/.agents/fetchproof/bin/preflight.mjs"` - a row superseded by a fresher
   capture **fails the gate** where an unknown still cites it, unless its quoted words
   survived the refresh (ADR-0193: `quote-survived-refresh`, shown with `--show-pass`). Either
   way, re-read the new capture, move the citation, and rewrite the finding
   (`finding-rewriter`). A cited page the refresh found gone (HTTP 404 or 410) fails as
   `cites-gone-page`: re-research the unknown, or record
   in the row's Finding that the page now answers HTTP 404 (or 410) and why the earlier
   reading still holds.
5. If a fact changed: record it as a contradiction in the brief (old capture vs new),
   redraft the brief, and tell the builder which E-## rows moved - `cite-in-code`
   comments name them.

## Rules

- `preflight`'s age limit is the machine config's `maxAgeDays` (180 by default) and holds
  for every project on the machine. Lower it only on a machine that works mostly on
  fast-moving vendors; for one project's fast facts, the volatile marking and
  `refreshDays` are the tool.

- Never edit an old capture to match the new page. History stays; the new capture
  supersedes it.
