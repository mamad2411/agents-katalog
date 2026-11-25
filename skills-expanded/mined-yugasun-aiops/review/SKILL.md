---
name: review
description: >
  Review in three modes — code (diff vs standards/spec), design (NOTES + tech-spec
  before planning), drift (implementation vs tech-spec before ship). Pick mode from
  Flow Conductor phase or user intent; do not mix artifact types.
---

# Review

Three modes. Each mode has its own inputs, axes, and output artifact. **Do not mix modes in one file.**

## Mode selection

| Mode | Trigger | Agent | Output |
| --- | --- | --- | --- |
| **code** | `delivery` sub-phase, user asks to review diff/PR | code-reviewer | `.scratch/<slug>/REVIEW.md` |
| **design** | `design_review` phase, user asks to review design | design-reviewer | `.scratch/<slug>/DESIGN_REVIEW.md` |
| **drift** | `drift_check` phase (after delivery, before ship) | design-reviewer | `.scratch/<slug>/DRIFT_REPORT.md` |

When unsure: Flow Conductor phase name wins. Direct invocation defaults to **code** unless the user names design or drift.

---

## Code mode

Review `git diff <fixed-point>...HEAD`:

- **Standards** — matches repo coding standards?
- **Spec** — matches originating issue/PRD?
- **Constitution** (optional) — when `CONSTITUTION.md` exists at repo root, violates any non-negotiable principle?

Run `/aiops-setup` if `docs/agents/issue-tracker.md` is missing.

### Process

1. **Pin fixed point** — commit, branch, tag, or `main`. Confirm ref resolves and diff is non-empty.
2. **Find spec** — issue refs in commits (`docs/agents/issue-tracker.md`), user path, or `docs/`/`.scratch/` PRD. No spec → Spec axis skips.
3. **Find standards** — `CODING_STANDARDS.md`, `CONTRIBUTING.md`, etc.
4. **Find constitution** — `CONSTITUTION.md` at repo root. Missing → Constitution axis skips.
5. **Parallel sub-agents** — one per active axis. Each under 400 words, cite sources.
6. **Aggregate** — one section per axis verbatim. One-line summary per axis; don't merge axes.

A change can pass one axis and fail another — keep axes separate.

### Output: REVIEW.md

```markdown
# Code Review: <feature-slug>

## Summary
<overall assessment>

## Design Alignment
- [ ] 实现符合 NOTES.md 设计决策
- [ ] 接口符合 tech-spec.md 规格
- [ ] 无超出 scope 的变更

## Findings

### Blocking (必须修复)
#### B1: <file:line> — <title>
- **问题**: …
- **建议**: …

### Non-blocking (建议改进)
#### N1: <file:line> — <title>
- **问题**: …
- **建议**: …

## Verdict
**APPROVE** | **REQUEST_CHANGES**
```

Gate: `review_approve` requires `REVIEW.md` contains `APPROVE`.

---

## Design mode

Review design artifacts **before** planning or implementation. No code diff — review `NOTES.md` + `tech-spec.md` only.

Vocabulary for depth/seam/deletion-test checks: [design-vocabulary.md](../architect-design/design-vocabulary.md).

### Inputs

- `.scratch/<slug>/NOTES.md`
- `.scratch/<slug>/tech-spec.md`
- `CONTEXT.md` (project root or per-area)
- `docs/adr/`
- `.scratch/<slug>/mockups/` (if UI mockups exist)

### Process

1. Read NOTES.md decisions — each must list at least one rejected alternative.
2. Read tech-spec.md module inventory — apply deletion test and depth assessment per [design-vocabulary.md](../architect-design/design-vocabulary.md).
3. Cross-check CONTEXT.md vocabulary and existing ADRs — flag conflicts unless explicitly justified.
4. If `CONSTITUTION.md` exists, check design against non-negotiable principles.
5. Independent second perspective — do not rubber-stamp architect reasoning.

Do not review implementation details (that is code mode).

### Output: DESIGN_REVIEW.md

```markdown
# Design Review: <feature-slug>

## Summary
<one paragraph>

## Design Soundness
- [ ] 每个设计决策列出了至少一个被否决的替代方案及原因
- [ ] 模块通过 deletion test（非 pass-through）
- [ ] 接口设计遵循 depth 原则：小接口 + 深实现
- [ ] 依赖分类正确，seam 位置合理（≥2 adapters 才有真实 seam）
- [ ] 接口定义与 CONTEXT.md 领域模型一致
- [ ] 无与现有 ADR 的冲突（或冲突已记录并有充分理由）
- [ ] Open Questions 全部解决或明确标记为非阻塞
- [ ] 无过早优化或过度设计
- [ ] Scope 边界清晰，out-of-scope 明确排除

## Findings

### Blocking (必须修正才能进入规划)
#### D1: <title>
- **问题**: …
- **建议**: …
- **关联**: NOTES.md Decision X / tech-spec.md §Y

### Non-blocking (建议改进)
#### N1: <title>
- **建议**: …

## Verdict
**APPROVE** | **REQUEST_CHANGES**
```

Gate: `design_review_approve` requires `DESIGN_REVIEW.md` contains `APPROVE`. Blocking findings block planner until resolved.

---

## Drift mode

After delivery, before ship: does the **implementation** match the **approved design**?

### Inputs

- `.scratch/<slug>/tech-spec.md`
- `.scratch/<slug>/NOTES.md` (scope and decisions)
- `git diff` since journey start or user-specified fixed point

### Process

1. Pin diff fixed point (same as code mode).
2. For each tech-spec requirement: implemented? partially? missing?
3. For each behaviour in the diff: in spec? out of scope?
4. Flag scope creep and spec gaps separately.

### Output: DRIFT_REPORT.md

```markdown
# Drift Report: <feature-slug>

## Summary
<overall drift assessment>

## Spec coverage
| Requirement (tech-spec) | Status | Evidence |
| --- | --- | --- |
| … | implemented / partial / missing | file:line or "not found" |

## Undocumented behaviour
| Change in diff | In spec? | Notes |
| --- | --- | --- |
| … | yes / no / partial | … |

## Findings

### Blocking (must fix or update spec before ship)
#### F1: …

### Non-blocking
#### N1: …

## Verdict
**PASS** | **DRIFT_FOUND**
```

Gate: `drift_check_pass` requires `DRIFT_REPORT.md` exists. Use `PASS` in verdict when no blocking drift.
