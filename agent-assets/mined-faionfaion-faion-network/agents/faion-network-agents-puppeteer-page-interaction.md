# Puppeteer Page Interaction (Selectors, Clicks, Forms)

## Summary

**One-sentence:** Produces a Puppeteer interaction layer using attribute-based selectors (data-testid/id/name), targeted waitForSelector instead of waitForTimeout, request interception for stable scraping, and form fills via type/select/check methods.

**One-paragraph:** Most flaky Puppeteer scripts have two root causes: positional selectors that break on any layout change, and fixed sleeps instead of targeted waits. This methodology produces an interaction layer with click/type/select helpers that take attribute-based selectors only, a wait helper that wraps waitForSelector + waitForFunction (never waitForTimeout), request-interception helpers for stable scraping (block analytics, mock APIs), and form-fill helpers that handle disabled-state checks before the action.

**Ефективно для:**

- Building a stable scraping or workflow script against an SPA.
- Refactoring a flaky positional-selector script onto attribute selectors.
- Adding request interception to block analytics and speed up scrapes.
- Writing form-fill flows that respect disabled/loading states.

## Applies If (ALL must hold)

- Worker uses Puppeteer 22+ (waitForTimeout removed).
- Target page exposes data-testid/id/name/aria-label on interactive elements (or you can add them).
- Stability across CSS refactors matters (script runs many times).
- Form flows where elements may be temporarily disabled.

## Skip If (ANY kills it)

- One-off debugging in dev where any selector works.
- Cross-browser need — use Playwright with role locators.
- Pages whose only stable identifiers are visual; consider a screenshot-based AI tool.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target page DOM via page.content() or staging copy | HTML snapshot | live page or staging |
| Selector contract | data-testid / id / name preferred | frontend team |
| Form/action map | list of (selector, action, expected post-state) | task brief |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[puppeteer-launch-setup]] | page handed in came from safe launch wrapper |
| [[puppeteer-agent-workflow]] | this code runs inside a Bash worker |

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
| `inspect-dom` | haiku | scan page.content() for stable attributes |
| `emit-interaction-helpers` | sonnet | render click/type/select with attribute-only selectors |
| `wire-request-interception` | sonnet | block analytics / mock APIs based on scrape goal |

## Templates

| File | Purpose |
|------|---------|
| `templates/interact.ts` | Interaction helpers using data-testid + wait + native APIs |
| `templates/interception.ts` | Request interception blocking analytics + ads |
| `templates/form.ts` | Form submission waiting for API response |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-puppeteer-page-interaction.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[puppeteer-launch-setup]]
- [[puppeteer-output-capture]]
- [[puppeteer-stealth-proxy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
