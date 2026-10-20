# Architecture Health Weekly Report Template

## Summary

**One-sentence:** Weekly arch-health report: hot-spots, debt deltas, risk register movement, one decision-needed item.

**One-paragraph:** Weekly arch-health report: hot-spots, debt deltas, risk register movement, one decision-needed item. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Weekly architecture report з hot-spot deltas і risk movement.
- Single 'decision needed' item, який вимагатиме рішення комітету цього тижня.
- Tracking debt delta тиждень-до-тижня (а не накопичений borrow).

## Applies If (ALL must hold)

- Team has ≥1 architect who owns the report.
- Codebase has ≥6 months of history with measurable hot-spot data.
- Leadership expects weekly visibility on architecture risk.

## Skip If (ANY kills it)

- Codebase younger than 6 months — noise dominates the signal.
- Team has <8 engineers — informal sync is sufficient.
- No named architect — report has no owner.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Code-churn dataset | csv / git log | ci |
| Incident log | markdown / ticketing | ops |
| Risk register | markdown | architecture |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[architecture-review-meeting-facilitation]] | Report feeds the weekly architecture meeting agenda |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 4-step procedure with input/action/output per step | 1000 |
| `content/05-examples.xml` | reference | One full worked example end-to-end | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/arch-health-weekly.md.j2` | Weekly report skeleton with hot-spots, debt-delta, risk-register, decision-needed |
| `templates/arch-health-weekly.md` | Weekly report skeleton with hot-spots, debt-delta, risk-register, decision-needed Generated from `templates/arch-health-weekly.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in report for a 12-engineer team mid-quarter |
| `templates/_smoke-test.md` | Filled-in report for a 12-engineer team mid-quarter Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-arch-health-weekly-report-template.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[architecture-review-meeting-facilitation]]
- [[architecture-proposal-document-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
