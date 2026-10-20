# BA Standup Script Template

## Summary

**One-sentence:** 3-bullet BA-specific standup script (clarifications-needed / AC-ready / blockers) replacing dev-style updates, captured as a typed daily artefact.

**One-paragraph:** BAs default to dev-style "what I did / what I will do" standup updates, which add noise without surfacing the BA-specific signal (open clarifications, AC ready for dev pull, blockers needing stakeholder attention). This methodology pins a 3-bullet script per day with named owners per blocker and a stable schema. Output is a daily `checklist` JSON the scrum master + dev lead can scan in 10 seconds.

**Ефективно для:**

- Daily Scrum / standup BA participation у multi-discipline teams.
- Slack-async standup channels де update is text-only.
- Audit trail BA контрибуцій для performance review.
- Multi-BA team sync — типована структура полегшує aggregation.

## Applies If (ALL must hold)

- BA participates in a daily/recurring standup or async update channel.
- Output is consumed by scrum master, dev lead, or PM.
- BA owns ≥1 actionable AC or clarification per sprint.
- Standup runs at consistent cadence (daily or 3×/week minimum).

## Skip If (ANY kills it)

- Solo BA with no daily sync.
- Async-only project where standups do not exist.
- BA off-engagement (PTO, training week).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Sprint backlog | Jira / Linear | scrum master |
| Open-clarifications log | Markdown / Notion | BA |
| Blocker registry | Slack / tracker | BA |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[acceptance-criteria]] | Day-to-day AC pipeline this script reports against |
| [[ba-to-qa-handoff-template]] | Sibling that consumes "AC-ready" bullets at sprint end |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: bound scope, typed input, named owner per blocker, versioned per day | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (3-bullet shape) + examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: dev-style update, anonymous blocker, blocker without owner, etc. | 800 |
| `content/06-decision-tree.xml` | essential | Routing on signal-shape | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Mechanical template fill from yesterday's state. |
| `synthesize_blockers` | sonnet | Bounded judgment on which open items rise to "blocker". |

## Templates

| File | Purpose |
|------|---------|
| `templates/standup-script.json` | Daily 3-bullet skeleton with required fields |
| `templates/_smoke-test.json` | Minimum viable filled standup script |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ba-standup-script-template.py` | Validate daily script against output-contract | Before posting to standup channel |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[acceptance-criteria]]
- [[ba-to-qa-handoff-template]]
- [[ba-onboarding-week-one-template]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on script-state (clarifications/AC-ready/blockers populated?) to the active rule.
