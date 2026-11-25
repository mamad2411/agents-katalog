---
name: brainstorming
description: "适用于编写代码前，当需求或方向仍不清楚时，梳理模糊想法、比较方案并形成轻量设计文档。Use before implementation when the request is ambiguous or the direction is undecided: refine rough ideas through questions, explore alternatives, validate design sections with the user, and save a concise decision spec. Do not create implementation plans or invoke planning/execution skills automatically. 中文关键词：想法不清楚、需求澄清、方案发散、方案对比、取舍分析、决策、设计文档、决策依据。"
---

# Brainstorming

Turn an unclear request into a shared decision and a concise decision spec.

## 输出语言

默认使用简体中文与用户沟通，并以简体中文编写决策文档。用户明确指定其他语言或既有文档语言另有约定时，遵从该约定；代码、命令、产品名和必须保持原文的引用不强行翻译。

## Scope

Do only these things:

- Clarify the need, intended outcome, constraints, and success criteria.
- Expand 2–3 genuinely distinct directions when alternatives matter.
- Compare trade-offs and recommend a direction when the evidence supports one.
- Apply YAGNI ruthlessly: remove features and decisions that are not needed to meet the success criteria from every direction and from the recommended design.
- Help the user make or confirm the decision.
- Write the confirmed decision as one spec.

## Hard boundaries

Do not:

- Create an implementation plan, task breakdown, checklist, or task file.
- Invoke `planning-with-files-zh` or any other planning/implementation skill.
- Write, edit, generate, or execute production code.
- Start a visual companion, server, or other auxiliary workflow.
- Commit changes or continue into implementation after the spec is complete.

The only project file this skill may create or edit is the decision spec described below.

## Establish shared understanding

Before proposing features or an approach, identify the intended outcome, who it is for, and what success looks like. If purpose or intended use is missing, ask one focused question; do not infer intent from the app genre. When the request already supplies this information, reflect it instead of asking again.

Write back a short understanding of the outcome, constraints, and success criteria, separating stated requirements from assumptions. Invite correction and incorporate the answer before treating it as the design brief. Carry that understanding into the decision spec and check proposed features and technical choices against it.

## Conversation

1. Ask one focused question at a time until the decision is well framed. Prefer concrete choices when they genuinely reduce ambiguity.
2. State the assumptions and constraints that matter. Surface unknowns instead of silently filling them in.
3. Offer 2–3 viable directions only when a real choice remains. For each, explain the primary benefit, primary cost, and the condition under which it is the better choice.
4. Recommend one direction, or explicitly say that the decision needs more information. Do not invent certainty.
5. Iterate until the user confirms a direction or asks to stop.

## Design validation

Before writing the spec, present the design in small sections and validate each section with the user:

1. **Scope and outcome** — the goal, success criteria, and exclusions.
2. **Design and behavior** — the chosen direction, user-visible behavior, and constraints.
3. **Trade-offs and risks** — alternatives rejected, accepted costs, and unresolved questions.

Revise any section the user does not validate. Do not proceed to the spec until the design is confirmed.

## Spec

After the user confirms a direction, write one spec to `docs/specs/YYYY-MM-DD-<topic>-spec.md`. Respect a user-provided path instead.

Keep it decision-focused:

1. **Goal and context** — what problem or opportunity matters.
2. **Decision** — the chosen direction and why it fits.
3. **Requirements and constraints** — observable outcomes, rules, and non-negotiables.
4. **Alternatives considered** — the meaningful options and the trade-offs that ruled them in or out.
5. **Out of scope** — what this decision deliberately does not cover.
6. **Open questions** — unresolved items that need an answer before implementation.

Do not include implementation steps, task assignments, code structure, file-by-file edits, or estimates.

## Spec self-review

Before finalizing, remove placeholders and resolve contradictions. Check that the decision, requirements, trade-offs, scope, and open questions agree with one another. Use [spec-document-reviewer-prompt.md](spec-document-reviewer-prompt.md) only when an independent spec review is explicitly permitted.

## Final response

Once the spec is written and reviewed, output only this decision summary. Do not add a plan, implementation steps, code, or a handoff.

```markdown
## 决策摘要

- **决策：** …
- **理由：** …
- **接受的取舍：** …
- **未决问题：** …
- **规格文档：** …
```
