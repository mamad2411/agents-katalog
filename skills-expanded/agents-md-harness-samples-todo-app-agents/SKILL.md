---
title: todo-app-agents-entry
project: todo-app
language: zh-CN
layer: root
---

# AGENTS.md

这是一个全栈 TODO App 样例项目，包含：

- `fe/`：基于 Vite 8、React、TanStack Router、Tailwind CSS 4 的前端应用
- `be/`：基于 Golang 的 TODO App 后端服务

该项目用于验证 `agents-md-harness` 在全栈项目中的可用性，包括产品、架构、开发、测试、UI/UX 多角色协作，以及 FE / BE API 对接场景。

在行动前：

1. 先读本文件。
2. 识别当前任务属于 FE、BE、全栈联动、产品 / 架构、测试中的哪一类。
3. 只加载 `_harness/` 中最小必要文档。
4. 先写短期任务记忆，再进入设计 / 对齐 / 实现流程。

## 最小工作集规则

- 任何任务的最小工作集都必须保留 `AGENTS.md` 本身。
- 不要用 `_harness/readme.md` 替代 `AGENTS.md`。
- 对大多数 FE / BE / 测试 / UI 任务，默认先读：
  - `AGENTS.md`
  - `_harness/catalog.md`
  - `_harness/rules.md`
  - `_harness/workflow.md`
- 只有在你确实缺少项目整体背景时，才补读 `_harness/readme.md`。
- 只有在任务涉及稳定决策、失败案例、测试结论、接口约定、长期沉淀时，才补读 `_harness/memory/project.md`。

## 路由

- 项目概览与全栈上下文 -> `_harness/readme.md`
- 结构与文件定位 -> `_harness/catalog.md`
- 规则与确认边界 -> `_harness/rules.md`
- 执行流程与测试方式 -> `_harness/workflow.md`
- 长期项目记忆 -> `_harness/memory/project.md`

## 默认执行风格

- 先设计 / 先对齐，再实现。
- 默认采用测试驱动开发思路推进任务。
- 每个 agent 在任务开始时先写短期任务记忆。
- 优先保持 harness 文档短小、清晰、可组合。

## 默认路由基线

### FE / BE / 测试 / UI 任务

默认工作集：

- `AGENTS.md`
- `_harness/catalog.md`
- `_harness/rules.md`
- `_harness/workflow.md`

### API 契约 / 架构 / 长期记忆任务

默认工作集：

- `AGENTS.md`
- `_harness/rules.md`
- `_harness/workflow.md`
- `_harness/memory/project.md`

以下情况再补 `catalog.md`：

- 需要明确 FE / BE 路径
- 需要定位 `fe/src/components`
- 需要定位 `be/internal/httpapi`
- 需要定位 `be/internal/todo`

## 必须先确认

- 项目模块决策
- 架构决策
- 破坏性更新
- API 契约与响应结构的重大调整
- 重大 UX / 数据流 / FE-BE 接口协作方式调整

## 默认不需要先确认

- 普通 FE 组件 / 页面 / 表单开发
- 普通 BE handler / service 新增
- 普通测试补充与回归测试方案细化
- 不改变契约的实现性修改
- 不改变信息架构的常规 UI 优化

## Memory

- 长期共享记忆：`_harness/memory/project.md`
- 短期 agent 记忆：`_harness/memory/agents/*.local.md`

## Evolution

核心 harness 文件属于高风险指导文件。
不要静默重写。
需要先提出修改建议，再等待确认。
