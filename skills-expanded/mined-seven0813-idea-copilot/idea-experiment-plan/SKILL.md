---
name: idea-experiment-plan
description: Convert a refined research idea into a claim-driven experiment plan with milestones, ablations, success criteria, and run order. Use only when the user explicitly asks to plan experiments, create an experiment plan, or decide how to test an idea.
argument-hint: "[refined-proposal-or-idea] [--run-dir path]"
---

# Idea Experiment Plan

Create a concrete experiment roadmap for: **$ARGUMENTS**.

Do not invoke this skill merely because a refined idea exists. Require an explicit experiment-planning request in the current user prompt.

Use `${REFINE_LOG_DIR}/FINAL_PROPOSAL.md` if present.

## Output Language

All user-facing text and all saved artifacts must be in **Chinese** by default. Keep dataset names, benchmark names, model names, file paths, run IDs, and code identifiers unchanged when needed. Follow `shared-references/output-language.md`.

Resolve `REFINE_LOG_DIR` by following `shared-references/run-directory.md`.

## Phase 1: Freeze Claims

Define at most two primary claims:

- **Primary claim**: the main mechanism or scientific contribution.
- **Supporting claim**: optional and directly supports the primary claim.
- **Anti-claim**: the skeptical alternative to rule out.

For each claim, write the minimum convincing evidence.

## Phase 2: Experiment Blocks

Design compact blocks:

1. sanity check
2. baseline reproduction
3. main result
4. novelty isolation ablation
5. simplicity or deletion check
6. failure analysis or qualitative diagnosis

Delete any block that does not change a reviewer belief.

## Phase 3: Specify Runs

For each block:

- claim tested
- dataset/split/task
- systems compared
- metrics
- setup details
- seeds
- success criterion
- failure interpretation
- expected table/figure
- priority: MUST / SHOULD / NICE

## Phase 4: Run Order

Use milestones:

- M0: data and metric sanity
- M1: strongest baseline
- M2: main method
- M3: decisive ablations
- M4: robustness and qualitative analysis

Each milestone needs:

- runs
- cost estimate
- decision gate
- risk
- mitigation

## Output

Write `${REFINE_LOG_DIR}/EXPERIMENT_PLAN.md`:

```markdown
# 实验计划

## Claim 映射表
| Claim | 最小证据 | 实验模块 |
|-------|------------------|-------------------|

## 实验模块
### B1：[实验模块名称]
- 被检验的 claim：
- 数据集 / split / 任务：
- 对比系统：
- 指标：
- 设置：
- 成功标准：
- 失败解释：
- 优先级：

## 运行顺序
| 里程碑 | 目标 | Runs | 决策门 | 成本 | 风险 |
|-----------|------|------|---------------|------|------|

## 计算与数据预算

## 风险与缓解

## 最先运行的三个实验
1. ...
2. ...
3. ...
```

Write `${REFINE_LOG_DIR}/EXPERIMENT_TRACKER.md`:

```markdown
# 实验追踪表

| Run ID | 里程碑 | 目的 | 变体 | 数据 | 指标 | 优先级 | 状态 | 备注 |
|--------|-----------|---------|---------|------|---------|----------|--------|-------|
```

## Rules

- Do not invent results.
- Do not design experiments without a linked claim.
- Prefer strong baselines over long baseline lists.
- Separate must-run experiments from nice-to-have experiments.
- If the plan exceeds the user's stated compute/time budget, propose a smaller pilot plan first.
