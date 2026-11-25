---
name: requesting-code-review
description: 在完成任务、实现主要功能或合并前使用，验证工作是否符合要求
---

# 请求代码评审

派遣 code-reviewer 子代理，在问题级联之前捕获它们。评审者获得精心构造的评审上下文——不会传递你的会话历史。这让评审者专注于工作产出而非你的思考过程，同时保留你自己的上下文以继续工作。

**核心原则：** 尽早评审，频繁评审。

## 何时请求评审

**必须：**

- 子代理驱动开发中每个任务完成后
- 完成主要功能后
- 合并到 main 之前

**可选但有价值：**

- 卡住时（换个视角）
- 重构前（基线检查）
- 修复复杂 bug 后

## 如何请求

**1. 获取 git SHA：**

```bash
BASE_SHA=$(git rev-parse HEAD~1)  # 或 origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 派遣 code-reviewer 子代理：**

使用 Task 工具，类型为 code-reviewer，填充 `code-reviewer.md` 中的模板

**占位符：**

- `{WHAT_WAS_IMPLEMENTED}` — 你刚构建了什么
- `{PLAN_OR_REQUIREMENTS}` — 它应该做什么
- `{BASE_SHA}` — 起始提交
- `{HEAD_SHA}` — 结束提交
- `{DESCRIPTION}` — 简要概述

**3. 处理反馈：**

- 立即修复严重（Critical）问题
- 继续之前修复重要（Important）问题
- 记录次要（Minor）问题留待后续处理
- 如果评审者有误，用技术理由反驳

## 示例

```
[刚完成任务 2：添加验证函数]

你：在继续之前请求代码评审。

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[派遣 code-reviewer 子代理]
  WHAT_WAS_IMPLEMENTED: 会话索引的验证和修复函数
  PLAN_OR_REQUIREMENTS: docs/plans/deployment-plan.md 中的任务 2
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: 添加了 verifyIndex() 和 repairIndex()，支持 4 种问题类型

[子代理返回]:
  优点：架构清晰，测试真实
  问题：
    重要：缺少进度指示器
    次要：魔法数字（100）用于报告间隔
  评估：可以继续

你：[修复进度指示器]
[继续任务 3]
```

## 与工作流的集成

**子代理驱动开发：**

- 每个任务后评审
- 在问题叠加之前捕获
- 修复后再进入下一个任务

**执行计划：**

- 每批（3 个任务）后评审
- 获取反馈、应用、继续

**临时开发：**

- 合并前评审
- 卡住时评审

## 红线

**绝不要：**

- 因为"很简单"就跳过评审
- 忽略严重问题
- 在重要问题未修复的情况下继续
- 对有效的技术反馈进行争辩

**如果评审者有误：**

- 用技术理由反驳
- 展示证明其可行的代码/测试
- 请求澄清

模板见：requesting-code-review/code-reviewer.md
