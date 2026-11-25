---
name: formax-rolling-plan-loop-workflow
description: "Use when the user wants a reusable rolling execution pattern (README + TODO-INDEX) like plans/web-reference-react-refactor, and wants to run delivery in small validated loops."
---

# Formax Rolling Plan Loop Workflow

## Goal

快速创建并维护一个“滚动循环执行”计划目录，结构与 `plans/web-reference-react-refactor/` 一致：

- `README.md`：目标、边界、固定执行循环
- `TODO-INDEX.md`：只保留未完成任务

## When to use

- 用户明确要求“模仿 `plans/web-reference-react-refactor` 的循环方式”。
- 用户希望以固定循环推进实现：实现 -> 定向测试 -> `codex review` -> 提交。
- 用户多次重复同类流程，想固化为可复用模式。

## Output contract

在 `plans/<topic-slug>/` 下创建（或更新）：

1. `README.md`
2. `TODO-INDEX.md`

可选：

3. 在 `plans/TODO-INDEX.md` 增加该计划入口（通常放在“并行参考”）。

## Default loop template

每个切片固定流程：

1. 实现（最小改动）
2. 定向测试
3. `codex review --uncommitted -c model="gpt-5.4" -c model_reasoning_effort="medium" -c service_tier="fast"`
4. 提交（Conventional Commit）

## Required guardrails

- 不在同一切片混入无关重构。
- 不做“测试全量覆盖”作为迭代默认命令（除非用户明确要求）。
- `TODO-INDEX.md` 只保留未完成项；已完成项不回填，历史以 Git commit 为准。

## Regeneration rules

当 `TODO-INDEX.md` 清空时：

1. 仅从同目录 `README.md` 派生下一批。
2. 按可提交的小切片拆分（建议 2-8 文件）。
3. 保持固定循环，不跳步。

## References

- 模板：`references/README.template.md`
- 模板：`references/TODO-INDEX.template.md`
