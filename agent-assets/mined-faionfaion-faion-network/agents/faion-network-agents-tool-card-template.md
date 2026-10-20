# Tool Card Template

## Summary

**One-sentence:** Produces a one-page tool card combining name, description-as-prompt, schema, error codes, eval rows, and owners — the artefact other tool-design methodologies feed into.

**Ефективно для:** LLM-agent developers shipping a new tool to a paying agent surface; platform owners standardising tool-card shape across teams; PMs requesting a single ground-truth tool spec.

**One-paragraph:** This methodology pins the recurring decision around "tool-card-template" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- A new tool is being added to an LLM agent surface.
- Tool will be invoked by an autonomous or supervised agent.
- Owner exists for the tool card after publication.
- Eval rows can be supplied (≥3 representative call examples).

## Skip If (ANY kills it)

- Tool is internal-only with no LLM caller.
- Tool is a thin wrapper around an existing tool with identical card — link the original.
- Throwaway tool for a single experiment with no ongoing maintenance.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool schema draft | JSON Schema / OpenAPI | tool author |
| 3+ eval call examples | JSONL | tool author |
| Owner + on-call rotation | handle / email | team roster |
| Description-as-prompt draft | text | tool author |
| Sample errors and remediations | JSON | tool author |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[tool-call-schema-design-checklist]]` | field-by-field schema gate runs first |

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
| `draft_card_fields` | haiku | Template fill from inputs. |
| `synthesize_description` | sonnet | Description-as-prompt requires judgment. |
| `trust_boundary_review` | opus | Cross-tool risk assessment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool-card-template.json` | JSON Schema for the Tool Card Template output contract |
| `templates/tool-card-template.md.j2` | Markdown skeleton with the required fields |
| `templates/tool-card-template.md` | Markdown skeleton with the required fields Generated from `templates/tool-card-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a tool-card-template record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a tool-card-template record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tool-card-template.py` | Enforce the Tool Card Template output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[tool-call-schema-design-checklist]] — gates the card before publication.
- [[tool-deprecation-lifecycle]] — sister methodology covering sunset.
- [[tool-trust-boundary-model]] — trust boundary block on the card.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
