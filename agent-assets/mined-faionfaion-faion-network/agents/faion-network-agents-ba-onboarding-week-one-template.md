# BA Week-One Onboarding Template

## Summary

**One-sentence:** Five-day, artefact-driven onboarding plan that gets a BA from "first commit" to "ready to write requirements" — day-level outputs committed to a week-one-pack/ folder.

**One-paragraph:** P4 outsource BAs rotate across projects; cost of starting blank is paid every time. This methodology fixes the sequence — Day 1 artefact pull, Day 2 stakeholder map + interview script, Day 3 glossary intake, Day 4 process baseline, Day 5 risk register + gap memo — and pins each step to a committed output. Output is a `checklist` artefact (`week-one-pack/` validator status) the BA can hand to a PM or successor without verbal context.

**Ефективно для:**

- P4 outsource BA rotation across projects every few weeks.
- New-project handoff від PM до BA з SOW + accessible workspace.
- Audit-ready discovery trail (compliance, retention).
- Mid-engagement successor handover where artefact pack still valid.

## Applies If (ALL must hold)

- BA joins project they have not worked on (or returned after >60 days).
- Project has a paying client and an existing scope document (SOW, brief).
- BA has ≥20% capacity for first 5 working days.
- ≥1 product/business owner reachable within first 3 days.

## Skip If (ANY kills it)

- Project lifetime <2 weeks.
- BA replacing an in-flight BA mid-sprint — use hand-off checklist instead.
- Pre-sales / estimation engagement — use ops-pre-sales-discovery.
- Internal product where BA is also founder — discovery informal already.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workspace read access | Confluence / Notion / Drive / Jira | engagement manager |
| Signed SOW or brief | PDF / Markdown | sales / PM |
| Kickoff calendar slot | 60-min within 48h | engagement manager |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ba-planning]] | Companion strategy doc; week-one is execution of plan |
| [[business-process-analysis]] | Day-4 process baseline reuses BPA diagram patterns |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: artefact-first, named stakeholder map, written glossary, process diagram, gap memo | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for week-one-pack manifest + examples | 700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: stakeholder-by-Slack, copy-paste glossary, missing diagram | 900 |
| `content/04-procedure.xml` | essential | Day-by-day 5-step procedure | 700 |
| `content/06-decision-tree.xml` | essential | Routing on pack-state completeness | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `artefact-inventory-from-workspace` | haiku | Mechanical listing of files + metadata. |
| `stakeholder-map-extraction` | sonnet | Reads SOW / kickoff transcript, infers roles + influence. |
| `gap-memo-synthesis` | opus | Cross-artefact reasoning: what is missing, what conflicts. |

## Templates

| File | Purpose |
|------|---------|
| `templates/week-one-pack-skeleton.md.j2` | Folder skeleton with empty README, stakeholders.md, glossary.md, processes.md, risks.md |
| `templates/week-one-pack-skeleton.md` | Folder skeleton with empty README, stakeholders.md, glossary.md, processes.md, risks.md Generated from `templates/week-one-pack-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/kickoff-interview-script.md.j2` | 12 standard kickoff questions + recording-consent prompt |
| `templates/kickoff-interview-script.md` | 12 standard kickoff questions + recording-consent prompt Generated from `templates/kickoff-interview-script.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable pack manifest |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ba-onboarding-week-one-template.py` | Validate pack manifest against output-contract; confirm all required files present | End of Day 5 + pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ba-planning]]
- [[business-process-analysis]]
- [[ba-to-qa-handoff-template]]
- [[ba-standup-script-template]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on pack state (which day's output is missing) to the rule firing. Use when reviewing whether Day-5 sign-off is achievable.
