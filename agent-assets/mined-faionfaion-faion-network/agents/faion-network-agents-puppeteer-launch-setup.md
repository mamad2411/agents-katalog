# Puppeteer Launch & Navigation Setup

## Summary

**One-sentence:** Produces a Puppeteer launch config + navigation wrapper with correct CI/Docker flags, pinned Chromium revision, finally-close discipline, and SPA-safe wait strategies.

**One-paragraph:** Puppeteer launch config is dominated by two failure modes: missing --no-sandbox in Docker/CI and over-using waitUntil='networkidle0' on SPAs. This methodology emits a launch wrapper with the safe flag set, PUPPETEER_CACHE_DIR for read-only containers, a pinned Chromium revision in the lockfile, a try/finally to guarantee browser.close, and a goto helper that defaults to domcontentloaded + a targeted waitForSelector. The artefact is the config metadata; the validator checks the canonical fields are present.

**Ефективно для:**

- First-time Puppeteer setup in a Node.js worker.
- Migrating an existing script onto Puppeteer 22+ (waitForTimeout removed).
- Containerised CI runs needing --no-sandbox + dev-shm flags.
- Serverless deploy via @sparticuz/chromium with pinned revision.

## Applies If (ALL must hold)

- Node.js worker driving Chromium via DevTools Protocol.
- Target environment is Docker, CI, or serverless (read-only filesystem).
- Need reproducible browser version across runs.
- Script runs as part of a larger pipeline (artifacts > exit code matter).

## Skip If (ANY kills it)

- Cross-browser testing — use Playwright.
- Long-lived browser daemons fronted by an API (use puppeteer-session-management).
- Manual interactive debugging in a developer's machine without CI parity.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target environment | local | docker | ci | serverless | deploy plan |
| Node.js >= 18 | binary on PATH | developer machine + CI |
| Chromium version policy | bundled | pinned | external @sparticuz | task brief |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[puppeteer-agent-workflow]] | this config is what the worker uses |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-flag-set` | haiku | lookup based on environment |
| `emit-launch-wrapper` | sonnet | render reusable launch + goto helpers |
| `verify-cleanup` | haiku | scan for missing browser.close in finally |

## Templates

| File | Purpose |
|------|---------|
| `templates/launch.ts` | Reusable launch wrapper with environment-aware flags |
| `templates/goto.ts` | SPA-safe page.goto helper |
| `templates/worker.ts` | Worker showing try/finally browser.close discipline |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-puppeteer-launch-setup.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[puppeteer-agent-workflow]]
- [[puppeteer-page-interaction]]
- [[puppeteer-session-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
