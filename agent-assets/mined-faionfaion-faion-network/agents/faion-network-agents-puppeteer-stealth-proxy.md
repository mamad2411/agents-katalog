# Puppeteer Stealth & Proxy

## Summary

**One-sentence:** Produces a Puppeteer stealth + proxy layer using one documented evasion stance (plugin or manual, never both), proxy rotation with circuit breaker on 4xx, and bounded retries.

**One-paragraph:** Stealth and proxy mistakes have one root cause: layering. This methodology requires picking exactly one evasion stance (puppeteer-extra-plugin-stealth alone OR manual navigator overrides alone) and documenting it. Proxy rotation uses a small bounded pool with health checks; 429/403 responses trip a circuit breaker that surfaces to the caller instead of silent looping. The artefact is the stealth + proxy config metadata; the validator enforces the canonical fields.

**Ефективно для:**

- Scrapers against targets with mild bot detection (signature checks, no Turnstile).
- Pipelines requiring rotating IPs for rate-limit avoidance.
- Workers using managed browser services (Browserless, ScrapingBee) with retry policies.
- Auditing existing scripts that mix stealth plugin + manual overrides (and breaking from there).

## Applies If (ALL must hold)

- Target has signature-based bot detection (navigator props, WebGL fingerprint) but not aggressive challenge pages.
- Run budget allows multiple retries against rate-limited responses.
- Proxy pool available (residential or DC) with health monitoring.
- Worker can surface circuit-breaker trips to the caller.

## Skip If (ANY kills it)

- Targets with hardened bot defence (Cloudflare Turnstile aggressive, Akamai BMP) — use a managed solver instead.
- Public APIs with documented rate limits — call the API, not the page.
- Local dev where no proxy is needed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stealth stance choice | plugin | manual | none | team decision |
| Proxy pool | list of endpoints + auth + health URL | ops provided |
| Retry policy | max retries + backoff + circuit-breaker threshold | task brief |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[puppeteer-launch-setup]] | launch wrapper accepts proxy + extra args |
| [[puppeteer-agent-workflow]] | worker exits non-zero with status on circuit breaker |

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
| `pick-stance` | sonnet | decide plugin vs manual; document it |
| `emit-proxy-rotator` | sonnet | render small pool + health check + circuit breaker |
| `audit-evaluate-assertions` | haiku | scan page.evaluate calls for navigator-prop asserts that mismatch the stance |

## Templates

| File | Purpose |
|------|---------|
| `templates/stealth-worker.ts` | Stealth-plugin-only worker (stance documented at top) |
| `templates/proxy-pool.ts` | Small proxy pool with health-check + circuit breaker |
| `templates/retry.ts` | Bounded retry helper with exponential backoff |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-puppeteer-stealth-proxy.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[puppeteer-launch-setup]]
- [[puppeteer-page-interaction]]
- [[puppeteer-session-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
