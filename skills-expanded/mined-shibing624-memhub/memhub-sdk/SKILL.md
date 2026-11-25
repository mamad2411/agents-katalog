---
name: memhub-sdk
description: >
  通过 memhub 为 agent 管理长期记忆：跨工具个人记忆中枢（Hub）、写入、检索、更新、删除与 scope 管理。
  触发场景：用户透露稳定个人信息/偏好、陈述值得长期记住的事实或计划、沉淀工程排障经验，或对话需要
  回忆该用户过去说过什么时。使用 MCP 工具或 CLI（memhub）调用 Hub Core 或 MemoryClient 方法。
---

# memhub 记忆技能

`memhub` 提供两层能力：
1. **跨工具个人记忆中枢（Hub）**：让本机 18 种 AI 工具（`claude-code`、`codex`、`cursor`、`agentica`、`hermes`、`codebuddy`、`opencode`、`workbuddy`、`kimi-cli` / `kimi-code`、`dsh`、`trae`、`zcode`、`qoder`、`copilot`、`kiro`、`cline`、`pi`、`openclaw`）共享同一份本地记忆，支持 `memhub ui` 可视化管理与跨设备同步（`git` / `dir` / `ssh` / `http`）。
2. **双系统分层记忆 SDK（`MemoryClient` / `SyncMemoryClient`）**：把对话与工具轨迹沉淀为四层长期记忆（`L0_RAW` / `L1_FACT` / `L2_PROFILE` / `L3_DERIVED`），检索时按 `profile` / `proactive` / `normal` / `procedures` / `schema` / `catalog` / `raw` 分组返回。它管**跨会话记忆**，不能替代 Agent 自己的当前窗口（WorkingMemory）。

## 1. 跨工具个人记忆中枢（Hub CLI）

日常在本机使用多个 AI 工具时，推荐直接用 `memhub` 一级命令管理共享记忆：

```bash
# 启动后台常驻服务（开机自启；卸载用 memhub uninstall-service）
memhub install-service

# 按需接入你正在用的 AI 工具（卸载用 memhub uninstall-host <工具名>）
memhub install-host claude-code
memhub install-host codex
memhub install-host cursor
# 支持：claude-code | codex | cursor | agentica | hermes | codebuddy | opencode | workbuddy | kimi-cli | kimi-code | dsh | trae | zcode | qoder | copilot | kiro | cline | pi | openclaw | all

# （可选）导入已有历史会话
memhub scan --source claude-code   # 或 --source all

# 跨工具检索记忆 + 历史原话
memhub recall "之前关于数据库锁冲突是怎么解决的"

# 在浏览器打开 http://127.0.0.1:8765/ui 按项目查看、搜索、编辑、删除记忆
memhub ui

# 查看 Core 状态、队列与宿主接入情况
memhub status

# 跨设备同步（优先推荐私有 Git 仓库）
memhub connect git git@github.com:you/my-memory.git
memhub connect dir "~/Library/Mobile Documents/com~apple~CloudDocs/memhub"
memhub connect ssh user@your-server
memhub sync
memhub disconnect
```

## 2. SDK 与社区生态集成（`memhub.integrations`）

memhub 原生对接 5 类社区生态，统一入口在 `memhub.integrations`：

| 生态 | 接入方式 | 关键文件 / 命令 |
|------|----------|----------------|
| skill | 本 `SKILL.md` + `MemoryClient` | `memhub/skills/memhub-sdk/SKILL.md` |
| mcp | MCP server（`memhub-mcp`，stdio / streamable-http） | `memhub/mcp/server.py` |
| hermes agent | `MemHubHermesProvider` 原生插件（被动 prefetch + 异步 `sync_turn`） | `memhub/integrations/hermes.py` |
| openclaw | `MemHubOpenClawProvider` 原生插件（同源 `MemoryProvider` 契约） | `memhub/integrations/openclaw.py` |
| agentica | `MemHubMemory` 记忆模块（`add_messages` / `retrieve`）+ `MemHubWorkspace`（`Agent(workspace=…)` 直接接入） | `memhub/integrations/agentica.py` |
| claude code | `memhub-hook` 子命令（`UserPromptSubmit` / `Stop`） | `memhub/integrations/claude_code.py` |

所有适配器都基于内嵌 `MemoryClient`，配置走 `~/.memhub/config.yaml` 或 `MEMHUB_*` 环境变量。程序化构造：

```python
from memhub.integrations import get_backend
mcp_server = get_backend("mcp")                       # MCPServer 实例
hermes = get_backend("hermes")                        # 注册进 Hermes runtime
openclaw = get_backend("openclaw")
memory = get_backend("agentica", user_id="u1")        # agentica 记忆模块
```

### agentica SDK 接入

agentica 的 `Agent` 通过 `workspace` 对象消费长期记忆。memhub 提供两层接入，均无需改动 agentica 框架代码：

- **`MemHubMemory`（记忆模块）**：暴露 `add_messages` / `retrieve`，用于手动把召回结果注入 system prompt。
- **`MemHubWorkspace`（Workspace 适配器）**：组合原生 agentica `Workspace`（承接 `AGENTS.md` / `PERSONA.md` / `USER.md` / `skills` 等文件型上下文），仅把「语义记忆」相关方法覆盖为调用 memhub。可直接 `Agent(workspace=...)`，自动召回 + 自动保存。

```python
from memhub.integrations.agentica import get_agentica_memory_backend
from agentica import Agent

ws = get_agentica_memory_backend(
    user_id="u1",                 # 或 client=<已构造的 MemoryClient>
    workspace_dir=".agentica",    # 文件型上下文（AGENTS.md 等）落盘目录
)
agent = Agent(workspace=ws, enable_long_term_memory=True)
```

## 3. 工具 ↔ CLI ↔ REST ↔ SDK 对照

| MCP 工具 | CLI | REST（`memhub serve-api`） | MemoryClient |
|---|---|---|---|
| `memory_add` | `memhub add` | `POST /v1/memories/` | `add` |
| `memory_search` | `memhub search` | `POST /v1/memories/search` | `search` |
| `conversation_search` | `memhub search-conversation` | `POST /v1/memories/search_conversation` | `search_conversation` |
| `memory_list` | `memhub list` | `GET /v1/memories/` | `list` |
| `memory_get` | `memhub get <id>` | `GET /v1/memories/{id}` | `get` |
| `memory_update` | `memhub update` | `PUT /v1/memories/{id}` | `update` |
| `memory_delete` | `memhub delete` | `DELETE /v1/memories/{id}` | `delete` |
| `memory_delete_scope` | `memhub delete-scope` | `DELETE /v1/memories/?confirm=true` | `delete_bulk` |
| `memory_list_scopes` | `memhub list-scopes` | `GET /v1/scopes/` | `list_scopes` |
| `memory_digest` | `memhub digest` | `POST /v1/digest/` | `digest` |

发现：`GET /v1/capabilities` 返回完整 HTTP 映射。

## 4. 归属标识（scope）与写入方式

**单产品默认：只传 `user_id` 即可**（`app_id` 省略时用 config 的 `default_app_id`，默认 `"default"`）。
- **`user_id`** — 终端用户 ID（SDK/独立 MCP 必填；Hub MCP 已自动绑定个人 scope，无需传）
- **`workspace_id` / `branch`** — 可选；带工具轨迹的 Coding 会话用来限定 `procedure` 工程经验的版本边界
- **`app_id` / `agent_id` / `session_id`** — 可选隔离维度

| 方式 | API | 适用 | 代价 |
|------|-----|------|------|
| 单条实时 | `add(content=...)` | 关键事实需立刻落库 | 1 次生成 + 1 次 JEV 裁决 + embed |
| 多轮批量 | `add(messages=[...])` | 会话末沉淀（含工具调用轨迹自动抽 `procedure`） | 整段对话走 1 次 pipeline |
| 先存原文 | `add_raw` 再 `distill` | 先保留原话，之后再抽结构化记忆 | `distill` 复用已有 `L0_RAW`，不再写第二条原文 |

## 5. 何时写入与检索

**何时写入（`memory_add`）**：
- 稳定画像：身份、职业、所在地、长期偏好、技术栈约定
- 值得记住的事实、计划或纠正旧信息（自动形成演化链）
- 工程排障结论：在带 `tool_calls` / `role="tool"` 的 `messages` 中写入，自动提炼 `task / solution / files`

**何时检索（`memory_search` / `conversation_search`）**：
- 需要个性化背景（「按我习惯推荐」）或项目历史排障经验（传 `procedure_limit=3`）
- 用户问「我之前说过什么 / 原话是什么」时用 `conversation_search`

## 6. CLI 与 MCP 示例

```bash
# 写入单条或多轮对话（含 Coding 会话）
memhub add --content "用户在深圳做 ML" --user-id u1
memhub add --messages-file messages.json --user-id u1 --workspace-id ~/code/app --branch main

# 检索与管理
memhub search "用户做什么工作" --user-id u1
memhub search "SQLite database is locked" --user-id u1 --procedure-limit 3
memhub search-conversation "原话" --user-id u1
memhub list --user-id u1 --include-history
memhub get <memory_id>
memhub update <memory_id> --content "新内容"   # 返回新 id，旧 id 仍可 get
memhub delete <memory_id>                     # 归档当前版本，不物理删除
memhub digest --mode dual                     # dual 模式生成 L3_DERIVED
```

```text
memory_add(user_id="u1", content="...")
memory_add(user_id="u1", messages=[{"role":"user","content":"..."}, ...], workspace_id="~/code/app")
memory_search(query="...", user_id="u1", procedure_limit=3)
conversation_search(query="...", user_id="u1")
memory_list(user_id="u1", include_history=false)
memory_get(memory_id="...")
memory_update(memory_id="...", content="...")   # 返回新 id
memory_delete(memory_id="...")                  # 归档当前版本
memory_digest()                                 # dual → L3_DERIVED
```

## 7. 检索结果解读

- **profile** — `L2_PROFILE` 画像与当前状态（优先参考）
- **proactive** — `L1_FACT` 里 `kind=intention` 的计划/待办意图；默认 `intention_limit=0` 为空
- **normal** — `L1_FACT` 事实与事件。默认检索不返回 `L0_RAW`；核对原话用 `conversation_search`
- **procedures** — `L1_FACT` 里 `kind=procedure` 的工程排障经验（`item.procedure` 含 `task` / `solution` / `files` / `workspace_id`）；传 `procedure_limit > 0` 时返回
- **catalog / schema** — `dual` 模式下 `digest()` 生成的 `L3_DERIVED` 画像目录与跨证据行为规律
- **evolution_chain / previous**：同一记忆多次更新时，`evolution_chain` 按最新→最旧排列（`[0]` 为当前版本，传 `include_derived=True` 展开完整链），`previous` 默认带一跳旧值。
