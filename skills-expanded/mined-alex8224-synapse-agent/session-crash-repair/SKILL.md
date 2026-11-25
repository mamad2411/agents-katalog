---
name: session-crash-repair
description: Detect and repair a Synapse session whose LangGraph checkpoint was left inconsistent after an abnormal process exit (dangling tool calls, pending graph tasks, stale transcript projection).
license: Apache-2.0
compatibility: Requires a synapse source checkout with uv and Python 3.12+.
allowed_tools: execute, read_file, write_file, search_files, find_files
---

# Session Crash Repair

进程异常退出（崩溃 / 被强杀）后，会话的 LangGraph checkpoint 可能停在一次工具调用中间，
导致重新打开该会话时：agent 卡住、历史不完整、甚至恢复执行了不该执行的挂起命令。

本 Skill 描述如何**检测**这种不一致，以及如何**修复**会话数据，使其恢复到可继续的干净状态。

## 触发场景

- 用户报告某会话（thread_id）"没正确记录 / 打不开 / 继续时行为异常"，且此前进程异常退出。
- 打开会话后 agent 立即执行了一个与当前请求无关的工具（可能是崩溃前遗留的挂起命令）。
- 转录里最后一轮停在一条"AI 决定调用工具"之后，没有任何工具结果。

## 数据文件

| 文件 | 作用 | 说明 |
| --- | --- | --- |
| `<project>/.synapse/checkpoints.sqlite` | LangGraph 状态（消息、图任务） | **事实来源**，修复主目标 |
| `<project>/.synapse/sessions.sqlite` | 会话元数据（标题/模型/摘要） | 通常不受崩溃影响 |
| `<project>/.synapse/transcript.sqlite` | 转录投影（TUI 展示用的派生缓存） | 崩溃后可能过期，需重建 |

## 第 1 步：检测

用 `SqliteSaver` 直接读取目标 thread 的 head checkpoint，不要通过正在运行的进程（可能已死）。
把下面的脚本写成临时文件（例如 `/.tmp/detect.py`）并用 `uv run --no-sync python` 执行：

```python
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from synapse.sessions.transcript import load_messages_from_checkpointer

THREAD = "<thread_id>"                                   # 待修复的会话 ID
CHECKPOINT = "<project>/.synapse/checkpoints.sqlite"     # 绝对路径

conn = sqlite3.connect(CHECKPOINT, check_same_thread=False)
saver = SqliteSaver(conn)
config = {"configurable": {"thread_id": THREAD}}

tup = saver.get_tuple(config)
print("head checkpoint:", tup.checkpoint["id"])
print("step:", tup.metadata.get("step"))
print("pending_writes:", tup.pending_writes)

vals = tup.checkpoint.get("channel_values") or {}
print("__pregel_tasks:", vals.get("__pregel_tasks"))

msgs = load_messages_from_checkpointer(saver, THREAD)
print("messages:", len(msgs))
print("last message:", type(msgs[-1]).__name__ if msgs else None)

# 悬挂工具调用：AIMessage 声明了 tool_call，但没有对应 ToolMessage
answered = {str(getattr(m, "tool_call_id", None)) for m in msgs if getattr(m, "tool_call_id", None)}
dangling = []
for m in msgs:
    t = (getattr(m, "type", None) or type(m).__name__).lower()
    if t in ("ai", "assistant", "aimessage"):
        for c in (getattr(m, "tool_calls", None) or []):
            cid = c.get("id") if isinstance(c, dict) else getattr(c, "id", None)
            if cid and str(cid) not in answered:
                name = c.get("name") if isinstance(c, dict) else getattr(c, "name", None)
                dangling.append((cid, name))
print("dangling tool calls:", dangling)

conn.close()
```

### 判定标准（出现任意一条即需要修复）

1. `__pregel_tasks` 非空，含 `Send(node='tools', arg=[...])` —— 恢复时会**执行**这个挂起的工具。
2. `dangling tool calls` 非空 —— 最后一条 AIMessage 有工具调用但没有工具结果，消息链不闭合。
3. 在 agent 上 `agent.get_state(config).next` 非空（`('tools',)` 等）。

### 关键风险

挂起的工具可能是**危险命令**（例如 kill 进程、删除文件）。**绝不能直接对同一 thread_id 发起新的
invoke/astream 让图"自然恢复"**，那会把挂起任务执行掉。必须先修复再继续。

## 第 2 步：修复 checkpoint

复用项目自带的取消修复逻辑 `repair_thread_after_cancel`，并用 `as_node=END` 兜底清空残留的
中间件 pending 任务。写成临时脚本执行：

```python
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END

from synapse.settings import load_project_settings
from synapse.app.agent import build_coding_agent
from synapse.sessions.cancel_repair import repair_thread_after_cancel

THREAD = "<thread_id>"           # 待修复的会话 ID
WORKSPACE = "<absolute project root>"

settings = load_project_settings(workspace=WORKSPACE)
conn = sqlite3.connect(settings.checkpoint_path, check_same_thread=False)
saver = SqliteSaver(conn)
agent = build_coding_agent(
    settings,
    project_root=WORKSPACE,
    checkpointer=saver,
    load_mcp=False,
)

config = {"configurable": {"thread_id": THREAD}}

# 1) 密封悬挂工具调用（写 ToolMessage）+ 追加边界注释（synapse_cancel_boundary）
notes = repair_thread_after_cancel(agent, config, reason="crash")
print("repair notes:", notes)

# 2) 该函数按 next 里的第一个非 tools 节点写边界注释，可能命中 before_model 中间件，
#    从而留下 `inject_steer_queue.before_model` 之类的残留 pending 任务；用 END 封死。
state = agent.get_state(config)
if tuple(getattr(state, "next", ()) or ()):
    agent.update_state(config, None, as_node=END)

# 3) 验证
state = agent.get_state(config)
print("next:", getattr(state, "next", None))
msgs = (getattr(state, "values", None) or {}).get("messages") or []
print("messages:", len(msgs))
for m in msgs[-2:]:
    print(type(m).__name__, getattr(m, "tool_call_id", None),
          str(getattr(m, "content", "") or "")[:60])
    ak = getattr(m, "additional_kwargs", None) or {}
    print("  flags:", {k: v for k, v in ak.items() if k.startswith("synapse")})

conn.commit()
conn.close()
```

### reason 参数语义

| reason | 密封内容 | 边界注释内容 |
| --- | --- | --- |
| `"crash"`（推荐，进程异常退出） | `[cancelled]` | 空内容 + `synapse_cancel_reason="crash"` |
| `None` / `"user"` | `[cancelled by user]` | `[本轮已由用户终止，上下文已保留]` |

## 第 3 步：重建转录投影

`transcript.sqlite` 是派生缓存，且 `contains_thread()` 只判断"是否存在"，**不会**因 checkpoint
变化自动失效。崩溃前的投影会停留在旧的轮次，必须手动重建：

```python
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from synapse.sessions.transcript import load_messages_from_sqlite_file
from synapse.sessions.transcript_projection import TranscriptProjection

THREAD = "<thread_id>"
CHECKPOINT = "<project>/.synapse/checkpoints.sqlite"
PROJECTION = "<project>/.synapse/transcript.sqlite"

# 新的 head checkpoint id（修复后）
conn = sqlite3.connect(CHECKPOINT, check_same_thread=False)
saver = SqliteSaver(conn)
head_id = saver.get_tuple({"configurable": {"thread_id": THREAD}}).checkpoint["id"]
conn.close()

messages = load_messages_from_sqlite_file(CHECKPOINT, THREAD)
projection = TranscriptProjection(PROJECTION)
projection.replace_from_messages(THREAD, messages, source_checkpoint_id=head_id)
projection.close()
```

## 验证清单（修复完成后必须全部满足）

- [ ] `agent.get_state(config).next == ()` —— 无挂起图任务。
- [ ] `checkpoint["channel_values"]["__pregel_tasks"]` 为空（或不存在）。
- [ ] 无悬挂工具调用；最后一条 AI 工具调用都有匹配的 `ToolMessage`。
- [ ] 消息末尾是密封 `ToolMessage` + `synapse_cancel_boundary=True` 的边界 `AIMessage`。
- [ ] `transcript.sqlite` 的 `transcript_meta.total_turns` 覆盖到崩溃前的最后一轮。
- [ ] 用 `read_session`（或 TUI 重新打开）确认最后一轮正常显示、可直接继续新的一轮。

## 注意事项

- 修复前先跑**只读检测脚本**确认是悬挂工具调用场景；不要对无异常会话执行修复。
- checkpoint 是追加式不可变存储：修复只新增 head checkpoint，不修改历史；若出错可删除新增的
  checkpoint 行回滚。
- 只读阶段用 `SqliteSaver`（同步）即可；不要开启 MCP、不要触发模型调用（`load_mcp=False`）。
- 构建 agent 仅用于调用 `get_state` / `update_state`，不会产生网络请求。
- 不要在任何脚本或 SKILL 内容中写入 API key / `.env` 内容。
