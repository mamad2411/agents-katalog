---
name: safenode-mcp-gateway
description: Put policy enforcement in front of an agent's MCP tools with the SafeNode MCP Gateway, a proxy that evaluates every tools/call before it reaches the downstream server. Use when the user wants guardrails, approvals, or an audit log on what their agent can do through MCP (file writes, shell, database, payments, GitHub), wants to block or review risky tool calls, or asks how to stop an agent from routing around a safety check. Also use when a tool result says "Blocked by policy", "Held for human review", or starts with "[SafeNode warning]".
---

# SafeNode MCP Gateway

The gateway (`npx safenode-mcp-gateway`, MIT, Node 18+) is an MCP proxy. It sits between the MCP
client and the user's existing MCP servers. `tools/list` passes through unchanged, so the agent sees
the same tools. Every `tools/call` is first sent to the SafeNode API, which returns `allow`, `warn`,
`review` or `deny`. A denied call never reaches the downstream server.

Why a proxy and not an `evaluate_action` tool: a check the model can decide not to call enforces
nothing. Explain this if the user asks why the setup is shaped this way.

This skill covers two jobs: **setting the gateway up**, and **behaving correctly when it blocks
you**.

## Part 1: Setting it up

### 1. Confirm prerequisites

- `node --version` is 18 or newer.
- The user has a SafeNode API key (`sn_...`, free tier at https://safenode.tech). If not, send them
  there to create one. **Do not ask them to paste the key into the chat.** It goes in an
  environment variable or the client's `env` block, which they can fill in themselves.

### 2. Find the user's existing MCP servers

Read the client config that is in use:

| Client | Config file |
| --- | --- |
| Claude Code | `.mcp.json` in the project (or `claude mcp list`) |
| Claude Desktop | `claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` or `.cursor/mcp.json` |
| Other MCP hosts | their `mcpServers` block |

Each entry under `mcpServers` has `command`, `args` and possibly `env`. These become the gateway's
`servers[]`.

### 3. Write `safenode-gateway.json`

Move each server across, keeping its `name`, `command`, `args` and `env`:

```json
{
  "failMode": "fail_closed",
  "payloadMode": "redacted",
  "logFile": "./safenode-decisions.jsonl",
  "servers": [
    {
      "name": "filesystem",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/you/projects"]
    }
  ],
  "tools": {
    "read_file": { "failMode": "fail_open" }
  }
}
```

Rules:

- **Never put the API key in this file.** `SAFENODE_API_KEY` in the environment takes precedence,
  so the file stays safe to commit.
- Keep `failMode: "fail_closed"` (the default) unless the user decides otherwise. If SafeNode is
  unreachable, calls are blocked. Loosen it per tool only for read-only tools such as `read_file`
  or `list_files`.
- Keep `payloadMode: "redacted"` (the default). Use `metadata_only` for tools whose arguments
  should never leave the machine. Use `full` only if the user asks for it.
- `tools.<name>.bypass: true` skips policy entirely for that tool. Only set it when the user asks,
  and say plainly that the tool will then have no check at all.

### 4. Dry run before anything is sent

```bash
SAFENODE_API_KEY=sn_... npx -y safenode-mcp-gateway --config ./safenode-gateway.json --dry-run
```

This prints the exact JSON an evaluation would POST and makes no network call. Show the user the
output so they can see what leaves their machine.

### 5. Replace the client entries with the gateway

**Replace** the old server entries; don't add the gateway alongside them. The gateway spawns
those servers itself, so leaving the old entries in place runs each server twice and gives the agent
an unguarded path to the same tools.

```json
{
  "mcpServers": {
    "safenode": {
      "command": "npx",
      "args": ["-y", "safenode-mcp-gateway", "--config", "/absolute/path/to/safenode-gateway.json"],
      "env": { "SAFENODE_API_KEY": "sn_..." }
    }
  }
}
```

Use an absolute config path for Claude Desktop and Cursor. A relative path works for a project
`.mcp.json` in Claude Code. Back up the original client config before editing it.

### 6. Verify

Restart the client, then confirm the tools still appear and that a harmless call succeeds. If
`logFile` is set, check that a line was written for that call. To see enforcement work, have the
user add a policy in the SafeNode dashboard that denies one tool, then call it.

## Part 2: When a tool call is blocked

These rules apply whenever a tool result comes from the gateway.

| Result text | Meaning | What to do |
| --- | --- | --- |
| Normal result | `allow` | Continue. |
| Starts with `[SafeNode warning]` | `warn`: the call ran | Continue, but tell the user what the warning said. |
| `Held for human review.` | `review`: the call did **not** run | Stop. Tell the user the action needs their approval in the SafeNode dashboard and give the reasons. Retry only after they say it is approved. |
| `Blocked by policy.` | `deny`: the call did **not** run | Stop that action. Report the reasons and the trace id to the user. |

**Do not route around a block.** After a `deny` or `review`, do not:

- retry the same call with arguments reworded or split up to get past the policy;
- reach the same effect through another tool (shell instead of the file tool, raw SQL instead of
  the query tool, and so on);
- ask the user to set `bypass`, change `failMode`, or remove the gateway so the call goes through.

You may suggest a different approach that meets the policy, for example writing inside the approved
workspace instead of outside it. If the user decides to change a policy, they make that change
themselves in the SafeNode dashboard.

If stderr or the log shows `SafeNode unreachable`, the decision came from `failMode` without a
policy check. Report it as an outage, not as a policy verdict.

## What the gateway is not

Say this when it matters to the user's decision. Don't overstate what the gateway does.

- Not a sandbox: once a call is forwarded, the downstream server can do anything it is able to.
  Still give servers the narrowest scope that works.
- Not a prompt-injection detector: it judges the action, not the reasoning behind it.
- Not offline: every gated call makes one round trip to the SafeNode API (5 s budget by default) and
  counts against the account's monthly quota.

## Reference

- Source and full configuration reference: https://github.com/sp3ak/safenode-mcp-gateway
- Docs and API keys: https://safenode.tech/docs
- Config keys: `apiKey`, `baseUrl`, `failMode`, `payloadMode`, `timeoutMs`, `logFile`,
  `prefixTools`, `servers[]`, `tools{}`, `context{}`. `failMode`, `payloadMode` and `context` can
  be set globally, per server or per tool, and the most specific setting wins.
- If two servers export the same tool name, the gateway prefixes every tool as `<server>__<tool>`.
