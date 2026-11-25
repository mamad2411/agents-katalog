---
name: session-cache-analysis
description: Analyze the prompt cache hit rate of a Synapse session (thread). Compute overall/per-turn/per-call cache hit rates from checkpoint usage metadata, distinguish normal incremental misses from full cache eviction, and diagnose the cause of an eviction using the model-request compression diagnostics.
license: Apache-2.0
compatibility: Requires a synapse source checkout with uv and Python 3.12+.
allowed_tools: execute, read_file, write_file, search_files, find_files, search_session, read_session
---

# Session Cache Hit-Rate Analysis

分析某个会话（thread）的 prompt 缓存命中率：算出整体/按轮/按调用的命中率，区分「正常的增量
miss」和「异常的缓存全量逐出」，并定位逐出的根因。

## 触发场景

- 用户问某会话的「缓存命中率」、缓存是否正常、为什么某轮命中率很低。
- 需要排查 token 成本异常（大量未命中输入）。
- 需要判断某次命中率塌陷是正常波动还是缓存被逐出。

## 数据文件

| 文件 | 作用 | 说明 |
| --- | --- | --- |
| `<project>/.synapse/checkpoints.sqlite` | LangGraph 状态（消息） | **事实来源**。每条 AIMessage 的 `usage_metadata` 里有缓存命中字段 |
| `<project>/.synapse/tool-outputs.sqlite` | 模型请求压缩诊断 | `model_request_compression_events` 表：每次调用的指纹与逐出诊断 |
| `<project>/.synapse/transcript.sqlite` | 转录投影 | `transcript_usage` 表**只存最后一轮**，不可当会话累计用 |
| `<project>/.synapse/search-index.sqlite` | 会话搜索索引 | 供 `search_session` / `read_session` 定位 thread_id |

## 核心概念

- `input_tokens` = 本次调用的总输入 token（DeepSeek `prompt_tokens`）。
- `cache_read` = 命中缓存的 token（DeepSeek `prompt_cache_hit_tokens`，synapse 映射到
  `usage_metadata.input_token_details.cache_read`）。
- `miss = input_tokens - cache_read`，`命中率 = cache_read / input_tokens`。
- 找不到 thread_id 时，先用 `search_session`（按标题/关键词）或 `read_session` 定位。

## 第 1 步：整体命中率

从 checkpoint 全量消息聚合，不要读 `transcript.sqlite`（它只存最后一轮）。写成临时脚本执行：

```python
import sys
sys.path.insert(0, "<project>/src")  # 若 synapse 已安装可省略

from synapse.sessions.transcript import load_messages_from_sqlite_file
from synapse.runtime.streaming.stream_events import aggregate_usage_from_messages

CHECKPOINT = "<project>/.synapse/checkpoints.sqlite"
THREAD = "<thread_id>"

messages = load_messages_from_sqlite_file(CHECKPOINT, THREAD)
print("messages:", len(messages))

totals = aggregate_usage_from_messages(messages)
print("input:", totals["input_tokens"], "cache:", totals["cache_tokens"],
      "output:", totals["output_tokens"])
hit = totals["cache_tokens"] / totals["input_tokens"] * 100 if totals["input_tokens"] else 0
print(f"整体缓存命中率 = {hit:.2f}%")
```

## 第 2 步：按调用 / 按轮次拆解，找下探点

```python
import sys
sys.path.insert(0, "<project>/src")

from synapse.sessions.transcript import load_messages_from_sqlite_file
from synapse.runtime.streaming.stream_events import _extract_usage

CHECKPOINT = "<project>/.synapse/checkpoints.sqlite"
THREAD = "<thread_id>"

messages = load_messages_from_sqlite_file(CHECKPOINT, THREAD)

def kind(m):
    t = type(m).__name__
    if t == "HumanMessage":
        return "user"
    if t == "AIMessage":
        return "ai"
    if t == "ToolMessage":
        return "tool"
    return t

turn = 0
print(f"{'turn':>4} | {'idx':>4} | {'input':>8} | {'cache':>8} | {'miss':>7} | {'hit%':>6}")
for i, m in enumerate(messages):
    if kind(m) == "user":
        turn += 1
    elif kind(m) == "ai":
        u = _extract_usage(m)
        if u["input_tokens"] or u["cache_tokens"]:
            miss = u["input_tokens"] - u["cache_tokens"]
            hit = u["cache_tokens"] / u["input_tokens"] * 100 if u["input_tokens"] else 0.0
            flag = "  <-- 大 miss" if miss > 3000 else ""
            print(f"{turn:4d} | {i:4d} | {u['input_tokens']:8d} | {u['cache_tokens']:8d} "
                  f"| {miss:7d} | {hit:5.1f}%{flag}")
```

观察 `miss` 骤升的调用（通常是某轮的第 1 次调用）。

## 第 3 步：区分两类 miss

| 判据 | 增量 miss（正常波动） | 全量逐出（异常） |
| --- | --- | --- |
| `cache_read` 绝对值 | **持续上升** | **骤降**（旧前缀丢失） |
| `input_tokens` | 明显增长（≈ 新工具结果大小） | 几乎不变 |
| miss 规模 | 几 K ~ 十几 K（≈ 前一步工具结果） | 几万 ~ 十几万（≈ 整个历史） |
| 后续调用 | 立即恢复 99%+ | 下次恢复（重新建缓存） |
| 根因 | 新工具结果还没进缓存 | 前缀失效（system/tools 变化或上游逐出） |

关键：**看 `cache_read` 绝对值，而不是命中率百分比**。大工具结果会撑大分母使百分比下降，
但 `cache_read` 绝对值仍上升；只有 `cache_read` 骤降才说明缓存真的被逐出。

## 第 4 步：逐出事件的根因诊断

用 `model_request_compression_events` 对比「失效那次调用」与「上一次调用」的指纹：

```python
import sqlite3
import json

DB = "<project>/.synapse/tool-outputs.sqlite"
THREAD = "<thread_id>"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
rows = conn.execute(
    "SELECT id, event_json, created_at FROM model_request_compression_events "
    "WHERE thread_id = ? ORDER BY id", (THREAD,)
).fetchall()

events = [json.loads(r["event_json"]) for r in rows]
print(f"{'id':>6} | {'turn':>4} | {'call':>4} | {'in':>8} | {'cache':>8} | {'hit%':>6} | "
      f"sys_chg | tool_chg | bust | created_at")
for r, e in zip(rows, events):
    cd = e.get("cache_diagnostics") or {}
    hit = e["provider_input_tokens"] and e["cache_read_tokens"] / e["provider_input_tokens"] * 100 or 0
    print(f"{r['id']:6d} | {e.get('turn_index'):4d} | {e.get('model_call_index'):4d} | "
          f"{e.get('provider_input_tokens',0):8d} | {e.get('cache_read_tokens',0):8d} | {hit:5.1f}% | "
          f"{str(cd.get('system_changed')):7} | {str(cd.get('tools_changed')):8} | "
          f"{str(cd.get('cache_bust_suspected')):5} | {r['created_at']}")
```

找到 `cache_read_tokens` 骤降的那一行（逐出事件），与它上一行做对比：

```python
# evict = 逐出事件的下标，prev = 它的上一行
ev = events[evict]
pv = events[evict - 1]
wf, pwf = ev.get("wire_fingerprints") or {}, pv.get("wire_fingerprints") or {}

print("system_hash 变化:", wf.get("system_hash") != pwf.get("system_hash"))
print("tools_hash   变化:", wf.get("tools_hash") != pwf.get("tools_hash"))
print("tool_count:", pwf.get("tool_count"), "->", wf.get("tool_count"))
print("message_count:", pwf.get("message_count"), "->", wf.get("message_count"))

a = [(p["tool_name"], p["schema_hash"]) for p in pv.get("tool_schema_profiles", [])]
b = [(p["tool_name"], p["schema_hash"]) for p in ev.get("tool_schema_profiles", [])]
print("删除的工具:", sorted({n for n, _ in a} - {n for n, _ in b}))
print("新增的工具:", sorted({n for n, _ in b} - {n for n, _ in a}))
print("工具顺序是否变化:", [n for n, _ in a] != [n for n, _ in b])

for k in ("summarization_saved_tokens", "prompt_saved_tokens",
          "tool_output_saved_tokens", "total_saved_tokens"):
    print(f"{k}: {pv.get(k)} -> {ev.get(k)}")
```

### 结果解读

| 信号 | 含义 |
| --- | --- |
| `system_hash` 变化 | 系统提示词变了（总结/压缩/注入内容变化） |
| `tool_count` 变化 / 工具增删 | 工具集真实变化（agent 重建） |
| `summarization_saved_tokens > 0` 或变化 | 历史被总结压缩 |
| `prompt_saved_tokens` 变化 | 发生了截断 |
| 全部不变 | 客户端前缀没变，逐出发生在**上游**（DeepSeek/网关） |

## 常见陷阱

1. **`transcript_usage` 不是会话累计**：`transcript.sqlite` 里该表每次 `INSERT OR REPLACE`，
   只保留最后一轮的 per-turn 用量；`last_cache_tokens` 恒为 0（持久化漏传）。要算整体命中率，
   必须从 checkpoint 消息聚合。
2. **`tools_hash` / `schema_hash` 被内存地址污染**：历史数据里（修复前）对 `StructuredTool`
   的 `model_dump()` 做 `json.dumps(default=str)`，把 `func` 序列化成 `<function ... at 0x...>`，
   每次 agent 重建哈希都变。判断「工具是否真变了」应看 **tool_count、工具名、顺序**，不要只看
   `tools_hash`。
3. **时间间隔不能预测逐出**：更长的轮次间隔可能命中率 99%+，更短的间隔反而逐出，不能用
   「隔了多久」下结论。
4. **CLIProxyAPI 的 `main.log` 里 `session-affinity: cache hit` 不是 prompt 缓存**：那是
   session→auth/provider 的路由亲和缓存，与 prompt KV 缓存无关。
5. **大工具结果 ≠ 缓存失效**：它只让「下一次调用的新内容」按 miss 计费，旧前缀仍命中；下一次
   就恢复。判断标准永远是 `cache_read` 绝对值是否下降。

## 验证清单

- [ ] 整体命中率来自 checkpoint 全量消息聚合，不是 `transcript_usage`。
- [ ] 逐出事件用 `cache_read` 绝对值骤降定位，而非仅看百分比。
- [ ] 对每次下探都确认了「增量 miss」还是「全量逐出」。
- [ ] 逐出根因逐项排查过 system / tools / summarization / prompt_saved。
- [ ] 脚本写在 `/.tmp/` 下用 `uv run --no-sync python` 执行，不污染工作区。

## 注意事项

- checkpoint 可能是 4GB+ 的大库，只用 `load_messages_from_sqlite_file` 按 thread_id 定向读取，
  不要全表扫描。
- `tool-outputs.sqlite` 的 `event_json` 是 JSON 文本，按 `thread_id` 走索引查询即可。
- 只做只读分析，不修改 checkpoint / 投影；如需重建投影参考 `session-crash-repair`。
- 不要在任何脚本或 SKILL 内容里写入 API key / `.env` 内容。
