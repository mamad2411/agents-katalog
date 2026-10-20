# Technical Debt Trade-off Framework

## Summary

**One-sentence:** Classifies a piece of technical debt on the Fowler quadrant, sizes the 15-20% debt budget, and emits a debt item with explicit repayment trigger.

**One-paragraph:** Technical debt is the implied cost of rework caused by choosing an easier solution now. This methodology emits a debt-record: Fowler-quadrant classification (deliberate/inadvertent x reckless/prudent), severity (localized vs systemic), repayment trigger (observable, not "someday"), and budget impact against the project's 15-20% debt allocation. Output drives the ADR Decision section and the team's debt backlog.

**Ефективно для:**

- Solo architect tagging shortcuts taken under deadline pressure with their repayment criteria.
- Reviewing accumulated debt before adding a new feature in the same code area.
- Quarterly prioritisation of which debt items to pay down within the 15-20% budget.
- Communicating debt severity to a non-technical founder when refactor competes with new feature.

## Applies If (ALL must hold)

- Shortcut affects a code area that will be touched again within 12 months.
- The "easier solution" is shippable now AND a "better solution" exists with known cost.
- Project has (or can have) a debt backlog tracked beside the feature backlog.
- Decision is deliberate (you see two options) — not retro-discovered.

## Skip If (ANY kills it)

- Code area will not be touched for 2+ years — debt is not debt if interest is never paid; document and accept.
- Decision is actually an architectural flaw (foundation-level wrong) — escalate to ATAM, not debt.
- One-off prototype that will be thrown away — debt is irrelevant.
- The "better solution" has no known cost — first do a spike to size it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Shortcut description | what we shipped vs the better option | architect / dev |
| Touch-frequency estimate | times/quarter this code is edited | git log + roadmap |
| Debt backlog | existing debt items + current total budget | project tracker |
| Project debt budget | percent of capacity allocated (15-20%) | architect / PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[architecture-decision-records]] | Debt items often inline into an ADR Decision section. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules (Fowler classification, observable repayment trigger, debt-budget cap, localized vs systemic, deliberate-vs-flaw boundary) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for debt-record + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: someday-trigger, debt-as-foundation-flaw, no-budget-cap, hidden-debt | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure (classify → trigger → size → budget-check → record) | 700 |
| `content/05-examples.xml` | essential | Worked example: deliberate-prudent debt with a load-threshold trigger | 500 |
| `content/06-decision-tree.xml` | essential | Routes by Fowler quadrant + touch frequency + budget headroom | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `trade_off_technical_debt_classify` | sonnet | Quadrant placement with judgement on intent. |
| `trade_off_technical_debt_trigger_design` | sonnet | Designing an observable repayment trigger from code metrics. |
| `trade_off_technical_debt_budget_check` | haiku | Mechanical arithmetic against the debt budget. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft-07) for the debt-record artefact |
| `templates/debt-record.md.j2` | Markdown skeleton for one debt item with Fowler quadrant + trigger |
| `templates/debt-record.md` | Markdown skeleton for one debt item with Fowler quadrant + trigger Generated from `templates/debt-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in debt-record for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trade-off-technical-debt.py` | Validate debt-record against schema + budget sanity | Pre-commit; CI on each debt-backlog change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[trade-off-stakeholder-communication]]
- [[architecture-decision-records]]
- [[refactoring-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on (a) Fowler quadrant — inadvertent-reckless escalates to ATAM not debt, (b) touch frequency — <1/quarter routes to "document and accept", (c) budget headroom — over-budget blocks new debt and forces repayment first. Every leaf references a rule in `01-core-rules.xml`.
