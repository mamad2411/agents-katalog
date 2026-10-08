---
description: >
  Designs tool use (function calling) for Claude API: tool schemas,
  parallel tool execution, error handling, and termination conditions.
  Use when adding tool use to a Claude app or designing an agent loop.
---

## Claude Tool Use

### Tool Definition
- **`name`:** snake_case verb. `get_weather`, `search_orders`.
- **`description`:** What the tool does, when to use it, expected outcome.
  This is the most important field — it drives the model's tool choice.
- **`input_schema`:** JSON Schema. Use `required`, `enum`, `description` per
  property. Strict typing > permissive.
- Keep tool count manageable (≤20 typical). Many tools = poor selection.

### Tool Choice Modes
- `auto` (default): model decides whether to call tools.
- `any`: model MUST call a tool, of its choice.
- `tool` (specific): force a specific tool. Useful for structured output.
- `none`: disable tool use for this call.

### Parallel Tool Use
- Claude can call multiple tools in one response.
- Execute them in parallel (`asyncio.gather`, `Promise.all`) and return all
  results in the next message.
- Each `tool_result` block must reference the matching `tool_use_id`.

### Error Handling
- Tool failures return `tool_result` with `is_error: true` and a clear message.
- DO NOT raise exceptions into the agent loop — the model can't recover from them.
- Include actionable detail: "Database timeout. Retry recommended."
  vs. "Internal error."
- For unrecoverable errors, return a final message and exit the loop.

### Loop Termination
- Max turns (default 10–20). Hard cap to prevent runaway costs.
- Exit when `stop_reason == "end_turn"` and no tool_use block.
- Exit on user-cancellation signal.
- Exit on budget exceeded (token cap per session).

### Interleaved Thinking
- For complex tasks, enable extended thinking with tool use:
  ```python
  thinking={"type": "enabled", "budget_tokens": 10000}
  ```
- The model can reason between tool calls. Higher cost, better outcomes.

### Anti-patterns
- Vague tool descriptions ("does stuff").
- Overlapping tools (`get_user` AND `lookup_user` AND `find_user`).
- Returning huge raw blobs as tool result. Summarize first.
- Letting the loop run forever without a hard cap.
- Forgetting to pass tool definitions on EVERY turn (some SDKs require this).

### Verification
- Eval set covers: simple call, parallel calls, tool error recovery, refusal.
- Trace each loop in observability with `tool_use_id` correlation.
- Track tool selection accuracy (right tool for the task).

### Reference
- See `python-fastapi-genai` skill for end-to-end FastAPI integration.
- See `prompt-caching-claude` for caching tool definitions.

### Model Tier
Default: Sonnet. Escalate to Opus for multi-tool agent design or when
adding new tools to a high-stakes workflow.
