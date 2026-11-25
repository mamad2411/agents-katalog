---
name: acp-protocol
description: Use when integrating ACP, Zed's editor↔agent protocol — JSON-RPC, capability negotiation, fs/terminal, permissions.
metadata:
  added: 2026-05-19
  last_reviewed: 2026-05-19
  type: protocol
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-19"
  related: [mcp-protocol, agent-design]
---

# Agent Client Protocol (ACP) Fundamentals

**Iron Law: ACP is JSON-RPC 2.0 over stdio, but it is NOT MCP. The communication is bidirectional and turn-based: the client (editor) hosts a prompt turn, the agent streams updates via `session/update` notifications, and the agent calls _back into the client_ for filesystem, terminal, and permission. Pin `protocolVersion` at `initialize` and reject mismatches. Tool execution failures are reported inside `session/update` `tool_call` items with a `status: "failed"` and content payload — not as JSON-RPC errors.**

## What ACP is

ACP (Agent Client Protocol) is an open spec from Zed Industries for how a code editor or IDE (the _client_) talks to an LLM agent (the _agent_) so the agent can read files, run terminals, and produce streamed reasoning + tool calls inside the editor's workspace. The agent runs as a separate process and the editor launches it. Reference: `agentclientprotocol.com` and `github.com/zed-industries/agent-client-protocol`.

The mental model: the **client owns the project** (filesystem, terminals, permissions), the **agent owns the reasoning** (LLM calls, tool planning). Communication is JSON-RPC over stdio.

## ACP vs MCP — when to pick which

|                       | ACP                                                                                     | MCP                                     |
| --------------------- | --------------------------------------------------------------------------------------- | --------------------------------------- |
| Direction             | bidirectional; client also has methods                                                  | mostly server-as-callee                 |
| Unit of work          | **prompt turn** (`session/prompt` → stream of `session/update` → terminal `stopReason`) | request/response per tool/resource call |
| Filesystem / terminal | **client provides** via `fs/*` and `terminal/*` methods the agent calls                 | each MCP server exposes its own tools   |
| Permission            | client mediates via `session/request_permission`                                        | host policy outside the protocol        |
| Designed for          | editors/IDEs hosting interactive agents                                                 | model providers consuming context       |

Both use JSON-RPC 2.0 + stdio. **Don't confuse them**: an ACP agent does not "expose tools to the model" — it _uses_ tools by talking back to the client.

## Wire format

Every message is a JSON-RPC 2.0 object — see [[mcp-protocol]] for the envelope shape (same wire format). Methods are namespaced with `/`:

| Direction      | Method                                                                                          | Purpose                                                           |
| -------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| client → agent | `initialize`                                                                                    | handshake, capability exchange                                    |
| client → agent | `authenticate`                                                                                  | (optional) credentials handoff                                    |
| client → agent | `session/new`                                                                                   | start a new prompt session                                        |
| client → agent | `session/load`                                                                                  | resume a prior session (agent must advertise `loadSession: true`) |
| client → agent | `session/prompt`                                                                                | send a user prompt; response carries final `stopReason`           |
| client → agent | `session/cancel`                                                                                | abort the in-flight prompt turn                                   |
| agent → client | `session/update` (notification)                                                                 | stream chunks, tool calls, plans                                  |
| agent → client | `session/request_permission`                                                                    | ask user/policy to allow a tool call                              |
| agent → client | `fs/read_text_file`                                                                             | read a file in the editor's workspace                             |
| agent → client | `fs/write_text_file`                                                                            | write a file in the editor's workspace                            |
| agent → client | `terminal/create` `terminal/output` `terminal/wait_for_exit` `terminal/kill` `terminal/release` | manage editor-side shells                                         |

stdio rule: newline-delimited JSON on stdin/stdout. **NEVER write logs to stdout** — the stream is the protocol. Logs go to stderr.

## Capability negotiation handshake

```jsonc
// client → agent
{ "jsonrpc":"2.0", "id":1, "method":"initialize",
  "params": {
    "protocolVersion": 1,
    "clientCapabilities": {
      "fs": { "readTextFile": true, "writeTextFile": true },
      "terminal": true
    }
  } }

// agent → client (result)
{ "jsonrpc":"2.0", "id":1, "result": {
    "protocolVersion": 1,
    "agentCapabilities": {
      "loadSession": true,
      "promptCapabilities": { "image": true, "audio": false, "embeddedContext": true },
      "mcpCapabilities": { "http": true, "sse": false }
    },
    "authMethods": []
  } }
```

The agent advertises what _it_ can accept (`promptCapabilities`, `loadSession`). The client advertises what _it_ will provide (`fs`, `terminal`). Feature-gate every cross-side call by the negotiated capabilities. **A `protocolVersion` mismatch must abort or downgrade explicitly** — silent drift produces field-not-found errors mid-turn.

## The prompt turn

A turn is the core abstraction:

```
client → session/prompt { sessionId, prompt: [ContentBlock,...] }
agent → session/update   (zero or more notifications: chunks, tool_call, plan, ...)
agent → session/update   (final tool_call with status="completed" or "failed")
agent → result for session/prompt { stopReason: "end_turn" | "max_tokens" | "refusal" | "cancelled" | "max_turn_requests" }
```

`session/update` notifications carry one of: `agent_message_chunk`, `agent_thought_chunk`, `user_message_chunk`, `tool_call`, `tool_call_update`, `plan`, `available_commands_update`. The client renders them progressively. **Long turns MUST honor `session/cancel`** — drop downstream LLM/tool calls and return `stopReason: "cancelled"`.

## Tool calls — the lifecycle

Tools in ACP are agent-declared, not server-registered. The agent emits a `tool_call` update when it intends to run something, optionally calls `session/request_permission`, performs the work (often via `fs/*` or `terminal/*` back to the client), then emits `tool_call_update` with `status: "completed"` and a `content` payload. Failures go in the same update with `status: "failed"`.

```jsonc
// agent → client (notification)
{ "method":"session/update", "params": { "sessionId":"...", "update": {
    "sessionUpdate":"tool_call", "toolCallId":"tc_1",
    "title":"Read README.md", "kind":"read", "status":"pending",
    "locations":[{"path":"/repo/README.md"}]
} } }

// optional: agent → client (request)
{ "method":"session/request_permission", "id":42, "params": { "sessionId":"...",
    "toolCall": { "toolCallId":"tc_1", "title":"Read README.md", "kind":"read" },
    "options":[
      {"optionId":"allow","name":"Allow","kind":"allow_once"},
      {"optionId":"reject","name":"Reject","kind":"reject_once"}
    ] } }
// client result: { "outcome": { "outcome":"selected", "optionId":"allow" } }

// agent → client (notification, terminal)
{ "method":"session/update", "params": { "sessionId":"...", "update": {
    "sessionUpdate":"tool_call_update", "toolCallId":"tc_1",
    "status":"completed",
    "content":[{"type":"content","content":{"type":"text","text":"# Project\n..."}}]
} } }
```

Failures use the same update with `status: "failed"` and an explanatory `content` block. **Do NOT** return a JSON-RPC `error` for tool execution failures — that aborts the prompt turn.

## Content blocks

The shared content type used everywhere a prompt or tool result carries data:

| Type                            | Use                                                                                    |
| ------------------------------- | -------------------------------------------------------------------------------------- |
| `text`                          | plain text chunk                                                                       |
| `image`                         | base64-encoded image (only if `promptCapabilities.image`)                              |
| `audio`                         | base64 audio (only if `promptCapabilities.audio`)                                      |
| `resource_link`                 | URI handoff, no inline data                                                            |
| `resource` (`EmbeddedResource`) | inlined `{ uri, mimeType, text\|blob }` (only if `promptCapabilities.embeddedContext`) |

Gate every block type by `promptCapabilities`. Sending an `image` to an agent that didn't advertise it is a protocol violation.

## Filesystem and terminal (client-side methods)

The agent calls back into the client; the client enforces project scope:

```jsonc
// agent → client
{ "method":"fs/read_text_file", "id":7, "params":{ "sessionId":"...", "path":"/abs/path/x.go" } }
{ "method":"terminal/create", "id":8, "params":{ "sessionId":"...", "command":"go", "args":["test","./..."] } }
```

Client responsibilities: resolve symlinks; verify the resolved path is under an allowed root (see anti-patterns); never honor relative paths blindly; rate-limit terminal spawns; stream stdout/stderr via `terminal/output`. The agent must **release** terminals it owns (`terminal/release`) — leaks pile up processes.

## Anti-patterns

- Returning a JSON-RPC `error` for tool failures — use `tool_call_update` with `status:"failed"` so the agent's loop can recover
- Logging to stdout in an ACP agent process — instant stream corruption
- Calling `fs/*` or `terminal/*` without checking `clientCapabilities` first — the client may not provide them
- Sending `image` / `audio` / `resource` content blocks the agent didn't advertise in `promptCapabilities`
- **Path traversal in `fs/read_text_file`**: resolving `path` lexically (`filepath.Clean` / `path.normalize`) without first resolving symlinks. Always resolve symlinks (`filepath.EvalSymlinks` in Go; `realpath` family elsewhere) THEN check the result is under an allowed root. A `Clean`+`HasPrefix` check alone is bypassed by a symlink under the root pointing outside it.
- Long-running prompt turns without honoring `session/cancel` — every downstream LLM/tool call needs context plumbing
- Leaking terminals — every `terminal/create` needs a paired `terminal/release` on the agent side
- Confusing ACP and MCP capabilities — `agentCapabilities.mcpCapabilities` lets the agent host MCP-style tools internally, but ACP itself isn't MCP

## Red flags

| Thought                                                           | Reality                                                                                      |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| "I'll expose the agent's tools via `tools/list` like MCP"         | Wrong protocol shape — ACP tools are inline in `session/update`                              |
| "I'll fail the prompt with a JSON-RPC error if the tool blows up" | That kills the turn; emit `tool_call_update` `status:"failed"` instead                       |
| "The client always provides terminals"                            | No — gate every `terminal/*` call on `clientCapabilities.terminal`                           |
| "Path is under the project, I can skip the symlink check"         | Symlinks bypass lexical prefix checks; resolve then verify                                   |
| "Cancel can be best-effort"                                       | Per spec, agents MUST honor cancel; drop downstream work and return `stopReason:"cancelled"` |

## Hand-off

For the JSON-RPC envelope, error code semantics, and the MCP comparison side: [[mcp-protocol]]. For agent loop architecture (when to plan, when to act, memory tiers, failure modes that show up _above_ the protocol layer): [[agent-design]]. SDK implementations live in future per-language impl skills (e.g., a `go-acp` mirroring [[go-mcp]]); none authored yet — check `ls skills/` for the live catalogue.
