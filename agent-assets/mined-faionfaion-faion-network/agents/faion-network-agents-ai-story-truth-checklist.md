# AI Story Truth Checklist

## Summary

**One-sentence:** Produces a per-story checklist that vets AI-generated user stories for plausible-but-wrong shapes: invented personas, conflated jobs, fabricated metrics, missing edge cases — before they enter the backlog.

**Ефективно для:** BAs running AI-assisted story drafting; PMs gating LLM-drafted backlog entries; QA leads detecting story-level hallucinations early.

**One-paragraph:** This methodology pins the recurring decision around "ai-story-truth-checklist" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- User stories drafted by an LLM (or LLM-assisted).
- Stories will enter a sprint backlog after this gate.
- Owner exists for the story review.
- Persona / job catalogue exists OR can be supplied.

## Skip If (ANY kills it)

- Stories are fully human-authored — apply standard story review.
- Spike / research story with no production output.
- Single-story experiment with no downstream impact.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| AI-drafted user story | Markdown | BA |
| Persona catalogue | Markdown / CSV | PM |
| Job catalogue (JTBD) | Markdown / CSV | PM |
| Owner for review | handle / email | team roster |
| Source requirement id | spec id | BA |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[ai-transcript-to-traceable-requirement]]` | source requirement has a provenance trail |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/06-decision-tree.xml` | essential | run / skip / variant router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_checklist_pass` | haiku | Mechanical story walk-through. |
| `synthesize_revision` | sonnet | Per-story judgment when a check fails. |
| `escalate_contradiction` | opus | When persona + job + AC conflict. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-story-truth-checklist.json` | JSON Schema for the AI Story Truth Checklist output contract |
| `templates/ai-story-truth-checklist.md.j2` | Markdown skeleton with the required fields |
| `templates/ai-story-truth-checklist.md` | Markdown skeleton with the required fields Generated from `templates/ai-story-truth-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-story-truth-checklist.py` | Enforce the AI Story Truth Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-ac-hallucination-checklist]] — sister checklist on acceptance criteria.
- [[ai-transcript-to-traceable-requirement]] — upstream provenance.
- [[ai-enabled-business-analysis]] — parent methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
