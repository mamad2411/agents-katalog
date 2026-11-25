---
name: build-managed-agents
description: 教 Claude Code / OpenClaw 等 coding agent 使用 Anthropic Claude Managed Agents（云端托管代理服务）API —— create/run/audit 全流程。当用户（或上游 coding agent）需要创建托管 agent、跑 session、流式处理事件、审计用量或调用 /v1/agents、/v1/environments、/v1/sessions 等 API 时使用。触发词：managed agents、托管代理、build a managed agent、agent_toolset_20260401、client.beta.agents、client.beta.sessions。
---

# build-managed-agents

这是一个给 coding agent（Claude Code / OpenClaw / Cursor agent 等）用的 skill —— 当 coding agent 需要帮用户构建基于 Claude Managed Agents 的应用时，照着本 skill 的 recipe 执行。

Anthropic 托管的 agent 运行时：云容器 + 内置工具 + 事件流。你不用自己搭 agent loop、工具执行、沙箱。

本 skill 覆盖三个阶段：**Create**（定义 agent/环境/session）→ **Run**（发消息、流式接收、处理工具确认）→ **Audit**（查状态、事件流、token 用量、成本）。

## 何时使用

- 用户要"创建一个 managed agent" / "托管 agent" / "跑一个 session"
- 代码里出现 `client.beta.agents`、`client.beta.environments`、`client.beta.sessions`
- 用户询问 `/v1/agents`、`/v1/environments`、`/v1/sessions` 等端点
- 用户要审计/调试 session（看事件流、token 消耗、错误重试）

## 前置条件

```bash
pip install anthropic  # Python
# 或 npm install @anthropic-ai/sdk  # TypeScript

export ANTHROPIC_API_KEY="sk-ant-..."
```

所有 API 需要 beta header：`anthropic-beta: managed-agents-2026-04-01`（SDK 自动加）。

Research preview 功能（outcomes / 多 agent / memory stores）需额外：`managed-agents-2026-04-01-research-preview`。

## 核心概念速查

| 概念 | 说明 | 生命周期 |
|------|------|---------|
| **Agent** | 模型 + system prompt + 工具 + MCP + skills | 复用，有版本号 |
| **Environment** | 云容器模板（预装包、网络规则） | 复用 |
| **Session** | 一次运行实例（Agent × Environment） | 一次性，有完整事件流 |
| **Event** | 会话中每条消息/工具调用/状态变更 | 永久存储，可审计 |

## 标准工作流

### 1. Create 阶段（一次性）

```python
from anthropic import Anthropic
client = Anthropic()

agent = client.beta.agents.create(
    name="My Agent",
    model="claude-sonnet-4-6",
    system="你的 system prompt",
    tools=[{"type": "agent_toolset_20260401"}],  # bash/read/write/edit/glob/grep/web_fetch/web_search
)

env = client.beta.environments.create(
    name="my-env",
    config={"type": "cloud", "networking": {"type": "unrestricted"}},
)
```

详细参数、MCP、skills、自定义工具、权限策略 → 见 `reference/create.md`

### 2. Run 阶段（每个任务一次）

```python
session = client.beta.sessions.create(agent=agent.id, environment_id=env.id)

with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(
        session.id,
        events=[{"type": "user.message", "content": [{"type": "text", "text": "..."}]}],
    )
    for event in stream:
        match event.type:
            case "agent.message":
                for block in event.content:
                    print(block.text, end="")
            case "agent.tool_use":
                pass  # 内置工具，系统自动执行
            case "agent.custom_tool_use":
                # 自定义工具 — 你必须发 user.custom_tool_result 回去
                ...
            case "session.status_idle":
                break
```

关键细节：
- **必须先开 stream 再 send**（不然前几个事件丢失）
- 遇到 `always_ask` 权限的工具，agent 会停下等 `user.tool_confirmation`
- 遇到 `agent.custom_tool_use`，你必须回 `user.custom_tool_result`，否则 session 卡死
- 要中断 agent 用 `user.interrupt`

完整事件类型表、图片/文档输入、多 agent、outcomes、memory stores → 见 `reference/run.md` 和 `reference/events.md`

### 3. Audit 阶段（任何时候）

```python
# 列出所有 session 状态
for s in client.beta.sessions.list(limit=50):
    print(s.id, s.status, s.usage.input_tokens + s.usage.output_tokens)

# 拉某个 session 的完整事件流（审计链）
for evt in client.beta.sessions.events.list(session_id):
    print(evt.type, evt.processed_at)

# 看 token 用量 + 时长
s = client.beta.sessions.retrieve(session_id)
print(s.usage, s.stats)
```

成本估算、按时间段过滤、错误分类统计 → 见 `reference/audit.md`

## 可用脚本

- `scripts/quickstart.py` — 一键跑通 create→run→audit 的最小模板
- `scripts/admin.py` — 管理工具（list-sessions / show / stats / cleanup）

直接 copy 到项目里改 system prompt 即可。

## 常见陷阱

1. **Agent 版本漂移**：生产环境要 pin 版本 `agent={"type": "agent", "id": "...", "version": N}`，否则 update 后静默升级
2. **Stream 顺序**：先 `.stream()` 打开通道，再 `.send()` 发消息，顺序反了会丢事件
3. **Custom tool 悬挂**：收到 `agent.custom_tool_use` 必须回 `user.custom_tool_result`（`is_error=True` 也行），否则 session 永远 idle
4. **Tool confirmation**：`always_ask` 权限下 agent 会停在 `session.status_idle` 且 `stop_reason.type="requires_action"`，需要 `user.tool_confirmation` 放行
5. **Rate limits**：Create 类 60/min，Read 类 600/min。列表操作尽量用 limit + pagination
6. **Archive vs Delete**：优先 archive（保留审计），delete 是永久的
7. **Running session 不能 delete**：先发 `user.interrupt` 让它 idle

## 参考文件索引

- `reference/create.md` — Agent/Environment/Session 完整创建参数
- `reference/run.md` — 事件收发、流式、多 agent、memory stores、outcomes
- `reference/events.md` — 所有事件类型 schema（agent.* / user.* / session.* / span.*）
- `reference/audit.md` — 列表查询、用量统计、成本估算、合规审计
- `reference/errors.md` — 错误类型、重试策略、状态机
- `scripts/quickstart.py` — 可运行模板
- `scripts/admin.py` — CLI 管理工具

## 官方文档

- https://platform.claude.com/docs/en/managed-agents/overview
- https://platform.claude.com/docs/en/managed-agents/quickstart
- https://platform.claude.com/docs/en/api/agents
