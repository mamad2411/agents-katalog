---
name: trajectory-view
description: 生成并打开当前或指定 Codex 会话的轨迹树、Eval、项目总览或代码执行视图。
---

用 Node 运行本目录相对路径 `../../../../scripts/trajectory-view.mjs --host codex --serve --keep-alive`，保留执行会话并打开返回的本机 `url`。默认从 `CODEX_THREAD_ID` 取得当前对话，指定其他会话时加 `--thread ID`。验证页面实际打开后交付。

按用户请求选择生成内容：默认轨迹树，`--eval` 打开会话 Eval，`--overview` 打开当前项目总览，`--code` 直接进入 Eval 的代码执行分析。一次只选一种。总览可以加 `--project PATH`，或重复 `--thread ID`、`--file SNAPSHOT` 选定来源；这些入口沿用同一数据和诊断流程。

The interface automatically follows the browser language. Add `--lang en` or `--lang zh-CN` only when a language is explicitly requested; `--lang auto` restores automatic selection. Preserve the language of the source conversation.

轨迹图长按或聚焦对象后按 Shift+Enter 可选取诊断，填写问题后复制草稿。沿草稿查询取证时保留会话、cut 和 logId；用户自己的问题优先于默认关注点。
