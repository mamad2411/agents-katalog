# Tool-Call Schema Design Checklist

## Summary

**One-sentence:** Produces a single design-this-tool-correctly checklist that bundles verb-object naming, description-as-prompt, bundle-vs-split, idempotent-write, structured-errors, enum-constraints, terse-default-output into one pass over a new tool-call schema.

**Ефективно для:** LLM-agent developers drafting a new tool schema before shipping; reviewers gating tool PRs; platform owners standardising tool-card shape across teams.

**One-paragraph:** This methodology pins the recurring decision around "tool-call-schema-design-checklist" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- A new tool-call schema is being authored or reviewed.
- Tool will be exposed to an LLM agent (not internal-only API).
- Owner exists for the resulting tool card.
- Schema target is JSON Schema / OpenAPI / Anthropic tool spec.

## Skip If (ANY kills it)

- Tool is internal-only with no LLM caller — REST-design rules apply, not this checklist.
- Single-throwaway tool used for one experiment.
- Wrapper around an existing tool with identical schema — re-use original card.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Draft tool schema | JSON Schema / OpenAPI | tool author |
| Existing similar tool cards | directory | platform repo |
| Caller agent system prompt | text | agent owner |
| Owner for the new tool | handle / email | team roster |

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
| `draft_checklist_pass` | haiku | Mechanical field-by-field review. |
| `synthesize_revision` | sonnet | Per-schema judgment when a field fails. |
| `escalate_ambiguity` | opus | When the tool itself is mis-scoped. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool-call-schema-design-checklist.json` | JSON Schema for the Tool-Call Schema Design Checklist output contract |
| `templates/tool-call-schema-design-checklist.md.j2` | Markdown skeleton with the required fields |
| `templates/tool-call-schema-design-checklist.md` | Markdown skeleton with the required fields Generated from `templates/tool-call-schema-design-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tool-call-schema-design-checklist.py` | Enforce the Tool-Call Schema Design Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[tool-card-template]] — produces the artefact this checklist gates.
- [[tool-trust-boundary-model]] — deeper trust-boundary review.
- [[verb-object-tool-naming]] — single field methodology this rolls up.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
