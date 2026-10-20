# Prompt PR Review Checklist

## Summary

**One-sentence:** Pause-point READ-DO checklist for every prompt-change PR — 7 killer-anchored items each with executor + artefact + incident-id reference.

**One-paragraph:** Prompt edits are the #1 cause of silent production regressions, but most teams have no PR-review checklist for them analogous to code review. This methodology produces a `prompt-pr-checklist.json` artefact with 5–9 items per pause-point, each anchored to a past incident or policy line. Output is a versioned checklist consumed at every prompt PR; reviewers cannot merge without filling executor + artefact + sign-off per item.

**Ефективно для:**

- Прев'юбати prompt PR перед merge — кожне item має killer-anchor (incident_id).
- READ-DO режим: executor читає item → робить → ставить артефакт.
- DO-CONFIRM режим (high-stakes prompt) — second reviewer confirms.
- Quarterly refresh checklist — кожне item треба перевіряти, чи його killer-anchor ще валідний.
- Бридж з [[prompt-ab-power-calculator]] — items вимагають power-calc spec link.

## Applies If (ALL must hold)

- Repository hosts prompt files reviewed via PR.
- Named owner accountable for checklist refresh.
- Checklist refresh cadence ≥ quarterly.
- Team agrees on READ-DO vs DO-CONFIRM mode per pause-point.

## Skip If (ANY kills it)

- No prompt PRs (prompts edited live in production console).
- Single-person team without PR review — use a personal review skill.
- No owner — defer.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Incident log (past prompt regressions) | JSONL | platform |
| Policy doc (refusal style, safety) | Markdown | safety repo |
| Pause-point definition (when reviewer pauses) | YAML | review policy |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[prompt-ab-power-calculator]]` | Power calc spec link required per item. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + run/skip terminals | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for prompt-pr-checklist + examples | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns | ~900 |
| `content/06-decision-tree.xml` | essential | Routes PR risk to READ-DO or DO-CONFIRM mode | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `assemble-items` | sonnet | Per-item judgment from incident log. |
| `verify-killer-anchor` | haiku | Mechanical incident-id lookup. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-pr-checklist.json` | JSON skeleton matching 02-output-contract. |
| `templates/prompt-pr-checklist.md.j2` | Markdown checklist for PR template. |
| `templates/prompt-pr-checklist.md` | Markdown checklist for PR template. Generated from `templates/prompt-pr-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-pr-review-checklist.py` | Validate prompt-pr-checklist | Pre-commit on the checklist itself |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[prompt-ab-power-calculator]]
- [[prompt-portability-audit]]
- [[provider-deprecation-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree picks READ-DO vs DO-CONFIRM mode based on PR risk (touched file count + production traffic exposure). Walk it before assigning pause-point mode.
