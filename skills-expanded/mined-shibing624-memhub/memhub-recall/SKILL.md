---
name: memhub-recall
description: 用户的全局个人记忆（memhub MemHub，跨 Agentica / Claude Code / Cline / CodeBuddy / Codex / Copilot / Cursor / DeepSeek Harness / Hermes / Kimi / Kiro / OpenClaw / OpenCode / Pi / Qoder / Trae / WorkBuddy / ZCode 共享）。回答涉及用户的偏好、项目约定与规范、代号、命令、过往决策的问题时使用，尤其是当前目录和代码里查不到答案时；用户要求「记住 / 别忘了 / 以后都按这个 / 改掉 / 撤销 / 更新 / 忘掉 / 删掉」某条记忆或约定，或问「我之前问过什么 / 之前在别的 CLI 聊到哪了」，或提到 memhub 记忆时也使用。
---

<!-- managed by memhub hub -->

# memhub MemHub 个人记忆

本机所有工具共用一个 Hub Core，当前宿主是 `{host}`。工具已绑定个人记忆，
不需要也不能传 `user_id` / `app_id` / `agent_id`。

每轮提问时，相关记忆通常已经以 `<relevant-memories>` 注入上下文。它是检索时生成的摘要和
原始对话片段，不是可编辑的记忆条目。先用注入内容，不够再查。普通对话结束后 Hook 会自动采集。

## 优先：宿主内置的 MCP 工具

优先调用宿主内置的 `memhub` MCP 工具，不要改用 CLI。

| 用户意图 | MCP 工具（`memhub`） | 说明 |
|---|---|---|
| 按记忆 ID 精确展开目录条目（渐进式披露） | `memory_get(memory_id="a1b2c3d4")` | 看到 `<relevant-memories>` 里的 `[procedure-index id=a1b2c3d4]` 或项目视图条目需要完整方案时，直接按 ID 精确读取 |
| 查偏好、画像、事实、历史结论 | `memory_search(query="...")` | 语义检索当前记忆，返回带 `id` 和 `source_id` 的列表 |
| 按 L0 来源 ID 展开完整原话（渐进式披露） | `conversation_search(source_id="37c85fe9", context_turns=1)` | 看到 `<relevant-memories>` 里的 `(来源: L0 37c85fe9)` 或 `source_id` 想核对完整原话及前后轮次时按需调用 |
| 查「我之前说过 / 问过什么」的原话 | `conversation_search(query="...")` | 返回历史对话原文；`session_id` 形如 `codex:<id>`，冒号前是来源工具 |
| 记住 / 别忘了 / 以后都按这个 | `memory_add(content="...")` | `content` 写成一条完整、可独立理解的第三人称陈述句 |
| 改掉 / 撤销 / 更新某条约定 | `memory_list(query="...")` 取 `id` → `memory_update(memory_id=id, content="...")` | 找不到匹配项就直接 `memory_add` 写新约定 |
| 忘掉 / 删掉某条记忆 | `memory_list(query="...")` 取 `id` → `memory_delete(memory_id=id)` | 只在用户明确要删除时用 |
| 排查 memhub 自身故障 | `memory_status()` | 查看 Core、记忆数量和写队列状态 |

返回内容都有上限，不会整段塞进上下文：`memory_search` 每条截到 600 字，`memory_list` 每条只给 200 字预览，
`conversation_search` 每段截到 1500 字（`source_id` 指向的那段 8000 字），被截断的条目末尾标着
`…[已截断，原文共 N 字]`。要看某条的全文，用 `memory_get(id)` 或 `conversation_search(source_id=...)` 单独展开，
不要调大 `limit` 去凑。

`memory_add` 返回 `ok: true` 就是成功终态；`status` 可能是 `pending`，后台会自动抽取。
找不到旧条目是正常结果：注入内容可能来自原始对话摘要，库里未必有对应的可编辑记录，
这时直接 `memory_add` 写一条新约定即可。

## 备选：CLI（MCP 工具不可用或未激活时）

CLI 入口是 `python3 -m memhub.cli <子命令>`，安装后也可直接 `memhub <子命令>`；
须使用装有 memhub 的解释器，本机等价入口是 `{cli}`。
下表是可以直接执行的完整命令（已带解释器路径和 `--hub-dir`），作用与对应的 MCP 工具相同：

| 要做的事 | 命令 |
|---|---|
| 按记忆 ID 精确展开完整方案 | `{memory_get} <记忆ID或8位前缀>` |
| 查询记忆与历史对话 | `{recall} "要查的内容"`（加 `--source-id <L0短ID>` 可直接展开对应 L0 原话及上下文） |
| 记住一件事 | `{remember} "要记住的内容"` |
| 列出当前记忆（含 `id`） | `{memory_list} "关键词"` |
| 改掉一条约定 | `{memory_update} <id> "新内容"` |
| 忘掉一条记忆 | `{memory_delete} <id>` |
| 查看 Core 状态 | `{status}` |

`{memory_list}` 每行是 `id`、层级和内容摘要（正文压成一行），加 `--json` 可输出完整字段。
这些命令与 `memhub add` / `search` / `update` / `delete` / `list` 不同：后几个是 SDK 命令，
会写进当前目录下另一个独立的库。

## 隐私：让某段内容不入库

不想被记住的片段用 `<private>...</private>` 包起来，采集时整段丢弃，同一轮里标签外的内容照常入库：

```
我的数据库密码是 <private>hunter2</private>，连接串是 postgres://db:5432/app
```

标签内的 `hunter2` 不会进库，标签外的连接串会；标签外的回答或工具输出若复述它，仍可能被采集。
整条提问用 `<private>...</private>` 包住时，本轮提问、回答和工具记录都不写入 MemHub。
本机的 `memhub_excluded_projects` 可停用匹配目录的采集与召回；当宿主未提供项目根时，MCP 记忆工具可传 `workspace` 供排除检查。
