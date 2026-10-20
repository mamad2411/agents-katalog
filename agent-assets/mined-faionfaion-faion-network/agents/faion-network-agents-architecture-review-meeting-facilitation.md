# Architecture Review Meeting Facilitation

## Summary

**One-sentence:** Playbook step to facilitate the weekly architecture review: pre-read, deliberation rules, decision capture, follow-up.

**One-paragraph:** Playbook step to facilitate the weekly architecture review: pre-read, deliberation rules, decision capture, follow-up. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Run weekly architecture review з прочитаним pre-read і structured deliberation.
- Decision capture: записані decision + dissent + follow-ups — а не 'we agreed, sort of'.
- Follow-up loop: previous-meeting decisions перевіряються next meeting.

## Applies If (ALL must hold)

- Org has a recurring architecture review (weekly / biweekly).
- Pre-read material is shared ≥24h before the meeting.
- Named facilitator owns the agenda and the decision log.

## Skip If (ANY kills it)

- Ad-hoc one-off meeting — use the lightweight ADR flow instead.
- No pre-read culture — fix that first or the meeting fails.
- Decision is already made and meeting is theater — cancel.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pre-read material | markdown | proposal author |
| Agenda | markdown | facilitator |
| Decision log | markdown | facilitator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[architecture-proposal-document-template]] | Proposals feed the meeting agenda |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output per step | 1000 |
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
| `templates/review-facilitation-step.md.j2` | Playbook step skeleton with pre-meeting / in-meeting / post-meeting phases |
| `templates/review-facilitation-step.md` | Playbook step skeleton with pre-meeting / in-meeting / post-meeting phases Generated from `templates/review-facilitation-step.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/decision-log.md.j2` | Decision log template with decision + dissent + follow-ups |
| `templates/decision-log.md` | Decision log template with decision + dissent + follow-ups Generated from `templates/decision-log.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in playbook for one review session |
| `templates/_smoke-test.md` | Filled-in playbook for one review session Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-architecture-review-meeting-facilitation.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[architecture-proposal-document-template]]
- [[arch-health-weekly-report-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
