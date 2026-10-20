# Agent GA-Readiness Checklist

## Summary

**One-sentence:** Produces a single-page GA-readiness checklist with ~12 items across auth, rate-limits, billing, eval bar, runbook, rollback, kill switch — gates pilot→GA transition with auditable skips.

**One-paragraph:** Geek-tier builders ship to small numbers of paying customers. They need a hardened checklist (auth, rate-limits, billing, eval bar, runbook, rollback) before flipping pilot → GA. Right now this is buried in vendor blog posts. This produces a one-screen checklist + skip-with-reason policy.

**Ефективно для:** pre-GA agent launches; quarterly re-readiness audits; agency-managed agent launches needing a checklist for client sign-off.

## Applies If (ALL must hold)

- You operate the recurring activity at least once per cycle (sprint, quarter, or annual)
- You have authority to act on each item — checklist items without owners or budget are deferred
- Skipped items must be auditable: a written reason replaces the action
- Time-box: full pass completes within the cycle window (30-90 min for sprint, 1-2 days for annual)

## Skip If (ANY kills it)

- One-off events with no recurrence — checklist value is in the rhythm
- Activities without a named owner — items will not be done, only ticked
- Teams running a more granular checklist already — adding a meta-layer creates conflict

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Agent in pre-prod with paying users planned | deploy | eng |
| Observability stack live | OTel + dashboards | observability |
| Eval baseline ≥85% (or team-defined bar) | eval suite | eval owner |
| Runbook draft | Markdown | on-call lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[agent-kill-switch-design]]` | Safety control |
| `[[agent-observability-stack-blueprint]]` | Observability |
| `[[agent-eval-harness-bootstrap-recipe]]` | Eval bar gate |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale and source | ~500 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Fill checklist | sonnet | Mechanical. |
| Verify eval bar | sonnet | Stat check. |
| Sign-off judgement | opus | Cross-item risk weighting. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md.j2` | Filled example for a customer-support agent GA. |
| `templates/_smoke-test.md` | Filled example for a customer-support agent GA. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-ga-readiness-checklist.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- `[[agent-kill-switch-design]]`
- `[[agent-customer-zero-pilot-protocol]]`
- `[[agent-eval-harness-bootstrap-recipe]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether agent-ga-readiness-checklist applies: root question — "Are you flipping a pilot to GA in the next 2 weeks?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
