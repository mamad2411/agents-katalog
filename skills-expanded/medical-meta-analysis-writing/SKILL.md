---
name: medical-meta-analysis-writing
description: Write medical systematic reviews and meta-analyses using a strict stepwise workflow aligned with PRISMA 2020, Cochrane, MOOSE, GRADE, and JAMA-style manuscript expectations. Use this skill when planning, screening, extracting, synthesizing, grading evidence, and drafting a publication-grade medical meta-analysis.
---

# Medical Meta-analysis Writing

## When to Use

Use this skill when the task is to plan, execute, write, revise, or audit a medical or clinical systematic review with or without quantitative meta-analysis. This skill is designed for publication-grade work rather than generic literature summaries.

Typical triggers:
- Draft a medical SCI meta-analysis
- Plan a systematic review and meta-analysis protocol
- Build PRISMA-compliant screening and exclusion logic
- Extract study data and assess risk of bias
- Choose effect measures and synthesis structure
- Write a JAMA-style title, Key Points, abstract, and manuscript
- Stress-test a meta-analysis before submission

## Default Policy

Apply these defaults unless the user explicitly overrides them:
- English-language full-text literature only
- Exclude grey literature, conference abstracts, dissertations, protocols, and preprints
- Default journal style: JAMA-like medical manuscript structure and tone
- Default review type: pairwise medical or clinical systematic review and meta-analysis
- Default interpretation style: conservative, evidence-proportionate, non-promotional
- Observational evidence should not be framed causally unless clearly justified

## Workflow Gatekeeping Rules

Do not skip these gates:
- Do not proceed to statistical synthesis or manuscript drafting before protocol-level decisions are stable. Load [prompt-module-1-protocol.md](references/prompt-module-1-protocol.md).
- Do not produce PRISMA narrative text until full-text screening and exclusion logging are complete. Load [prompt-module-2-search-screening.md](references/prompt-module-2-search-screening.md).
- Inclusion in the systematic review does not automatically imply inclusion in quantitative synthesis. Load [prompt-module-3-extraction-bias.md](references/prompt-module-3-extraction-bias.md).
- Do not start pooled synthesis until candidate synthesis sets and pooling eligibility are defined. Load [prompt-module-4-statistical-synthesis.md](references/prompt-module-4-statistical-synthesis.md).
- Do not write strong conclusions before certainty of evidence is assessed. Load [prompt-module-5-grade-displays.md](references/prompt-module-5-grade-displays.md).
- If quantitative synthesis is not justified or not performed, downgrade the article type and front matter from meta-analysis to systematic review.

## Workflow Map

Follow the workflow in order:
1. Topic feasibility, question framing, and protocol drafting
2. Search strategy, title/abstract screening, and full-text exclusion logging
3. Data extraction, risk-of-bias assessment, and pooling eligibility decisions
4. Effect measure selection, primary synthesis, heterogeneity, subgroup, sensitivity, and publication-bias analysis
5. GRADE certainty assessment, Summary of Findings logic, and figure/table package design
6. JAMA-style front matter and full manuscript drafting
7. Submission audit, reviewer simulation, and cover letter preparation

For the full dependency map, load [workflow-overview.md](references/workflow-overview.md).

## Which Reference File to Load

Load only the files needed for the current stage:
- Methodological hard rules: [methodology-core.md](references/methodology-core.md)
- Workflow dependencies and stage inputs/outputs: [workflow-overview.md](references/workflow-overview.md)
- Topic framing and protocol prompts: [prompt-module-1-protocol.md](references/prompt-module-1-protocol.md)
- Search, screening, and PRISMA prompts: [prompt-module-2-search-screening.md](references/prompt-module-2-search-screening.md)
- Extraction, bias, and pooling-eligibility prompts: [prompt-module-3-extraction-bias.md](references/prompt-module-3-extraction-bias.md)
- Statistical synthesis prompts: [prompt-module-4-statistical-synthesis.md](references/prompt-module-4-statistical-synthesis.md)
- GRADE, Summary of Findings, and display prompts: [prompt-module-5-grade-displays.md](references/prompt-module-5-grade-displays.md)
- Title, abstract, IMRAD, and conclusion prompts: [prompt-module-6-manuscript-writing.md](references/prompt-module-6-manuscript-writing.md)
- Submission audit, reviewer simulation, and cover letter prompts: [prompt-module-7-submission-review.md](references/prompt-module-7-submission-review.md)
- JAMA-facing style constraints: [journal-style-jama.md](references/journal-style-jama.md)

## Output Standards

Unless the user asks otherwise:
- Final manuscript prose should be in English
- Working explanations and methodological reasoning may be in Chinese
- Report effect estimates with uncertainty, not p-values alone
- Distinguish pre-specified analyses from exploratory analyses
- Distinguish narrative-only inclusion from pooling-ready inclusion
- Keep claims aligned with risk of bias, heterogeneity, and GRADE certainty
- Prefer honest downgrading over overstated synthesis
