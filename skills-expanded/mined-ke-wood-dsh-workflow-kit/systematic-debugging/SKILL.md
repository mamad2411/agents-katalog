---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

## Overview

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue: test failures, bugs in production, unexpected behavior,
performance problems, build failures, integration issues.

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:** issue seems simple (simple bugs have root causes too)、
你很急（急必返工）、有人要求立刻修（系统化比乱试更快）。

## The Four Phases

You MUST complete each phase before proceeding to the next.

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

**Phase 1 判据（不可跳）**：读完整错误信息 · 能稳定复现 · 查最近改动 ·
多组件系统先加诊断埋点定位是哪一层 · 深层错误沿调用栈回溯到源头。

**Phase 3 判据**：一次只测一个假设；没验证就不许叠加第二个修复。

**Phase 4 判据**：先写失败测试，再改；一次一个修复；不顺手重构。
**3 次修复都失败 → 停手，这是架构问题，不是假设问题**，必须先与人对齐。

> 四阶段的完整步骤、多组件埋点示例、架构问题判断细则见
> `references/four-phases.md`。

## Red Flags - STOP and Follow Process

If you catch yourself thinking:

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt"（已经试过 2 次以上时）**
- **每个修复都在不同地方冒出新问题**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (see Phase 4.5).

## 人的信号：他在告诉你走错了

- "Is that not happening?" —— 你没验证就假设了
- "Will it show us...?" —— 你该先加证据收集
- "Stop guessing" —— 你在不懂的情况下提修复
- "Ultra-think this" —— 该质疑根本假设，不是表面症状
- "We're stuck?"（不耐烦）—— 你的路子不对

**看到这些：停，回 Phase 1。**

## Common Rationalizations

最常见的四条（完整表见 `references/four-phases.md`）：

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | 简单问题也有根因，流程对简单问题更快。 |
| "Emergency, no time for process" | 系统化比猜-改-再猜的来回折腾更快。 |
| "I'll write test after confirming fix works" | 没测试的修复留不住，测试先证明它。 |
| "One more fix attempt" (after 2+ failures) | 3+ 次失败 = 架构问题，别再修。 |

## Supporting Techniques

These techniques are part of systematic debugging and available in this directory:

- **`root-cause-tracing.md`** - Trace bugs backward through call stack to find original trigger
- **`defense-in-depth.md`** - Add validation at multiple layers after finding root cause
- **`condition-based-waiting.md`** - Replace arbitrary timeouts with condition polling
