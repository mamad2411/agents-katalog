---
name: workflow-runner
description: Compose skill stages with complete task diagnostics and honest output status.
---

# Workflow runner

## English

Create one task identity and ordered stage list for the user's request. Track each stage's inputs, outputs and status (`pending`, `running`, `completed`, `failed`, `cancelled`, `unavailable`). A stage consumes only verified output from its dependencies. Preserve earlier outcomes when another stage starts or fails.

Retain full diagnostic records with `stage`, `severity` (`error|warning|info`), `kind`, message, source path and suggested action. Group by severity plus kind, never tag alone. In CLI summaries show counts and errors by default; keep warnings/information available in the full report. If the host offers disclosures, close the entire panel without errors, otherwise open only error groups. This skill does not provide a UI component.

Write an authorized task report with all stage outcomes and artifact paths, or return it in the conversation when file output was not requested. Never erase previous stage logs on a progress reset. Clear a retained report only on explicit user instruction. Redact credentials and provider payloads. Distinguish a successful source generation from preview/export success and preserve partial outputs on failure.

## 中文

为用户请求建立一个任务标识与有序阶段列表，记录每阶段的输入、输出及状态（`pending`、`running`、`completed`、`failed`、`cancelled`、`unavailable`）。阶段只消费已验证的依赖输出，后续阶段开始或失败时仍保留前序结果。

完整诊断记录包含 `stage`、`severity`（`error|warning|info`）、`kind`、消息、来源路径和建议操作。按严重级别加标签分组，不能仅按标签合并。CLI 摘要默认显示计数与错误，完整报告保留警告及信息。若宿主提供折叠界面，无错误时整体收起，有错误时仅展开错误组。本技能不提供界面组件。

在已授权范围内写入包含所有阶段结果和产物路径的报告；未请求文件输出时在会话中返回。进度重置不得擦除前序日志，只在用户明确要求时清空保留的报告。隐去凭据及 provider 载荷，区分源生成与预览/导出成功，失败时保留部分产物。
