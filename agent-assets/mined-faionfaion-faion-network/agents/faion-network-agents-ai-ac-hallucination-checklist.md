# AI Acceptance Criteria Hallucination Checklist

## Summary

**One-sentence:** Produces a per-story checklist that vets AI-generated acceptance criteria for plausible-but-wrong shapes: invented happy paths, missing edge cases, fabricated metrics, contradictory constraints, before ACs enter sprint.

**Ефективно для:** BAs gating AI-generated acceptance criteria; QA leads catching AC hallucinations before sprint start; PMs reviewing AI-drafted stories.

**One-paragraph:** This methodology pins the recurring decision around "ai-ac-hallucination-checklist" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Acceptance criteria drafted by an LLM (or LLM-assisted).
- Story will enter a sprint backlog after this gate.
- Owner exists for the AC review.
- Story is for a software / agent feature, not pure research.

## Skip If (ANY kills it)

- ACs are fully human-authored — apply standard AC review.
- Story is a spike / research task with no production output.
- Single-story experiment with no downstream impact.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| AI-drafted acceptance criteria | Markdown / Gherkin | BA |
| Source requirement record | spec id | BA |
| Definition-of-done reference | Markdown | engineering lead |
| Owner for review | handle / email | team roster |
| Existing edge-case catalogue | Markdown | QA |

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
| `draft_checklist_pass` | haiku | Mechanical AC walk-through. |
| `synthesize_revision` | sonnet | Per-AC judgment when a check fails. |
| `escalate_ambiguity` | opus | When two checks contradict. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-ac-hallucination-checklist.json` | JSON Schema for the AI Acceptance Criteria Hallucination Checklist output contract |
| `templates/ai-ac-hallucination-checklist.md.j2` | Markdown skeleton with the required fields |
| `templates/ai-ac-hallucination-checklist.md` | Markdown skeleton with the required fields Generated from `templates/ai-ac-hallucination-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-ac-hallucination-checklist.py` | Enforce the AI Acceptance Criteria Hallucination Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-story-truth-checklist]] — sister checklist on user stories.
- [[ai-transcript-to-traceable-requirement]] — upstream traceability.
- [[ai-enabled-business-analysis]] — parent methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
