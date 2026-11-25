---
name: idea-refine
description: Refine a selected research idea into a problem-anchored, focused method proposal. Use after idea review or when the user has a promising but vague idea that needs PI-level sharpening.
argument-hint: "[selected-idea] [--run-dir path]"
---

# Idea Refine

Turn a selected idea into a focused research proposal: **$ARGUMENTS**.

Use prior artifacts when available:

- `${IDEA_STAGE_DIR}/FINAL_IDEA_RANKING.md`
- `${IDEA_STAGE_DIR}/REVIEW_REPORT.md`
- `${IDEA_STAGE_DIR}/NOVELTY_REPORT.md`
- `${IDEA_STAGE_DIR}/LANDSCAPE.md`

## Output Language

All user-facing text and all saved artifacts must be in **Chinese** by default. Keep official paper titles, benchmark names, model names, file paths, and code identifiers unchanged when needed. Follow `shared-references/output-language.md`.

Resolve `IDEA_STAGE_DIR` and `REFINE_LOG_DIR` by following `shared-references/run-directory.md`.

## Principles

1. Freeze the problem before changing the method.
2. One paper, one dominant contribution.
3. Prefer the smallest mechanism that directly addresses the bottleneck.
4. Do not add modern primitives such as LLM/VLM/RL/diffusion unless they solve a concrete failure.
5. Make the novelty delta operational, not rhetorical.

## Phase 1: Problem Anchor

Write:

- bottom-line problem
- must-solve bottleneck
- non-goals
- constraints
- success condition
- closest prior work to beat or differentiate from

## Phase 2: Method Thesis

Define:

- one-sentence thesis
- proposed mechanism
- input/output and data flow
- what is reused/frozen
- what is new
- training or inference recipe
- why the method is minimal
- failure modes and diagnostics

## Phase 3: Reviewer Recheck

If an external reviewer is available, ask:

- Does the proposal preserve the problem anchor?
- Is the contribution focused enough?
- Is the mechanism concrete enough to implement?
- What would a reviewer still reject?
- What must be changed before experiment planning?

Revise once unless the reviewer says the proposal is fundamentally broken.

## Output

Write `${REFINE_LOG_DIR}/FINAL_PROPOSAL.md`:

```markdown
# 最终 Idea 方案

## 问题锚点
- 底线问题：
- 必须解决的瓶颈：
- 非目标：
- 约束：
- 成功条件：

## 最近 Prior Work 与差异

## 方法论点

## 提出机制

## 贡献焦点
- 主导贡献：
- 支持性贡献，如有：
- 明确不主张的贡献：

## 为什么这值得成为一篇论文

## 已知风险

## 细化过程中做出的决策
```

Write `${IDEA_STAGE_DIR}/SELECTED_IDEA_BRIEF.md` as a one-page handoff.

## Rules

- If the method cannot be described concretely, stop and ask the user whether to regenerate or narrow the problem.
- Do not let the refined proposal become a kitchen-sink system.
- Preserve unresolved risks instead of smoothing them away.
