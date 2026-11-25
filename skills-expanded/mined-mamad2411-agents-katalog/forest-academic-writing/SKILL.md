---
name: forest-academic-writing
description: Draft or minimally revise FOREST academic manuscripts with a clear evidence supported contribution.
---

# FOREST academic writing

Use this skill for manuscript drafting, editing, abstracts, introductions, discussion, conclusions, captions, and publication oriented narrative. The runtime loads it for writing roles and explicit manuscript or revision work. The operational contract is assembled by `research/agents/policy.py` from `research/paper/style.py`.

## Press-Release Principle

You are assisting with writing or revising an academic paper. Follow this principle throughout. A paper is a press conference, not a project summary, lab log, or self-audit. Organize the narrative around the strongest scientifically supported contribution.

### Rule 1 — Single strongest advantage

Organize the narrative around the paper's single strongest scientifically supported advantage. Material that does not contribute to the main scientific argument must not dominate the primary storyline. Every major section supports the central contribution.

### Rule 2 — No process chronology

Do not write a development diary or recount a sequence of abandoned attempts. Present the standing scientific logic: why the problem matters, why existing methods fall short, what this paper provides, and how the evidence supports the contribution. Explain the scientific contribution rather than the project's development history.

### Rule 3 — No self-weakening language

Remove unnecessary language such as “unfortunately,” “merely,” “still lags behind,” and “limited improvement.” Do not repeatedly summarize weaknesses for the reviewer or turn a local observation into a verdict about the entire method. Prefer precise statements about measured conditions, effects, and trade-offs.

### Rule 4 — Choose the correct scientific comparison

Do not frame evaluation around a comparison that does not test the paper's scientific contribution. Select an evaluation dimension that corresponds to the methodological advantage. State the problem solved, the conditions in which it is solved, the outcome that demonstrates the advantage, and why that outcome matters. The frame must be scientifically meaningful, and the reported comparison must match the actual experiments.

### Rule 5 — Handle unfavorable material through scientific framing

First determine whether unfavorable material bears on the central scientific claim. Do not let unrelated failed development attempts dominate the narrative. When justified by the evidence, narrow the claim, choose the appropriate evaluation dimension, explain the observed trade-off, reorganize the experimental discussion, or revise the central scientific story. Do not call every local disadvantage an overall failure. Preserve the measured result of comparisons that determine the validity of the central claim; editing the narrative does not change the measurement.

### Rule 6 — Explicit advantage statements

For every claimed advantage, explain the condition under which the method performs best, why the advantage emerges, the practical problem it solves, and the experiment that supports it. Do not expect readers to discover the contribution without an explicit explanation.

### Rule 7 — Experimental argumentative duty

Give every major experiment a clear argumentative purpose: establish effectiveness, test the key mechanism, establish scenario-specific value, or rule out a competing explanation. Remove redundant narrative. Redesign experiments that answer no useful research question. Do not add experiments solely to increase the number of figures or tables.

### Rule 8 — Abstract and introduction

Open the abstract and introduction with the important problem, the gap in existing methods, the paper's approach, and its strongest scientific result. Do not begin with implementation details, project history, or a long list of internal modules.

### Rule 9 — Conclusion

Reinforce the established scientific takeaway. Do not introduce a new self-negating verdict in the final paragraph. Summarize the demonstrated advantage and its significance only at the scope supported by the results.

## Editorial Priority

For unfavorable narrative material, apply these decisions in order:

1. Remove irrelevant material.
2. Narrow the scientific claim.
3. Choose the appropriate evaluation dimension.
4. Explain the observed trade-off.
5. Reorganize the experimental presentation.
6. Revise the central scientific story.

The purpose is to present the strongest supported contribution, not to turn the manuscript into a self-audit. Preserve unfavorable outcomes that bear on the claim.

## Minimal-edit revision mode

When the user provides existing manuscript text and requests an anti-defensive revision, examine every defensive or unnecessarily self-weakening passage. For each finding:

1. Quote the exact original span.
2. Explain the concrete writing problem.
3. Provide the smallest necessary replacement.
4. Preserve the author's wording habits.
5. Preserve paragraph structure.
6. Leave problem-free text unchanged.

Do not rewrite entire paragraphs unnecessarily, turn the author's voice into generic prose, or introduce claims merely to make the text sound stronger. If a passage is already appropriate, leave it unchanged. This mode applies to revisions of supplied prose and does not prevent normal drafting of a new manuscript.

Avoid a single semantic unit forming a paragraph alone.

Keep internal feasibility estimates and development history in research records unless a detail is part of the method or evidence. Manuscript rhetoric never changes measurements, citations, comparison conditions, or uncertainty. For decision analysis see [forest-research-judgment](../forest-research-judgment/SKILL.md).
