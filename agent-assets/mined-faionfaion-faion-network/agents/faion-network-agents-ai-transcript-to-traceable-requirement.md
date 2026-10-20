# AI Transcript to Traceable Requirement

## Summary

**One-sentence:** Produces a traceable requirement record from a stakeholder-interview transcript: requirement statement, source quote, stakeholder owner, ambiguity flag, and link to the verbatim moment in the transcript.

**Ефективно для:** BAs running AI-assisted stakeholder interview capture; PMs converting verbatim into traceable backlog items; auditors checking requirement provenance.

**One-paragraph:** This methodology pins the recurring decision around "ai-transcript-to-traceable-requirement" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Stakeholder interview captured as transcript (recorded + transcribed).
- Requirements will be extracted and tracked downstream.
- Owner exists for requirement record after publication.
- Transcript permissions allow content extraction.

## Skip If (ANY kills it)

- Interview not recorded; only memory notes — provenance impossible.
- Stakeholder is anonymous / un-attributable.
- Free brainstorm with no requirement intent.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Interview transcript | text / JSON with timestamps | interview capture tool |
| Stakeholder roster | CSV | PM |
| Requirement template | Markdown / spec | BA |
| Owner for resulting record | handle / email | team roster |
| Ambiguity taxonomy | Markdown | BA lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[ai-enabled-business-analysis]]` | BA workflow with LLM assistance is in place |

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
| `draft_extraction` | sonnet | Per-snippet requirement extraction with judgment. |
| `synthesize_ambiguity` | sonnet | Ambiguity classification. |
| `escalate_conflict` | opus | When two stakeholders contradict each other. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-transcript-to-traceable-requirement.json` | JSON Schema for the AI Transcript to Traceable Requirement output contract |
| `templates/ai-transcript-to-traceable-requirement.md.j2` | Markdown skeleton with the required fields |
| `templates/ai-transcript-to-traceable-requirement.md` | Markdown skeleton with the required fields Generated from `templates/ai-transcript-to-traceable-requirement.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a ai-transcript-to-traceable-requirement record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a ai-transcript-to-traceable-requirement record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-transcript-to-traceable-requirement.py` | Enforce the AI Transcript to Traceable Requirement output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-enabled-business-analysis]] — parent methodology.
- [[ai-ac-hallucination-checklist]] — adjacent acceptance-criteria gate.
- [[compliance-traceability-pack]] — downstream regulatory pack.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
