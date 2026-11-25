---
name: workflow-yylo
title: YYLO Ledger 工作流定义库（workflow Record）
description: 当编码智能体需要沉淀或维护已验证的工作流定义（workflow Record）时使用；驱动 yy ledger 完成检索、校验读取、安全创建与修订，保持存储、执行与运行证据三边界分离，产出不可变 Record ID 与回执；不适用于执行工作流或保存运行日志证据；触发词：workflow、工作流定义、validated、Record、yy ledger
domain: 协作/automation
triggers: [已验证工作流定义沉淀, workflow Record 创建与修订, validated 只读校验读取, schema_version v1 步骤定义, 存储执行证据三边界分离, compare-and-replace 安全修订, yy ledger workflow 命令, 运行证据走 Artifact Record]
tags: [工作流, workflow, 校验, 版本控制, 编码智能体, yylo, cli, 自动化]
level: 进阶
status: stable
agents: [claude-code, codex]
tools: [yy]
requires: []
related: [ledger-tasks-yylo, wiki-yylo, agent-workflow-builder]
combines_with: [spec-driven-workflow, n8n-workflow-patterns]
license: MIT
source: yylo-dev/yylo-skills
source_license: MIT
---

# YYLO Ledger 工作流定义库（workflow Record）

采编自 yylo-dev/yylo-skills（MIT），由 YYLO 团队自荐并适配为本库格式。

## 何时使用

当智能体要把「已验证的工作流步骤」放进比脚本注释更可靠、可被审查与复用的载体时使用：

- 沉淀或维护 workflow Record：经校验的工作流定义与修订历史。
- 执行前冻结工作流身份（Record ID、revision、payload digest、runner、授权），执行后把有界输出归档为证据。
- **不该用**：直接执行工作流、保存运行日志/stdout/报告（走 Artifact Record 证据通道）、任务状态（走 Task）、持久知识（走 Wiki）。

## 步骤 / 指令

1. **预检**：`yy ledger workflow --help`（命令 help 为当前运行时的权威说明）；命名空间缺失时禁止发明命令或直改存储。只读 Ledger 主机也没有工作流执行端点。
2. **发现**：无 ID 时先有界检索：
   `yy ledger workflow search --text "release verification" --projection summary --limit 20 -f json`
3. **读取**：`yy ledger workflow get RECORD_ID -f json`；字节级 `--raw`；`--validated` 仅在校验通过后输出规范化 YAML。发现后优先使用不可变 ID。
4. **创建**（文件/stdin 传输，workflow v1 最小结构）：

   ```yaml
   schema_version: v1
   workflow_id: focused-validation
   steps:
     - id: test
       command: ["npm", "test"]
   ```

   `yy ledger workflow create --title "Focused validation" --file workflow.yaml`
   Ledger 拒绝不安全或不可移植 YAML：重复键、别名/锚点、显式标签、递归结构、非字符串键、隐式日期时间、非有限数、CRLF、未支持的值。绝不把可执行 shell 当未校验替身存入。
5. **安全修订（compare-and-replace）**：先读当前 revision 与历史 → 按安装版 `yy ledger workflow update --help` 的控件，绑定期望 revision 与 preimage/digests 执行更新 → 校验并回读。漂移时停下对账，绝不强推；归档非破坏。
6. **执行边界**：执行前冻结 Record ID、revision、payload digest、runner 身份、输入与授权；执行后把有界输出存入 Artifact Record（带 workflow/run 溯源）。执行请求绝不隐含合并、发布、部署或生产权限。
7. **结果上报**：上报 Record kind/profile、真实不可变 ID 与真实 slug（来自返回 Record 或原生 get 回读），绝不凭标题编造 slug。

## 示例

```
yy ledger workflow search --text "release verification" --projection summary --limit 20 -f json
yy ledger workflow get wf_ab12cd34 --validated
yy ledger workflow create --title "Focused validation" --file workflow.yaml
yy ledger workflow update --help   # 按安装版本的 compare-and-replace 控件回读后执行
```

## 注意事项

- 三边界铁律：Ledger 只存储并校验工作流数据，不执行；另行选定的 runner 才执行已评审数据；运行证据归 Artifact Record，绝不回写定义。
- 存储不授予执行、网络、变更、发布、部署权限。
- 修订必须绑定期望 revision 与 preimage/digests；并发漂移先对账。
- slug 只是发现便利；ID 才是关系与生命周期操作的权威。

## 互见

- requires：无硬前置。
- related：`ledger-tasks-yylo`（同一家族的任务看板技能，任务状态走它）、`wiki-yylo`（同一家族的持久知识技能，Wiki/Task/Workflow/Artifact 归属判别）、`agent-workflow-builder`（同类中的多智能体编排脚本构建，workflow Record 管理其确定性定义）。
- combines_with：`spec-driven-workflow`（规格驱动开发流程可冻结为已验证 workflow Record）、`n8n-workflow-patterns`（三方编排模式的定义治理与边界分离可复用本技能的审查纪律）。
