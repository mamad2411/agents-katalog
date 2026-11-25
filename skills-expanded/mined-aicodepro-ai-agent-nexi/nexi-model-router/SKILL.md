---
description: "How Nexi picks models and routes intents. Use when debugging misrouting, wrong-model bugs, or a stuck ReAct/tool loop."
license: "MIT"
---
# Nexi Model Router

Two separate routing concerns: **which model** runs a task, and **which
intent/tool** a user utterance maps to.

## Model selection — `engine/model_registry.py`

- `MODELS` is a capability lookup table (tools/multiturn_tools/json_object/
  vision/reasoning/speed) built from **measured** Groq API behavior, not
  vendor claims.
- `select_model(task)`: env override wins first; otherwise picks the
  highest-ranked model whose capabilities satisfy the task AND whose
  provider's API key is actually set (`endpoint_for(model)["api_key"]`) — so
  Nexi never auto-picks a model it can't call.
- `which_model(slots)` / `why(task)` expose the live decision + rejection
  reasons — use these first when debugging "wrong model got used" instead of
  grepping env vars.
- **Never hardcode a model name as a fix.** If a caller needs a specific
  model, add/adjust its capability row in `MODELS`, or set the task's env
  override — don't inline a literal model string.

### Known Groq quirks baked into the registry

- `gpt-oss-20b` / `gpt-oss-120b` reject `response_format=json_object` (HTTP
  400) → `GROQ_INTENT_MODEL` must resolve to a model with `json_object: True`
  (e.g. scout).
- `gpt-oss` leaks harmony `<|channel|>` tokens into tool names on the 2nd+
  turn of a tool loop → `multiturn_tools: False`, so `REACT_MODEL` must be a
  model with `multiturn_tools: True` (e.g. llama-3.3-70b).
- `llama-3.3-70b` returns `arguments:"null"` for zero-arg tools —
  `engine/providers/openai_compat.py` coerces `null` args to `{}`.

## Intent routing — `engine/groq_intent_router_v2.py`

Tiered pipeline: semantic/embedding match → small model → large model, with a
compound-request branch that hands off to `engine/react_planner.py` for
multi-step tool use. Legacy keyword routing is the final fallback.

- The embedder is e5 (sentence-transformers), not a hashing embedder — don't
  assume hashing when debugging semantic-match misses.
- **The 3-list tool trap**: a tool must be registered in `_TOOLS`,
  `ALLOWED_INTENTS`, and `TOOL_INTENTS` in `engine/tool_registry.py`. Missing
  any one causes a SILENT failure — the utterance routes to chat or gets
  scrubbed to `unknown`, never an exception. `tests/test_tool_intent_consistency.py`
  guards this; run it after touching any of the three lists.
- 429 from Groq fails fast (no retry storm) by design — don't "fix" that into
  a retry loop.
