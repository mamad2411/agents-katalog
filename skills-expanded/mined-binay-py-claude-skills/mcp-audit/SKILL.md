---
name: mcp-audit
description: Audit the MCP servers Claude Code loads and what they cost. Finds every server in ~/.claude.json (user and local scope), project .mcp.json files and installed or claude.ai-synced plugins, counts how often each one was actually called in the session logs, and flags servers you never use, duplicate and redundant copies, missing binaries, archived or test packages, and literal secrets in env, args, urls or headers (key name and type only, never the value). With --measure it starts each server, runs the MCP handshake and sizes its tool list in tokens and its startup time. Use when the user asks which MCP servers they need, why sessions start slowly or servers time out, how much context MCP tools take, or wants to clean up their MCP config.
---

# mcp-audit

`scripts/mcp-audit.mjs` is zero-dependency Node 22+. By default it only reads files and changes nothing.

```
node mcp-audit.mjs                         # inventory + calls per server over the last 30 days
node mcp-audit.mjs --days 90
node mcp-audit.mjs --root ~/code           # also find .mcp.json files under this folder (repeatable, depth 4)
node mcp-audit.mjs --measure               # START the servers and size their tool lists (see below)
node mcp-audit.mjs --measure --only git,memory --timeout 30000
node mcp-audit.mjs --json
```

**`--measure` runs code.** For stdio servers it runs the configured command with its configured env. For http servers it sends JSON-RPC requests to the url. Claude Code does the same at every session start, but ask the user before using it. It skips unapproved or rejected `.mcp.json` servers and disabled plugins unless you name them with `--only`, because a cloned repo's `.mcp.json` should not be trusted until it is approved. Each server is killed (process tree included) after it answers or when `--timeout` runs out (default 10 s).

## Where it looks
- `~/.claude.json`: top-level `mcpServers` (user scope), `projects[path].mcpServers` (local scope), and the per-project `disabledMcpServers`, `enabledMcpjsonServers` and `disabledMcpjsonServers` lists.
- `.mcp.json` in the current folder, in every `--root`, and in every project folder Claude Code has opened (project scope). Approval comes from `~/.claude.json` and the project's `.claude/settings*.json`.
- Plugins: install paths from `~/.claude/plugins/installed_plugins.json` and `~/.claude/plugins/synced/*/<plugin>/` (claude.ai-synced), using `.mcp.json` or `mcpServers` in `.claude-plugin/plugin.json`. Enabled state comes from `enabledPlugins`.
- Usage: every `*.jsonl` under `~/.claude/projects/` (subagent logs included) changed within `--days`. It counts `tool_use` blocks named `mcp__<server>__<tool>`, or `mcp__plugin_<plugin>_<server>__<tool>` for plugin servers. Calls to local and project servers only count when the session ran inside that project.

## Flags
| Flag | Meaning |
|---|---|
| 0 calls | Active, but not called once in the window. It still starts in every session in its scope. |
| `same server as "x": loads twice` | Same command+args or url under a different name. Both start and both tool lists load. |
| `identical to the user-scope "x": redundant` | A local or project copy with the same name. Only one loads (local beats project beats user), so the copy only hides later edits to the user entry. |
| `command not found` | The binary isn't on PATH, or the absolute path doesn't exist. It fails at every startup. |
| `uses unset env var` | A `${VAR}` without a `:-default` that isn't set in this shell. |
| archived / TEST server | `@modelcontextprotocol/server-everything` (the protocol test server) or a reference server moved to servers-archived. |
| `literal secret in env X (type)` | A key pattern, or a long value in a field whose name suggests a secret, in env, headers, args or url. `${VAR}` references are not flagged. |
| `needs auth` (measure) | The http server returned 401/403. OAuth tokens live in Claude Code's credential store, so this can't be measured from outside. |

Servers called in the logs but not in local config are listed separately: claude.ai connectors (`claude_ai_*`), built-ins like `claude-in-chrome`, or servers removed since.

## Acting on the results
- Unused server: turn it off in `/mcp` (keeps the config) or remove it: `claude mcp remove <name> -s user|local|project`. For local scope, run that from the project folder. For a plugin server, use `claude plugin disable <plugin>@<marketplace>` or `/plugin`.
- Used in one project only: remove it from user scope and add it again with `-s local` in that project.
- Redundant local copies: `claude mcp remove <name> -s local` in that project. The user entry keeps working.
- Literal secrets: replace the value with `${ENV_VAR}`. Claude Code expands `${VAR}` and `${VAR:-default}` in command, args, env, url and headers. A key in a committed `.mcp.json` is leaked: rotate it.
- Token cost: with tool search on (the default on current models), only tool names and server instructions load at session start ("upfront" in `--json`), and full definitions load on demand. The full tool-list size is what loads every session when `ENABLE_TOOL_SEARCH=false`, on older models, or behind a gateway that rejects tool search. Startup time matters either way: many npx servers starting together can hit the connect timeout even when each one is fine alone.

## Limits
- Tokens are estimated at ~4 characters per token of the `tools/list` JSON plus server instructions. The real tool-definition encoding differs a little.
- Legacy SSE transport (`"type": "sse"`) and WebSocket servers are listed but not measured. Servers that need OAuth show "needs auth".
- Calls can't be split between same-named entries in different scopes, so a user entry's count includes calls made while a local copy was active.
- It doesn't read managed MCP config (`managed-mcp.json`), `--mcp-config` files or Agent SDK servers. It can't list claude.ai connectors you never called.
- Plugin enabled state comes from user settings and the project settings of local-scope installs. Synced claude.ai plugins show their sync preference, not a definite on/off.
