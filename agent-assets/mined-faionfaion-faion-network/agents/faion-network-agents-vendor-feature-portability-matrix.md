# Vendor Feature Portability Matrix

## Summary

**One-sentence:** Produces a portability matrix comparing LLM-vendor feature parity (tool use, JSON mode, streaming, vision, batch, caching) with a migration delta + risk per feature for moving from lock-in to a multi-vendor gateway.

**Ефективно для:** platform leads planning a multi-model gateway migration; finance / procurement on vendor concentration risk; PMs scoping a 2-month migration sprint.

**One-paragraph:** This methodology pins the recurring decision around "vendor-feature-portability-matrix" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Team currently single-vendor with material spend (≥$5k/month) on LLM.
- ≥2 candidate vendors exist with overlapping capability.
- A migration timeline (≤6 months) is on the table.
- Owner exists for the matrix after publication.

## Skip If (ANY kills it)

- Single-vendor lock-in is contractually required (e.g., regulated long-term agreement).
- Team budget too small to justify the audit overhead (<$500/mo).
- Roadmap requires a vendor-specific feature with no parity (e.g., specific tool integration).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current vendor + feature usage report | CSV | platform telemetry |
| Candidate vendor feature docs | URL list | procurement |
| Migration timeline | calendar | PM |
| Owner for the matrix | handle / email | team roster |
| Eval row set for capability tests | JSONL | RAG / agent owner |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip / variant router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_matrix_grid` | haiku | Feature-grid template fill. |
| `synthesize_migration_delta` | sonnet | Per-feature delta + risk. |
| `escalate_blocker` | opus | Cross-feature gating decision. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vendor-feature-portability-matrix.json` | JSON Schema for the Vendor Feature Portability Matrix output contract |
| `templates/vendor-feature-portability-matrix.md.j2` | Markdown skeleton with the required fields |
| `templates/vendor-feature-portability-matrix.md` | Markdown skeleton with the required fields Generated from `templates/vendor-feature-portability-matrix.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a vendor-feature-portability-matrix record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a vendor-feature-portability-matrix record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vendor-feature-portability-matrix.py` | Enforce the Vendor Feature Portability Matrix output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[fine-tune-vs-prompt-decision-tree]] — depth axis on vendor lock-in.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
