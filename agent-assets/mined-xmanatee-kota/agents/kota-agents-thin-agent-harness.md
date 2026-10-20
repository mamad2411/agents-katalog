# Thin Agent Harness Module

Adapter module that registers the `thin` harness — a single-turn text
completion loop that uses the core ModelClient registry.

- The harness is deliberately minimal: one request, no tool loop, no MCP.
  Operators can select it when they want a claude-agent-sdk-free path against
  any provider the model-clients module ships (Anthropic, OpenAI, Ollama,
  Groq, Together, LM Studio, etc.).
- The thin harness runs no tool loop, so there is no `KotaTool` translation
  seam in this module (see `src/core/agent-harness/AGENTS.md`).
- Guardrail options (canUseTool, mcpServers, allowedTools, disallowedTools),
  per-step `harnessOverrides`,
  per-run subprocess env, `onMessage` subscriptions, and
  `autonomyMode === "supervised"` are rejected at the boundary. The harness
  has no tool surface to guard, no message stream to emit, and no
  approval-queue routing, so silently ignoring those options would violate
  the protocol's "fail loudly on unsupported" contract.
- Requires the `model-clients` module for `createModelClient` to resolve.
- System prompt must be a plain string. The Claude Agent SDK preset form is
  not portable.
- Declared capabilities: `askOwnerToolName = null` (no tool loop means the
  owner-questions surface cannot be hosted; `runAgentHarness` throws if a
  caller sets `askOwner` against this adapter) and
  `emitsAgentMessageStream = false`.

Conversation history uses core reconstruction across invocations, including
interrupted calls. Provider response ids are not exposed as resumable sessions.
