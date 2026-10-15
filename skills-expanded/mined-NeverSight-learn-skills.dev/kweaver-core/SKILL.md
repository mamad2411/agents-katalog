---
name: kweaver-core
description: >-
  通过 kweaverc CLI 登录 KWeaver 平台、与 Agent 对话、管理和查询业务知识网络（BKN）、
  调用 Context Loader 从知识网络检索概念和实例。
  当用户需要认证、Agent 对话、BKN 管理/查询、知识检索时使用。
---

# KWeaver Core

KWeaver 平台的 CLI 工具，覆盖认证、Agent 对话、BKN 管理与查询、Context Loader 检索四大能力。

## 安装

若未安装，提示用户执行：

```bash
npm install -g kweaver-caller
```

需 Node.js 22+。也可用 `npx kweaverc` 临时运行。详见项目根目录 [README.md](../../README.md) 的 Install 部分。

## 使用前提

**使用任何 kweaverc 命令前，必须先登录平台。** 若用户未认证，提示用户先执行 `kweaverc auth <platform-url>`。

登录流程：`kweaverc auth <platform-url>` 会自动注册 OAuth 客户端、打开浏览器、回调获取 token。可用 `--alias` 给平台取别名。若请求失败，优先检查当前平台是否正确、token 是否过期。详见 [README.md](../../README.md) 的 Auth 部分。

## 认证命令速查

```bash
kweaverc auth <platform-url>
kweaverc auth <platform-url> --alias <name>
kweaverc auth list
kweaverc auth status [platform-url|alias]
kweaverc auth use <platform-url|alias>
kweaverc auth logout [platform-url|alias]
kweaverc auth delete <platform-url|alias>
kweaverc token
```

## 2. Agent 对话

与 Agent 进行非交互式多轮对话。常用：`kweaverc agent list --pretty` 查看可用 Agent；`kweaverc agent chat <agent_id> -m "..." --no-stream` 发送消息；续聊时加 `--conversation-id <id>`。

详细命令、策略与约束见 [references/agent.md](references/agent.md)。

## 3. BKN 管理与查询

管理业务知识网络，以及通过 ontology-query 查询对象、子图、属性和行动。常用：`kweaverc bkn list --pretty` 列出网络；`kweaverc bkn get <kn-id> --pretty` 查看详情；`kweaverc bkn object-type query <kn-id> <ot-id> --limit 10 --pretty` 查询对象实例。

详细命令、参数与策略见 [references/bkn.md](references/bkn.md)。

## 4. Context Loader

从 BKN 检索 schema、实例、逻辑属性和行动信息。常用：`kweaverc context-loader config set --kn-id <kn-id>` 配置知识网络；`kweaverc context-loader kn-search "<查询>" --only-schema --pretty` 检索 schema。

详细 CLI/MCP 对应、三层数据流与约束见 [references/context-loader.md](references/context-loader.md)。

## BKN 与 Context Loader 的边界

- **bkn**：直接调用 ontology-query 原生接口，适合已知 `kn_id`、`ot_id`、`at_id` 且需透传 JSON 的场景
- **context-loader**：schema → 实例 → 逻辑属性/行动信息 的分层检索工作流，适合 Agent 化检索（需先 `kn-search` 发现 schema，再逐层调用）
