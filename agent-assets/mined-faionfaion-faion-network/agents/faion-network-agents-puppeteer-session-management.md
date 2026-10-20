# Puppeteer Session Management

## Summary

**One-sentence:** Produces a Puppeteer session layer using userDataDir per logical identity, explicit cookie serialisation as a secondary mechanism, isolated browser contexts per parallel job, and a daemonised runner for long-lived sessions.

**One-paragraph:** Sessions in Puppeteer come from two mechanisms: userDataDir (full Chromium profile: cookies, storage, cert cache) and explicit cookies via page.setCookie/page.cookies. userDataDir per identity is the primary choice — it survives complex login flows including HSTS pinning. Explicit cookie serialisation is a secondary path for simple cases. Parallel jobs MUST use distinct browser.createIncognitoBrowserContext to isolate state. Long-lived sessions live in a daemonised runner the agent talks to over HTTP/queue, not in the LLM turn. The artefact is the session config; the validator enforces the canonical fields.

**Ефективно для:**

- Multi-tenant scrapers running parallel jobs against the same target.
- Workers reusing an existing logged-in session across many runs.
- Daemonised browser runners called via queue or HTTP.
- Tests needing isolated state per scenario.

## Applies If (ALL must hold)

- Worker authenticates to a target site and reuses the session many times.
- Multiple jobs run concurrently and must not see each other's state.
- Auth flow is non-trivial (HSTS pin, MFA setup) and userDataDir simplifies it.
- Daemon process is acceptable for the deployment target.

## Skip If (ANY kills it)

- One-off scripts with no auth.
- Single-shot login flows where storageState (Playwright) is a better fit.
- Pure stateless scraping of public pages.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Number of logical identities | 1 | N | task brief |
| Parallelism plan | single | concurrent N | ops plan |
| Session lifetime | per-run | persistent | daemon | deploy plan |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[puppeteer-launch-setup]] | launch wrapper invoked with userDataDir option |
| [[puppeteer-agent-workflow]] | long-lived sessions live behind a queue, never inline |

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
| `decide-userdatadir-vs-cookies` | sonnet | decision tree application |
| `emit-session-helpers` | sonnet | render perIdentity launch + cookie save/load |
| `isolate-parallel-jobs` | haiku | wrap each job in createIncognitoBrowserContext |

## Templates

| File | Purpose |
|------|---------|
| `templates/session.ts` | Per-identity session launch + cleanup |
| `templates/daemon.ts` | Daemon runner serving session work via HTTP |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-puppeteer-session-management.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[puppeteer-launch-setup]]
- [[puppeteer-agent-workflow]]
- [[puppeteer-stealth-proxy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
