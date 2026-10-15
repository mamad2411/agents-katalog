---
name: designing-bench-task
description: Use when designing a new bench_env task suite, adding several new tasks to an existing suite, or critiquing a task-set proposal for a mobile-gym App — before any `class FooTask(...)` is written under `bench_env/task/`.
---

# Designing bench_env Tasks

## Overview

Rushing from "here's an App" to "here are 5 task classes" produces low-difficulty suites whose judge logic can't actually verify completion. Design must precede code.

**Authoritative reference:** `bench_env/docs/task/TASK_AUTHORING_GUIDE.md` (reading §1 + §2 once is required; this skill enforces its gates).

## The Gate: two artifacts before any Python

Produce both as plain text in the conversation **before** writing any task class. If you catch yourself opening `tasks.py` / `defs/<TaskName>.py`, stop and produce them.

### 1. Functional audit table (TASK_AUTHORING_GUIDE §1.1–1.2)

A table with one row per distinct feature area. Columns:

| Page/feature | Source file(s) | User-visible actions | Observable state path |

You must actually read: `manifest.ts`, `navigation.declaration.ts`, `data/defaults.json`, `state.ts`, `pages/*`, and the suite's `app.py` accessor if it exists. No skipping "because the app looks simple."

### 2. Data sufficiency check (TASK_AUTHORING_GUIDE §1.3)

For every function you plan to parameterize, confirm `defaults.json` / `state.ts` provides ≥3 varied entries. If it doesn't, either propose expanding defaults, or drop parameterization for that function.

## Per-task: 4 judge-predict questions

For each proposed task, answer in 1-2 lines each **before writing code** (this is the soundness/completeness audit later enforced by `TASK_AUTHORING_GUIDE §2.7` "Reliability requirements"):

1. Agent 完全做对时，最终 state / answer 长什么样？
2. Agent 最常见的 1-2 种错误是什么？会不会被误判通过？（soundness）
3. 有没有合理完成任务的替代路径？会不会被误判失败？（completeness）
4. 有无边界情况导致正确答案不唯一、或判定证据不足？

If any answer surfaces a flaw (common: initial state already equals criteria; ground truth not unique; answer requires subjective judgement), **iterate the design in text** — do not defer the fix to code review.

## Rationalization table — STOP and do the step

| Excuse | Reality |
|---|---|
| "App is tiny, audit is overkill" | Audit surfaces the data gap so you can close it before writing code. |
| "Judge predict is slow, I'll see issues when coding" | Design bugs (init=goal, non-unique ground truth) are 10× cheaper to fix in text. |
| "These tasks are obvious, pre-sim is busywork" | A task obvious enough to skip pre-sim is obvious enough to answer the 4 questions in 30 seconds. |
| "I'll produce both artifacts and code in one pass" | Then when code inherits a design flaw, you've wasted the coding pass. Gate is gate. |

## Checklist before producing any `class FooTask(...)`

- [ ] Functional audit table in conversation
- [ ] Data sufficiency assessed per parameterized function; gaps declared
- [ ] For each task, 4 pre-sim questions answered
- [ ] No task has initial state == goal state (the task must require Agent action to flip something)
- [ ] Cross-checked `TASK_AUTHORING_GUIDE.md` §2.7 "Reliability requirements" + §4.7 "Authoring check_goals"

## After design is approved

For actual code discipline: see the **writing-bench-task-judge** skill and `bench_env/docs/task/TASK_CODE_SPEC.md`. For tests: **testing-bench-task** skill + `bench_env/docs/task/TASK_TESTING_GUIDE.md`.
