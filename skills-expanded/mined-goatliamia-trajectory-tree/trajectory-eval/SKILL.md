---
name: trajectory-eval
description: 打开当前或指定 Codex 会话的 Eval 图表，按轮次检查有记录的用量、耗时和工具结果。
---

用 Node 运行本目录相对路径 `../../../../scripts/trajectory-view.mjs --host codex --eval --serve --keep-alive`，保留执行会话并打开返回的 `url`。默认读取 `CODEX_THREAD_ID`，指定其他会话加 `--thread ID`，已捕获会话加 `--file SNAPSHOT`。验证页面实际打开后交付。

用户要项目总览时，改用 `--host codex --overview --serve`。默认按当前目录读取最近的项目会话，可用 `--project PATH` 或重复 `--thread ID`、`--file SNAPSHOT` 选定范围。用 `--lang en` 或 `--lang zh-CN` 固定界面语言。

用户指定命令、脚本或 PowerShell 报错时，用 `--code` 替代 `--eval`，直接进入同一会话 Eval 的代码执行分析。运行指标、代码执行与处理线索共用同一切点。

从图表详情选择要诊断的轮次、工具或报错，复制草稿回 Codex 输入框。用随包的 `trajectory-query.mjs` 执行草稿里的查询，保留其中的 `cut` 和 `logId`。如果图表来自手动捕获的快照，CLI 取证也使用同一个 `--file` 和 `--rollout`（如有）。

草稿带有取证快照时，优先用 `--evidence "<快照路径>"` 查询这份固定记录。
