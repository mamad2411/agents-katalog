---
name: locate-review-research-gap
description: "Locate a concrete, defensible research gap from a literature review synthesis and convert it into an executable future research direction. Use when the user is writing the conclusion, research outlook, thesis proposal significance, or contribution section and needs to avoid vague phrases like \"more research is needed\" by connecting question, modules, method limits, contradictions, and a specific next study. 触发词：研究空白、研究gap、研究展望、创新点。"
metadata:
  version: "0.3.0"
---

# Locate Review Research Gap

## Discipline And Interview Setup

Read [discipline-routing.md](references/discipline-routing.md), then only the selected discipline profile. Reuse the user's existing brief; do not restart intake at each stage. For journalism/communication or information science, use that profile's concepts, extraction fields, and appraisal checks instead of a generic social-science template.

When the user requests "grill me", 追问, or 模拟答辩, read [research-interview.md](references/research-interview.md). Ask one decision-relevant question per turn and wait; do not generate the stage deliverable until enough decisions are settled or the user asks to proceed. In quick/no-question mode, record assumptions and continue without inventing answers.

For evidence extraction or drafting, read [review-workflow.md](references/review-workflow.md). With no sources, give a plan or outline, not a purported synthesis. If reference files are unavailable, retain the source guardrails below and state that discipline guidance is missing.

## Goal

Turn a literature review's ending from generic "future research" into a specific, justified research direction: what predecessors have done, where the explanation gets stuck, where to cut in, and why that move matters.

## Workflow

1. Restate the question anchor.
2. Summarize progress within the reviewed corpus, not automatically the whole field. State the search coverage and distinguish supported convergence from unresolved questions; neither consensus nor contradiction is mandatory.
3. Identify where progress gets stuck: theory gap, method limitation, data blind spot, context boundary, variable/mechanism omission, or contradictory evidence.
4. Select one cut-in point: a module, mechanism, variable relation, context, population, time window, or method design.
5. Explain the candidate contribution and test it against the strongest available counterexample or prior work. It may clarify a concept, extend an interpretation, resolve a contradiction, or test a boundary; do not promise field-wide novelty without evidence.
6. Draft a concise research outlook or contribution paragraph.

## Four Required Questions

A strong research gap must answer all four:

1. What have previous studies already established?
2. Where exactly is the explanation stuck?
3. Which specific opening will the next study enter through?
4. Why is this opening worth entering?

If any answer is missing, do not present the gap as ready.

## Gap Types

Use the type that matches the evidence:

- Theory gap: existing frameworks miss a mechanism or actor.
- Method gap: existing methods cannot observe the needed process, time dimension, or causal structure.
- Data gap: important samples, contexts, time windows, or measurements are absent.
- Boundary gap: known findings may not hold under certain conditions.
- Contradiction gap: studies disagree and the disagreement has a plausible unresolved source.
- Integration gap: separate modules exist but have not been connected into one explanation chain.

## Output Format

Provide:

```markdown
## Current Progress

[Consensus + tension in one sentence]

## Stuck Point

[Where the literature cannot yet explain enough]

## Proposed Cut-In Point

[Specific module/mechanism/variable/context/method]

## Why It Matters

[How this fills a gap, resolves a contradiction, tests a boundary, or advances explanation]

## 段落草稿（需作者改写并核对来源）

[Draft prose for conclusion/research outlook. Start with: "以下为草稿，请改写成你自己的论证，并逐句核对来源后再使用。" Tag every literature-dependent sentence with source and status, or [需补来源]]

## Three-Minute Oral Test

- Previous studies have shown: ...
- They have not explained: ...
- I will focus on: ...
- This is valuable because: ...

## 待核实清单

[Unverified sources, "未查到" results, sentences marked [需补来源], and inferences that still need checking; write "无" if empty]

## 给作者的问题

[Judgment calls that belong to the author; write "无" if empty]
```

The output sections above, and the two closing sections, keep fixed names and order; see `references/output-contract.md` (a copy bundled in this skill folder).

## Guardrails

- Do not use "few studies have examined" as the only proof of a gap; explain why the missing piece matters.
- Do not propose an opening that is broader than the user's review question.
- Do not confuse the user's not-yet-searched area with a true research gap; mark it as "needs verification" when evidence is insufficient.
- Source integrity: follow `references/source-integrity.md`. A gap claim about what the literature lacks needs sources or must be marked "needs verification". Use only sources the user provided or that are verified, tag each with a status (用户提供 / 已核验 / 未核验), write "未查到" instead of completing authors, year, journal, or pages, and put anything unverified in `## 待核实清单`. If that file is not available, still apply these rules.
