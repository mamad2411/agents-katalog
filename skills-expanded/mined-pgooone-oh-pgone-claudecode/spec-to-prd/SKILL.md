---
name: spec-to-prd
description: Structured pipeline for turning dense technical documents into actionable artifacts. When a user provides any specification, tender, RFP, procurement document, contract, vendor datasheet, or requirements-heavy document and wants to analyze it, translate it, extract requirements from it, build a glossary, do a technical risk analysis, write a PRD, create a traceability matrix, or break it down systematically — use this skill. Covers the full chain from document intake through structured parsing, bilingual glossary building, deep technical analysis with risk flagging, faithful translation with translator notes, and exhaustive requirements PRD with FR/NFR IDs, priority levels, acceptance criteria, and source traceability. Also use for partial requests like "translate this spec", "build a glossary from this document", "extract requirements from this RFP", "analyze this tender for risks", or "write a PRD from this procurement specification". Triggers on keywords including spec, specification, tender, RFP, bid, procurement, contract, datasheet, requirements document, PRD, glossary, traceability matrix, technical analysis, risk analysis, requirements extraction.
---

# Spec to PRD Pipeline

Turn a dense source document into a set of artifacts a delivery or bid team can act on. The value is in the *chain*: each artifact feeds the next, so the final PRD is traceable all the way back to the source.

## Outputs

Produce these five artifacts, in order:

1. **Structured text parse** — faithful, section-by-section extraction of the source.
2. **Glossary** — source-to-target term table with definitions.
3. **Technical analysis** — architecture, protocols, constraints, risks, ambiguities.
4. **Translation** — complete, faithful translation into the target language.
5. **Requirements PRD** — exhaustive, itemized PRD derived from the translation.

Collect all five under one container so they cross-reference each other.

## When to use

Trigger whenever someone hands you a spec/tender/RFP/contract/datasheet and wants extraction, translation, a glossary, technical analysis, or a PRD. A single-output request still warrants offering the whole chain, because the artifacts reinforce one another — a glossary makes the translation consistent, the parse makes the PRD complete.

## How to run

Read references/workflow.md first; it covers intake and the order of operations. Then work each stage, reading its reference file before producing that artifact:

- references/text-parsing.md
- references/glossary.md
- references/technical-analysis.md
- references/translation.md
- references/prd.md

Assemble the deliverables per references/output-structure.md.

## Principles that make this work

- **Faithful before helpful.** Never invent a requirement. If the source is silent, say so; do not fill the gap with a plausible guess.
- **Flag, do not fix, contradictions.** Real specs contradict themselves (for example two sections give different retention periods). Record each contradiction as an open item with both source references rather than silently picking one.
- **Distrust machine translation.** Many source documents are themselves machine-translated. Watch for mangled symbols, false friends, and units. Note suspected artifacts instead of trusting them.
- **Trace everything.** Each PRD requirement should point back to a source section. A traceability matrix is the bridge between what they wrote and what we will build.
- **Stay domain-neutral.** This skill carries no domain content of its own. Derive all terminology and structure from the source in front of you; do not import vocabulary from past runs.
