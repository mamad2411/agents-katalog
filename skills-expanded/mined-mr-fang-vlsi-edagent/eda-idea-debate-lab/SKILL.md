---
name: eda-idea-debate-lab
description: Generate and refine EDA research ideas through structured brainstorming and pro-vs-con debate, then output a testable idea decision memo.
---

# EDA Idea Debate Lab

## When to use

Use this skill when you need to generate new ideas or stress-test an idea before implementation.

## Workflow

1. Brainstorm at least 3 candidate ideas from current evidence.
2. For each candidate, write:
- strongest support (pro),
- strongest objections (con),
- failure modes and disproof signals.
3. Run a structured debate:
- side A argues expected upside and feasibility,
- side B argues risk, confounders, and likely false-positive paths.
4. Converge to one or two candidate ideas with explicit assumptions.
5. Export assumptions into hypothesis design inputs.

## Outputs

1. `idea_brainstorm.md`
2. `pro_con_debate.md`
3. `idea_decision_memo.md`

## Hard rules

1. Steelman both sides; avoid weak strawman objections.
2. Every selected idea must have at least one falsifiable key assumption.
3. Do not skip unresolved risks; list them explicitly.

## Reference

Load when needed:
1. `references/debate-template.md`
