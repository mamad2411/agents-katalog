---
name: dissertation-literature-review
description: Plan, review, and synthesize literature for a dissertation on AI agents, active learning, higher education, teacher adoption, co-design, educational technology, and responsible AI in teaching.
---

# Dissertation Literature Review

Use when the user asks for literature review help, concept mapping, research gaps, source screening, or synthesis.

For new searches or source discovery, use `dissertation-research-search-protocol` first. After useful new reading, use `dissertation-learning-loop` to preserve evidence boundaries and implications. Use this skill after sources exist or when building the literature review argument from already screened sources.

## Inputs

Look for:

- `DISSERTATION_BRIEF.md`
- `research-wiki/LITERATURE_MAP.md`
- existing chapter drafts
- bibliography files, reference lists, PDFs, notes, or Zotero exports if present

## Workflow

1. Identify the review question and scope.
2. If new sources are needed, run `dissertation-research-search-protocol` to create a source map before synthesis.
3. Organize sources into clusters:
   - active learning in higher education
   - AI agents for teaching and learning support
   - teacher perceptions, concerns, and adoption
   - co-design and participatory design in education
   - responsible AI, trust, workload, autonomy, and assessment
4. For each cluster, summarize:
   - key concepts
   - major debates
   - representative sources
   - relevance to this dissertation
   - gaps or tensions
5. Build a synthesis matrix instead of a source-by-source summary.
6. Mark any weak, missing, or unverified citations.

## Outputs

Prefer creating or updating:

- `research-wiki/LITERATURE_MAP.md`
- `research-wiki/LITERATURE_GAPS.md`
- `chapter-plans/LITERATURE_REVIEW_PLAN.md`

## Guardrails

Read `../dissertation-shared/references/citation-discipline.md` before producing citation-heavy text.
Do not invent references. If exact source details are missing, mark them as `NEEDS VERIFICATION`.
