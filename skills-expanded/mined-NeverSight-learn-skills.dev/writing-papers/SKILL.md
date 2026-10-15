---
name: writing-papers
description: Academic-paper drafting, review, and polishing. Use when experiment results or an algorithm need a paper structure; to draft an introduction, abstract, related work, or contribution bullets; to polish manuscript LaTeX or a NeurIPS paragraph while preserving technical claims; to review logical self-consistency, experiment narrative, captions, figure-text linkage, and evidence-bound conclusions; to write the paragraph interpreting what a result means for the contribution; or to remove AI tone. Chinese triggers include 从零开始写论文, 写摘要, 写引言, 相关工作, 起草论文, 贡献列表, 润色论文 LaTeX, 去掉 AI 味, 不改变技术主张, 首句点题, 图表 caption, 证据自洽, and 终稿红线. Do not use for answering reviewer comments on a revision, generic editing, standalone figure production, or submission packaging.
license: MIT
---

# Writing Academic Papers

Draft and revise technical papers around one evidence-backed contribution. Use only author-provided
facts, experiments, citations, and method details. Mark missing inputs as `[AUTHOR INPUT]`.

## Route

| Input state | Branch |
|---|---|
| Ideas, results, or outline without prose | Draft the missing structure and sections. |
| Existing manuscript, LaTeX, data, or figures | Review and compress the existing material. |
| Mixed material | Draft missing structure first, then review existing prose. |

All branches preserve equations, citations, labels, numbers, terminology, and uncertainty.

## Draft

Read the [drafting framework](references/drafting-framework.md) for the section-level build order
and [paper taste](references/karpathy-writing.md) for the gestalt a draft has to reach before it
reads as a paper rather than a lab report. Establish one core contribution, then make every section
support it:

1. Abstract: problem, method, and principal contribution with minimal background.
2. Introduction: problem, importance, difficulty, prior gap, approach/results/limitations, then
   contribution bullets.
3. Body: expose the contribution early and keep each section a linear, skimmable story.
4. Experiments: state what is measured, why it supports the claim, and how comparisons are fair.
5. Conclusion: restate the supported result without copying the abstract or introduction.

Drafting is complete when the requested structure is present, every empirical statement comes from
supplied evidence, and every missing fact is marked `[AUTHOR INPUT]`.

## Review and polish

Read [review dimensions](references/review-dimensions.md) for a full manuscript review and
[output modes](references/output-modes.md) for the requested deliverable.

- Trace motivation → method → experiment → figure/table → conclusion.
- Remove repeated claims, defensive patches, mechanical transitions, unsupported praise, and AI tone.
- Make paragraph openings state their role while preserving the author's technical meaning.
- Check terminology, abbreviations, captions, cross-references, metrics, and numeric consistency.
- Let figures carry dense information; prose should explain the finding and its relevance.

Classify findings as P0 blocker, P1 important, or P2 local polish. Every P0/P1 must identify evidence,
risk, and a concrete repair. A final redline with no substantive issue returns
`[PASS — no substantive issues]`.

## Completion

The requested branch is complete only when claims stay inside the evidence, LaTeX and technical
meaning are preserved, figure/text relationships have been checked where applicable, and every
unresolved author decision is explicit. Producing the figure artifacts themselves, and assembling
the files a submission screen asks for, are outside this skill.

Responding to a revision decision is a different discipline: reviewer comments are a spec to
implement, not prose to polish. Draft manuscript text here only after that work has decided what
the paper will say.
