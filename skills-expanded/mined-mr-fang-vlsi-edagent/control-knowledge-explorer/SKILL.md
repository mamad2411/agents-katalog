---
name: control-knowledge-explorer
description: Explore and structure local EDA knowledge, identify evidence gaps, and prepare targeted literature retrieval tasks for local download and follow-up parsing.
---

# Control Knowledge Explorer

## When to use

Use this skill at the start of a research topic or when evidence is fragmented across KB, logs, and papers.

## Knowledge And Tool Interaction

1. Use `eda-context-accessor` when the task first needs a shared scoped KB/tool snapshot before deeper evidence-gap mapping begins.
2. Treat the local knowledge base as the primary evidence source once exploration starts.
3. Write outputs as reusable knowledge artifacts that later skills can consume directly.

## Workflow

1. Read core KB context and recent experiment summaries.
2. Build a gap map:
- known claims,
- uncertain assumptions,
- missing evidence.
3. For missing external evidence, delegate to `eda-paper-fetch` and generate a local download queue.
4. If local PDFs are available, delegate parse/summarize to `eda-pdf-local-summary`.
5. Produce explicit research questions that can be tested in later experiment design.

## Outputs

1. `knowledge_gap_map.md`
2. `paper_download_queue.tsv`
3. `evidence_to_question_map.md`

## Hard rules

1. Distinguish confirmed evidence from hypotheses.
2. Do not present unsourced claims as conclusions.
3. Keep file/path-level references for each key claim.

## Reference

Load when needed:
1. `references/exploration-checklist.md`
