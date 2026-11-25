---
name: cnllm-skill
description: |
  A Python library for OpenAI-compatible Chinese LLM APIs. Use this when users need per-request batch configuration, automated streaming accumulation, streaming structural overview, vendor-native parameter validation with feedback, memory control, configurable failure policy, and batch task progress tracking. Replaces OpenAI SDK/LiteLLM for multi-model workflows.
license: Complete terms in LICENSE.txt
---

# CNLLM: Chinese LLM Unified Adapter

## When to Use This Skill

- **Multi‑model workflows** – call different Chinese LLMs (DeepSeek, GLM, Qwen, etc.) in multi-model workflows.
- **Per‑request batch** – configure distinct parameters (`model`, `thinking`, `tools`, `stream`) for each request in a batch.
- **Automated streaming accumulation** – real‑time access to `reasoning_content`, `content`, `tool_calls` via properties (`think`/`.still`/`.tools`).
- **Streaming structural overview** – inspect streaming process via a structured view (`.repr`).
- **Parameter validation** – explicit feedback on unsupported parameters with configurable handling (`drop_params`).
- **Memory control** – manage memory usage with `keep`.
- **Batch progress tracking** – monitor batch task progress via `.status`.

## Vendor Support

DeepSeek, GLM (Zhipu), KIMI (Moonshot), MiniMax, Doubao (ByteDance), Xiaomi mimo, Qwen (Alibaba), Ernie (Baidu), Hunyuan (Tencent), Step (阶跃星辰). 
(Model list see `docs/model_list.md`)

## Installation & Version

```bash
pip install cnllm
```

For latest features, ensure version >=0.9.10.

## Basic Principles

### 1. Initialize the client 
```python
client = CNLLM(model="deepseek-chat", api_key=os.getenv("DEEPSEEK_KEY")) # use default base_url - vendor's OpenAI-compatible url
resp = client.chat.create(prompt="Hello, world!", model="deepseek-v4-pro")
```
Note: Initialize the client before invocation. Parameters at call will override the same parameters set at client.

### 2. Unified Parameters
Use **OpenAI standard parameters**, configure vendor-native ones if needed, which will be passed as-is if supported (do not need `extra_body` ). 

### 3. HTTP Control Parameters
| Parameter         | Type    | Default    | Description          |
| ----------------- | ------- | ---------- | -------------------- |
| `timeout`         | `int`   | `60`       | Request timeout  |
| `max_retries`     | `int`   | `3`        | Maximum retry count  |
| `retry_delay`     | `float` | `1.0`      | Retry delay    |
| `max_concurrent`  | `int`   | `3`(chat)/`12`(embeddings) | Maximum concurrent requests, batch only |
| `rps`             | `int`   | `2`(chat)/`10`(embeddings) | Maximum requests per second, batch only |
| `performance`     | `bool`  | `False`  | Pooled distribution: weighted by model throughput, requires `fallback_models` |

## Chat Examples

### 1. Single Chat with Streaming Incremental Access and Live View

```python
import os
from cnllm import CNLLM, ToolCollector

client = CNLLM(model="deepseek-chat", api_key=os.getenv("DEEPSEEK_KEY"))
resp = client.chat.create(messages=[{"role": "user", "content": "Hello"}],
                          stream=True, thinking=True, tools=[...])

# ── Streaming: iterate ALL chunks to consume the stream ──
#    chunk.* returns per-frame delta (mandatory)
#    with resp as view: terminal live dict (optional)
frontend_content = []
frontend_reasoning = []
frontend_tools = ToolCollector()   # auto-merge tool_calls by index

with resp as view:
    for chunk in resp:
        frontend_content.append(chunk.still)
        frontend_reasoning.append(chunk.think)
        frontend_tools.update(chunk.tools)  # List[Dict] per-frame delta
        view.refresh()

# ── After stream: resp.* returns fully accumulated results ──
print(resp.still)  # fully accumulated content
print(resp.think)  # fully accumulated reasoning
print(resp.tools)  # List[Dict], OpenAI standard format, no index
print(resp)        # final merged dict

# ── Build next-turn conversation context ──
from cnllm import ContextBox

messages += ContextBox(resp.still, resp.think, resp.tools,
                       executor=execute_tool)  # define your own tool executor function
# → assistant message + tool_calls attached + tool results appended
```

### 2. Streaming Batch with Per‑Request Incremental Access and Live View
```python
resp = client.chat.batch(
    prompt=["Weather in Beijing", "Weather in Shanghai"],
    stream=True,
)

with resp as view:              # terminal live view: {status + usage}
    for chunk in resp:
        rid = chunk["request_id"]
        frontend[rid].append(chunk.still)  # route delta to per-request panel
        view.refresh()

print(resp.still)  # {"request_0": "...", "request_1": "..."}
print(resp.tools)  # {"request_0": [{tool_call}], "request_1": []}  List[Dict] per request
```

### 3. Mixed Batch (stream + non-stream) with Live View
```python
resp = client.chat.batch(requests=[
    {"prompt": "Weather", "stream": True, "tools": [weather_tool]},
    {"prompt": "1+1=?"},
    {"prompt": "Hello", "stream": True},
])

with resp as view:
    for chunk in resp:
        frontend[chunk["request_id"]].append(chunk.still)
        view.refresh()

print(resp.still)  # content of all requests
```
Note: Streaming and mixed batch **must be iterated** to trigger request processing, `resp.still`/`resp.think`/`resp.tools` complete after iteration.

### 5. Non-Streaming Batch with Adaptive Scheduling

Non-streaming batch (`chat.batch(stream=False)`) uses an adaptive scheduler by default — dynamic concurrency, RPS limiting, RPM learning, and 429 freeze/thaw. Pass `max_concurrent`/`rps` explicitly to override with fixed values. With `fallback_models` + `performance=True`, requests distribute by model throughput; `max_concurrent`/`rps` cannot be set when `performance=True`.

### 4. Parameter Validation (`drop_params`) and Memory Control (`keep`)
```python
resp = client.chat.batch(
    prompt=["A","B"],
    drop_params="strict",
    keep=["results"],
)
```
Note: 
- set `drop_params="strict"` to reject unknown parameter (request fail and continue batch), or use `warn` to warn and continue request, or `ignore` to silently drop.

**`keep` defaults** ：
| Call Scenario               | Default keep                    | Release       |
| --------------------------- | ----------------------- | -------------------- |
| `client.chat.batch()`       | `still/think/tools/status/usage` | `results/errors/raw` |
| `client.embeddings.batch()` | `vectors/status/usage/batch_info` | `results/errors`     |

During iteration, all fields are available, independent of `keep`.

## Batch Response Structure

**chat.batch():**
```
{
    "status": {"elapsed": "3.42s", "success_count": 2, "fail_count": 1, "total": 3},  # Statistics
    "usage": {"prompt_tokens": 5, "total_tokens": 5},     # Batch processing total usage info
    "errors": {"request_2": "error message"},             # Mapping of all failed requests' request_id to error messages
    "results": {"request_0": {...}, "request_1": {...}},  # Mapping of all successful requests' request_id to standard responses
    "think": {"request_0": "...", "request_1": "..."},
    "still": {"request_0": "...", "request_1": "..."},
    "tools": {"request_0": [{tool_call}], "request_1": [{tool_call}]},  # List[Dict] per request
    "raw": {"request_0": {...}, "request_1": {...}}
}
```

**embeddings.batch():**
```
{   
    "status": {"elapsed": "3.35s", "success_count": 1, "fail_count": 1, "total": 2},
    "batch_info": {"batch_size": 2, "batch_count": 2, "dimension": 1024},
    "usage": {"prompt_tokens": 5, "total_tokens": 5},
    "results": {"request_0": {...}, "request_1": {...}}
    "errors": {"request_2": "error message"},
    "vectors": {"request_0": [...], "request_1": [...]}    # Mapping of all successful requests' request_id to embedding vectors
}
```

## Highlights

| Feature | Description | Import |
|---------|-------------|--------|
| `chunk.still` / `chunk.think` / `chunk.tools` | Per-frame delta during streaming | Built-in on `StreamChunk` |
| `ToolCollector` | Auto-merge tool_calls by index | `from cnllm import ToolCollector` |
| `ContextBox` | Build conversation context from `resp.*` | `from cnllm import ContextBox` |
| `with resp as view:` | Terminal live dict during streaming | Built-in on all responses |

## Examples (See `examples/` directory)

- `streaming_incremental.py` – single streaming with `chunk.*` + `resp as view`
- `batch_streaming.py` – batch streaming with `request_id` routing
- `mixed_batch.py` – mixed (stream+non-stream) batch
- `embeddings.py` – single/batch embedding requests
- `fallback.py` – `fallback_models` with detailed error handling
- `async_client.py` – async client usage with `asyncCNLLM`
- `langchain_integration.py` – LangChain Runnable integration
- `batch_customization.py` – `custom_ids` and `callbacks`
- `tool_chain.py` – multi-turn tool calling with `ContextBox`

## References (See `references/` directory)

model_list.md - supported models
common_mistakes.md - common mistakes