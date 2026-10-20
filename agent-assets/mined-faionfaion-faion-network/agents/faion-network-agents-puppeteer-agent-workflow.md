# Puppeteer Agent Workflow

## Summary

**One-sentence:** Produces a Puppeteer worker script that the agent invokes via Bash with a hard timeout, captures structured artifacts to disk, and never runs browser logic inline in the LLM turn.

**One-paragraph:** Driving Puppeteer from an LLM agent has one core constraint: the LLM context is stateless and token-bounded, while browser processes are long-lived and stateful. This methodology produces a node script that the agent launches via Bash with --timeout, captures console/screenshots/HAR/structured-JSON to disk, then reads back only the structured artifact. Long sessions live in a daemonised runner the agent talks to over a queue or HTTP. The script bans waitForTimeout (removed in Puppeteer 22), bans waitUntil='networkidle0' on SPAs, requires attribute-based selectors over screenshot-derived ones, scrubs secrets before persisting, and pauses for human review on credential/CAPTCHA/2FA walls.

**Ефективно для:**

- Agentic web tasks that need DevTools Protocol features (CDP, request interception).
- Headless Chromium scripting where Playwright bundles are too large for the serverless target.
- Stateless scripts invoked per task, capturing artifacts for later LLM analysis.
- Long-lived browser daemons fronted by a queue or HTTP API the agent calls.

## Applies If (ALL must hold)

- Headless Chrome via DevTools Protocol with CDP needs.
- Generating PDFs or screenshots from rendered HTML in a Node-only pipeline.
- Light scraping where stealth is already handled (no aggressive bot defence).
- Running on serverless (chromium binary via @sparticuz/chromium).

## Skip If (ANY kills it)

- Cross-browser testing — use Playwright (Firefox + WebKit are first-class there).
- E2E test suites with parallelism, retries, fixtures — Playwright Test or Cypress.
- Long-running scraping farms against bot-defended targets — managed service.
- Tasks that need to run inside the LLM turn synchronously — wrong tool entirely.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target URL + task description | free text | task brief |
| Credentials policy | session token | env vars | human-in-loop | secret policy |
| Output artifact shape | JSON | screenshot | PDF | downstream consumer |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[puppeteer-launch-setup]] | config knobs and headless flags |
| [[puppeteer-page-interaction]] | selector + wait discipline |
| [[puppeteer-output-capture]] | artifact shapes and quality settings |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-bash-or-inline` | sonnet | always Bash; reject any plan that runs Puppeteer in the LLM turn |
| `write-worker-script` | sonnet | scaffold node script with timeout + artifact capture |
| `scrub-secrets` | haiku | diff artifacts against secret patterns; replace matches |

## Templates

| File | Purpose |
|------|---------|
| `templates/worker.mjs` | Bash-invoked worker script with hard timeout + artifact capture |
| `templates/invoke.sh` | Bash wrapper applying wall-clock timeout |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-puppeteer-agent-workflow.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[puppeteer-launch-setup]]
- [[puppeteer-page-interaction]]
- [[puppeteer-output-capture]]
- [[puppeteer-session-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
