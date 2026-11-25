---
name: artifact-yylo
title: YYLO Ledger 证据归档库
description: 当编码智能体需要把测试报告、模型输出、操作回执等运行证据固化为可验证的不可变 artifact Record 时使用；驱动 yy ledger 完成证据画像与载荷模式分类、显式创建、溯源与保留选择，以及按摘要与历史回读的检索核验；不适用于任务状态、持久知识或工作流定义；触发词：artifact、证据、回执、receipt、digest、不可变、yy ledger
domain: 智能/agents
triggers: [运行证据归档, artifact Record 创建与检索, report/receipt/model-output 证据分类, inline/local/external 载荷模式选择, digest 与溯源核验, 保留策略 temporary/standard/permanent, 不可变证据替代与归档, yy ledger artifact 命令]
tags: [证据, artifact, 归档, 回执, 不可变, 编码智能体, yylo, cli]
level: 进阶
status: stable
agents: [claude-code, codex]
tools: [yy]
requires: []
related: [ledger-tasks-yylo, wiki-yylo, workflow-yylo, agent-memory-systems]
combines_with: [postmortem-writer, error-log-detective]
license: MIT
source: yylo-dev/yylo-skills
source_license: MIT
---

# YYLO Ledger 证据归档库

采编自 yylo-dev/yylo-skills（MIT），由 YYLO 团队自荐并适配为本库格式。

## 何时使用

当智能体要把「运行证据」放进比日志文件更可靠、可被审查与复验的载体时使用：

- 捕获或检索 artifact Record：测试报告、模型输出、操作回执等持久证据。
- 按意图选择证据画像（stdout / model-output / report / receipt）与载荷模式（inline / local / external / link），并绑定溯源与保留策略。
- **不该用**：任务状态（走 Task）、持久知识（走 Wiki）、工作流定义（走 Workflow）；发布 / 部署 / 生产变更（捕获证据不授予执行权限）。

## 步骤 / 指令

1. **预检**：`yy ledger artifact --help`（命令 help 为当前运行时的权威说明）；命名空间缺失时禁止发明命令或手写存储文件。
2. **先分类**：按证据选画像——stdout 有界输出 / model-output 模型响应 / report 生成结果 / receipt 操作与结果绑定；按后续核验需求选载荷模式：需要字节级证明时选不可变模式（inline / local / external），link 只是 URI 引用，不是内容寻址证明。
3. **显式创建**（文件/stdin 传输 + 媒体类型）：

   ```bash
   yy ledger artifact create --title "Focused test report" --profile report \
     --mode local --media-type application/json --file report.json
   ```

   绝不在 URI 里嵌凭据；只附受支持的非秘密溯源（actor / agent / model / session / run / task / workflow，任务与工作流溯源用不可变 Record ID）；保留策略（temporary / standard / permanent）显式选择，保留元数据本身不授权删除。
4. **检索与核验**：先检查 `yy ledger get --help`；已知 ID 优先 `yy ledger get RECORD_ID -f json`（不猜类型）。若当前 get 仅支持 Task，检查 `yy ledger record get --help` 后使用 `yy ledger record get RECORD_ID -f json`；仍不支持通用 Record 时停止并请求升级，不改猜其他类型。无 ID 先有界检索：

   ```bash
   yy ledger artifact search --profile report --projection summary --limit 20 -f json
   ```

   元数据回读 `yy ledger artifact get RECORD_ID -f json`，修订历史 `yy ledger artifact history RECORD_ID -f ndjson`；仅在当前 help 确认支持内容读取参数时，用 `yy ledger get RECORD_ID --content --max-content-bytes 1048576` 核验字节（选新的外部输出文件并检查退出码，上限 16 MiB）；不支持则请求升级，不以元数据回读代替字节核验。
5. **不可变纪律**：载荷字节绝不覆写；替代 = 显式 predecessor/successor 关系 + 修订安全契约；归档是生命周期迁移不是删除；新 ID 用 `artifact_` 前缀，不给既有 ID 加前缀。
6. **结果上报**：上报 Record kind / profile、真实不可变 ID 与真实 slug（来自返回 Record 或原生 get 回读），绝不凭标题编造 slug。

## 示例

```
yy ledger artifact create --title "Focused test report" --profile report --mode local --media-type application/json --file report.json
yy ledger artifact search --profile report --projection summary --limit 20 -f json
yy ledger get artifact_ab12cd34 -f json
yy ledger artifact history artifact_ab12cd34 -f ndjson
yy ledger get artifact_ab12cd34 --content --max-content-bytes 1048576 > evidence.out
```

## 注意事项

- 元数据/摘要回读不是字节往返证明：依赖精确字节前先核验 profile、mode、media type、digest、size、溯源、保留、revision 与不可变 ID；损坏即停，绝不静默改用其他修订。
- 外部/link 载荷 Ledger 绝不代下载，外部获取需单独授权；universal get 内嵌可读内容默认 64 KiB，超出返回省略原因而非空成功。
- 运营文档（PDR、架构与迁移契约、计划、报告、回执、执行证据）走 Artifact Record，不进产品 `docs/`、任务正文或手工控制器路径；API 不可用时保留外部草稿并请求 Ledger 升级。
- 存储、发布、生产变更互不授权：捕获证据绝不隐含发布、部署或生产变更权限。

## 互见

- requires：无硬前置。
- related：`ledger-tasks-yylo`（同一家族的任务看板技能，任务状态走它）、`wiki-yylo`（同一家族的持久知识技能，Wiki/Task/Workflow/Artifact 归属判别）、`workflow-yylo`（同一家族的工作流定义技能，其运行输出归本技能的证据通道）、`agent-memory-systems`（同类中的智能体记忆系统，记忆与不可变证据的边界判别）。
- combines_with：`postmortem-writer`（复盘报告定稿后固化为 report 证据 Record）、`error-log-detective`（排障结论与关键输出存为可复查证据）。
