---
name: refine-literature-question
description: "Refine a broad literature review topic into a bounded question for searching and screening, including explanatory, scoping, conceptual, and historical reviews. Use for thesis proposals, journalism and communication, or information science review questions. 触发词：综述选题、收紧研究问题、新闻传播综述、情报学综述、开题选题。"
metadata:
  version: "0.3.0"
---

# Refine Literature Question

## Discipline And Interview Setup

Read [discipline-routing.md](references/discipline-routing.md), then only the selected discipline profile. Reuse the user's existing brief; do not restart intake at each stage. For journalism/communication or information science, use that profile's concepts, extraction fields, and appraisal checks instead of a generic social-science template.

When the user requests "grill me", 追问, or 模拟答辩, read [research-interview.md](references/research-interview.md). Ask one decision-relevant question per turn and wait; do not generate the stage deliverable until enough decisions are settled or the user asks to proceed. In quick/no-question mode, record assumptions and continue without inventing answers.

For evidence extraction or drafting, read [review-workflow.md](references/review-workflow.md). With no sources, give a plan or outline, not a purported synthesis. If reference files are unavailable, retain the source guardrails below and state that discipline guidance is missing.

## Goal

Turn a broad topic into a usable question anchor before searching, reading, or writing the review. The output should be a one-sentence research question that forces selection: some papers become clearly relevant, and others become safe to skip.

## Workflow

1. Identify whether the user's input is a topic, a phenomenon, or an actual question.
2. Identify the review type, then replace vague nouns with bounded concepts, objects, relationships, periods, or puzzles.
3. Generate 3-5 candidate angles after scope decisions are clear; do not flood an interview turn with candidates.
4. Evaluate each candidate against the three-anchor test.
5. Recommend one primary question and 1-2 backups, then explain what each would make the review include or exclude.

## Three-Anchor Test

A strong literature review question should:

- Match the review purpose: explanation, bounded evidence mapping, conceptual distinction, or historical interpretation. A causal "why/how" question is not mandatory.
- Force literature selection by making some studies irrelevant to the question.
- Feel worth answering if a reader could get a credible answer from the review.

If the question fails any item, revise it before proceeding to search or outline the literature.

## Question Patterns

Use these patterns when generating candidates:

- Mechanism: `Why does [phenomenon] occur in [context], and through what mechanism?`
- Contrast: `Why does [outcome] differ between [group/place/time A] and [group/place/time B]?`
- Condition: `Under what conditions does [factor] influence [outcome]?`
- Tension: `Why do existing studies disagree about [relationship/result]?`
- Process: `How does [actor/system] move from [state A] to [state B]?`
- Scoping: `What concepts, methods, and populations have been studied for [object] within [scope]?`
- Conceptual/history: `How has the meaning of [concept] changed across [traditions/periods], and what does that change explain?`

## Output Format

Provide:

```markdown
## Candidate Questions

1. ...
2. ...

## Recommended Anchor

[One sentence]

## Why This Works

- Selection boundary: ...
- Likely literature modules: ...
- What to skip: ...

## Revision Notes

- If the user wants broader scope: ...
- If the user wants narrower scope: ...

## 待核实清单

[Unverified sources, "未查到" results, sentences marked [需补来源], and inferences that still need checking; write "无" if empty]

## 给作者的问题

[Judgment calls that belong to the author; write "无" if empty]
```

The output sections above, and the two closing sections, keep fixed names and order; see `references/output-contract.md` (a copy bundled in this skill folder).

## Guardrails

- Do not accept an unbounded label such as `XX research review` as the final anchor. Descriptive, historical, and conceptual reviews are valid when their corpus, scope, and analytical purpose are explicit.
- Do not invent a domain-specific claim when the user has not provided enough context; offer candidate angles and mark assumptions.
- Treat AI as a sparring partner: generate options and pressure-test wording, but keep the user's academic judgment in charge.
- Source integrity: follow `references/source-integrity.md`. Claims about what "existing studies" do or disagree on are assumptions until the user supplies sources; mark them. Use only sources the user provided or that are verified, tag each with a status (用户提供 / 已核验 / 未核验), write "未查到" instead of completing authors, year, journal, or pages, and put anything unverified in `## 待核实清单`. If that file is not available, still apply these rules.
