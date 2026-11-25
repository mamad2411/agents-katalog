---
name: using-forgeteam
version: "1.0.0"
description: "ForgeTeam workflow bootstrap: select and apply the existing delivery Skills before starting work"
triggers:
  - auto: "before any business-system development, change, review, or release task"
route_level: [micro, standard, full]
inputs:
  - user_request
  - project context
outputs:
  - selected ForgeTeam route and next Skill
next: propose | plan | execute
token_budget: 1000
constraints:
  must:
    - "选择已有 ForgeTeam Skill，不自行发明替代流程"
    - "在代码变更前确认路由和验收方式"
---

# Using ForgeTeam

## 目标

在开始业务系统需求、代码变更、评审或发布任务前，先选择并遵循 ForgeTeam 的既有 Skills。这个 Skill 只负责路由和衔接，不替代 `propose`、`html`、`plan`、`execute`、`review`、`verify` 或 `ship` 的具体职责。

## 必须执行

1. 读取项目上下文（存在时）：`.forgeteam/config.yaml`、`.forgeteam/memory/state.md`、`.forgeteam/memory/project-map.md`、`.forgeteam/memory/decisions.md`、`.forgeteam/memory/known-issues.md` 与 `specs/active/`。
2. 按变更范围选择路由：
   - Micro（少于 50 行且范围明确）：`execute → verify → done`。
   - Standard（50–500 行）：`plan → [html] → execute → review → verify → ship`。
   - Full（超过 500 行、方案不明确、跨模块/接口/数据变更）：`propose → [html] → plan → execute → review → verify → ship`。
3. 页面、表单、列表、交互或数据展示变更必须插入 `html`，并在用户确认原型前不进入开发。
4. 只调用对应的既有 ForgeTeam Skill：`propose`、`html`、`plan`、`execute`、`review`、`verify`、`ship`、`debug`、`memory`、`evolve`、`onboard`。
5. 业务变更必须记录适用的权限、流程、数据、审计和集成验收证据；发布前不得跳过 build、test、run、safety 验证。

## 触发方式

安装 Codex 插件后，优先根据用户的自然语言请求自动路由。用户明确点名某一阶段时，直接加载对应的 ForgeTeam Skill；不要依赖 Claude Code 专用的 `/forge-*` 语法。

## 边界

- 不在 Full 路由的 proposal 或原型确认前写代码。
- 不把“代码已修改”当作业务验收完成。
- 单个任务连续 3 次修复失败，或连续 2 个任务受阻时，暂停并请求人工决策。
