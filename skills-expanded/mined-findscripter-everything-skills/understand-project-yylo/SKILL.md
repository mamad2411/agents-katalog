---
name: understand-project-yylo
title: YYLO 项目理解与变更前调研
description: 当在规划或实现变更前需要摸清产品架构、依赖与验证回路时使用；读 AGENTS.md/源码/测试与 Ledger 任务及持久规格，有界追踪依赖，产出当前行为、事实源、风险与最小验证回路的调研报告；不适用于直接实现、任务状态或证据归档；触发词：项目理解、变更前调研、架构摸底、依赖追踪、validation loop、yy task start
domain: 研发/architecture
triggers: [变更前项目调研, 架构与依赖摸底, AGENTS.md/CLAUDE.md 事实源阅读, Ledger 任务与持久规格检索, 有界依赖与运行路径追踪, 最小验证回路识别, yy task start 任务工作树, 运营规格 report Record 固化]
tags: [项目理解, 架构, 调研, 依赖分析, 验证回路, 编码智能体, yylo, cli]
level: 进阶
status: stable
agents: [claude-code, codex]
tools: [yy]
requires: []
related: [ledger-tasks-yylo, artifact-yylo, legacy-codebase-modernizer]
combines_with: [c4-architecture-docs, codebase-onboarding-doc]
license: MIT
source: yylo-dev/yylo-skills
source_license: MIT
---

# YYLO 项目理解与变更前调研

采编自 yylo-dev/yylo-skills（MIT），由 YYLO 团队自荐并适配为本库格式。

## 何时使用

当智能体在「动代码或写计划」之前需要一份可靠的现状底稿时使用：

- 规划或实现某个变更前，摸清当前产品架构、依赖与验证回路。
- 通过规范元数据控制器读取相关 Kanban 任务与持久规格，不臆测计划文件位置。
- **不该用**：直接实现（走 `yy task start` 的任务工作树流程）；任务状态管理（走 Task Record）；运行证据归档（走 Artifact Record）；无变更目标的漫游式代码阅读。

## 步骤 / 指令

1. **读事实源**：在集成或指定特性工作树中读 `AGENTS.md`/`CLAUDE.md`、仓库状态、相关源码、测试与既有产品文档。
2. **读任务与规格**：通过规范控制器读相关 Kanban 任务与持久规格；不假设 `.juno_task/plan.md` 存在，不把控制器私有元数据物化进产品工作树。取回上下文不猜类型：

   ```bash
   yy ledger get --help
   yy ledger get RECORD_ID -f json          # 已知 task_/doc_/artifact_ ID 首选
   yy ledger record get RECORD_ID -f json   # 安装的 get 仅支持任务时，查原生 help 后再用
   yy ledger record search --projection summary --limit 20 -f json
   ```

   精确读取含热存与归档；发现默认仅热存（归档需显式 scope）；保留缺失/歧义/损坏诊断，不改试其他类型或项目；universal get 内嵌可读内容默认 64 KiB；显式 `--content` 读本地字节上限 16 MiB，检查退出码，绝不隐式拉取外部 URL。
3. **有界追踪**：只追踪达成目标所需的依赖与运行路径；独立问题可并行有界调查。
4. **产出调研报告**：当前行为、事实源、受影响组件、风险、未知项、最小可用验证回路。
5. **交接**：用户要规划 → 交给规划流程；要实现 → 只在 `yy task start TASK_ID` 返回的任务工作树内工作。
6. **运营规格（仅在需要时）**：外部起草 → 预检 `yy ledger artifact` API → 以不可变 `report` Artifact Record 固化（带溯源/保留）→ 核验取回、摘要与历史；API 不可用时保留外部草稿即停，绝不回退到产品 `docs/`、任务正文、`.juno_task/specs` 或直改控制器存储。产品 `docs/` 保留给随产品发布的文档。
7. **结果上报**：上报 Record kind/profile、真实不可变 ID 与真实 slug（来自返回 Record 或原生 get 回读），绝不凭标题编造 slug 或与 ID 混淆；字段缺失就说不可用，不编造。

## 示例

```
yy ledger get task_01h2k3 -f json
yy ledger record search --projection summary --limit 20 -f json
yy ledger get artifact_9f8e7d -f json
yy task start TASK_ID    # 实现请求 → 只在返回的工作树内工作
```

## 注意事项

- 仓库状态与测试结果先读后报，不凭记忆臆测当前行为；报告中区分「读到的事实」与「推断」。
- 控制器私有元数据只在控制器内消费，绝不物化进产品工作树或提交进产品仓库。
- 发布、部署、生产变更与清理不在本技能授权范围；调研结论不构成执行权限。
- 持久运营文档只在被明确要求或确有价值时固化为 report Record；不要用瞬态状态更新根指令。

## 互见

- requires：无硬前置。
- related：`ledger-tasks-yylo`（同一家族的任务看板技能——本技能读取其任务与规格上下文）、`artifact-yylo`（同一家族的证据归档技能——运营规格以不可变 report Record 固化）、`legacy-codebase-modernizer`（同类中的遗留系统现代化——改造前同样依赖现状底稿）。
- combines_with：`c4-architecture-docs`（先做现状调研，再自底向上生成 C4 架构文档）、`codebase-onboarding-doc`（调研结论按受众沉淀为新人上手文档）。
