# AI-Enabled Business Analysis

## Summary

**One-sentence:** Produces a methodology spec for AI-assisted BA workflows: requirements extraction via NLP, stakeholder sentiment analysis, process discovery, AI-accelerated BA docs, agentic system specs, with AI TRiSM compliance gates.

**Ефективно для:** BAs integrating LLMs into requirements / process / acceptance-criteria workflows; BA leads standardising the AI-BA toolchain; compliance reviewers gating AI-BA outputs under AI TRiSM.

**One-paragraph:** This methodology pins the recurring decision around "ai-enabled-business-analysis" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Team has BA function with ≥1 LLM-assisted workflow live or planned.
- Source corpora include documents (contracts / RFPs) or transcripts.
- Compliance regime applies (GDPR / SOC2 / AI TRiSM-aligned).
- Owner exists for the BA methodology.

## Skip If (ANY kills it)

- BA team has no LLM access and no plan to add one.
- Domain is too specialised — model hallucinates on terms.
- Stakeholder dynamics make AI analysis of communications ethically inappropriate.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Source corpora | PDF / DOCX / transcript | engagement |
| Domain glossary | Markdown | BA lead |
| Sentiment corpus consent | CSV | trust + safety |
| BA methodology owner | handle / email | team roster |
| AI TRiSM gate checklist | Markdown | compliance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[ai-transcript-to-traceable-requirement]]` | interview-extraction sub-flow |

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
| `extract_requirements` | sonnet | Document-corpus extraction with judgment. |
| `synthesize_acceptance_criteria` | sonnet | Per-requirement AC generation. |
| `escalate_trism_gate` | opus | Compliance-gate decisions touch multiple regimes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-enabled-business-analysis.json` | JSON Schema for the AI-Enabled Business Analysis output contract |
| `templates/ai-enabled-business-analysis.md.j2` | Markdown skeleton with the required fields |
| `templates/ai-enabled-business-analysis.md` | Markdown skeleton with the required fields Generated from `templates/ai-enabled-business-analysis.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a ai-enabled-business-analysis record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a ai-enabled-business-analysis record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-transcript-to-traceable-requirement]] — adjacent extraction step.
- [[ai-ac-hallucination-checklist]] — adjacent acceptance-criteria gate.
- [[compliance-traceability-pack]] — adjacent regulatory pack.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
