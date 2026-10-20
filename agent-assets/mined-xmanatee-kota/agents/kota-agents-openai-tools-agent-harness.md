# OpenAI Tools Agent Harness Module

Adapter module that registers the `openai-tools` harness: a multi-turn
tool-calling loop driven by any OpenAI-compatible `ModelClient`. It also
registers the opt-in `openai-tools-scaffold` harness for weaker or local
models that need a smaller compound-tool action space. Select either with a
preset, default harness config, or a per-step `harness`.

This module owns the `KotaTool` to OpenAI-tools native-loop translation at the
adapter seam. Tool execution routes through the shared KOTA tool runner so
guardrails, approvals, idempotency, effect-aware scheduling, MCP dispatch, and
secret masking stay aligned with the classic loop.

## Supported Providers

Provider coverage comes from `model-clients`. Any resolved client whose
`messages.stream` implementation returns `tool_use` blocks works here:
`openai`, `ollama`, `groq`, `together`, `lmstudio`, and explicit compatible
`--base-url` endpoints.

## Loop Shape

Each turn sends the full `KotaMessage[]` transcript plus the filtered tool list
through `ModelClient.messages.stream`, forwards streamed text, validates tool
calls, executes them through guarded core tool paths, appends `tool_result`
messages, and repeats until no tool calls remain or the max turn limit fires.
The scaffold harness exposes only compound inspect/search-read/edit/patch/run/
verify tools and expands each call back into the shared KOTA tool runner; the
normal harness continues to expose the filtered raw tool catalog unchanged.

Guardrails are applied inside the shared runner. Filtered tools are hidden and
denied if called; `canUseTool` can update inputs, return a denial tool result,
or interrupt the run. Non-empty `mcpServers` are hosted by a KOTA-owned
`McpManager` for stdio/http transports; unsupported transports fail at the
adapter boundary. Scope-local `.kota/mcp.json` discovery is skipped before
manager initialization when `mcpProjectConfigPolicy` is `"disabled"`; this
does not suppress caller-provided server declarations, which remain explicit.

The adapter additionally rejects a bare `claude_code` preset `systemPrompt`
without an `append` body because that shape is Claude-specific. Portable
`append` text is accepted for operator CLI paths.

Persisted native-loop sessions use the shared core conversation store. Resume
decodes metadata, tool declarations, and every neutral transcript message
before model dispatch; malformed or unsupported records fail explicitly.
Writes atomically replace the session file. A preservation-enabled run creates
its KOTA-owned session id before the first model turn and checkpoints only
complete transcript boundaries, so workflow continuation never treats a
provider message id as a resumable session.

## Reasoning Effort

`AgentHarnessRunOptions.effort` is forwarded to `ModelClient.messages.stream`.
Provider-specific translation lives in `model-clients/reasoning.ts`. The validated
adapter option `reasoning: "provider-default"` explicitly omits portable effort
from requests, allowing providers without an effort translator to run. Other
adapter options reject. Matrix artifacts report this posture without claiming
a portable effort level.

## Protocol Errors

Malformed `tool_use` blocks, missing names, and non-object inputs throw before
reaching tool runners. Coercion belongs at the wire boundary only.
