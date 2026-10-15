---
name: spec-orchestrator
description: superpowers 的规范编排技能。用户只要在问“先走哪条路、该用哪种工作流、该如何在 OpenSpec、Spec Kit 和 superpowers 之间协作”时就使用它。它只负责判断路径与产物，不依赖任何单独的规范技能。
---

# 规范编排器

这是一个规范编排技能。它不代写规范、计划或代码，只负责把任务路由到正确的工作流。

## 什么时候用

在这些情况下使用本 skill：

- 用户问“先走哪条流程”
- 用户想知道新项目、现有系统改造、实现执行分别该怎么分工
- 用户要在 OpenSpec、Spec Kit 和 superpowers 之间选路
- 用户希望统一项目目录和产物命名

## 核心职责

1. 判断任务属于新项目、现有系统改造，还是纯执行。
2. 选择对应的工作流和目录结构。
3. 只输出下一步该走什么，不展开详细内容。
4. 保持 OpenSpec、Spec Kit 和 superpowers 三者边界清楚。

## 输出模板（最小化）

默认按 4 行内输出，避免把编排回答写成规范正文：

1. `路径判断：新项目 / 现有系统改造 / 已确认执行`
2. `建议目录：.specflow/...`
3. `下一步接力：skill1 -> skill2 -> skill3`
4. `可选 CLI 起步：给 1-2 条命令；若不可用给手工兜底`

## 工作方式

- 新项目优先走初始化原则、规格、计划、任务、实现的路径。
- 现有系统改造优先走提案、规格差异、任务、实现、归档的路径。
- 已确认的实现工作交给 superpowers 的执行流。
- 如果用户只是在问“怎么分流”，只回答路径，不代写内容。

## superpowers 接力

当路径已经确定后，按这个顺序接力：

1. `brainstorming`：澄清目标、边界、约束。
2. `writing-plans`：把已确认规格拆成执行计划。
3. `subagent-driven-development` 或 `executing-plans`：进入实现。
4. `verification-before-completion`：完成前做证据校验。
5. `requesting-code-review`：提交前代码审查。

## CLI 约束

- 新项目优先给 Spec Kit 命令示例。
- 现有系统改造优先给 OpenSpec CLI 命令示例。
- 命令不确定时明确标注“以官方 README 为准”。
- 若用户环境命令不可用，立即切手工模板，不阻塞流程。

## 停止条件

当路径已经分流清楚时，本 skill 就停下。

## 参考

- `README.md`
- `references/工作流图.md`
- `references/路径选择.md`
- `references/产物布局.md`
- `references/CLI对接.md`
