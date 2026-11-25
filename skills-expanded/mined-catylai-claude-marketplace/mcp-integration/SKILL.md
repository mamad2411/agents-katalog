---
name: mcp-integration
description: "Wires MCP servers into Claude Code and the Agent SDK. Use when adding, scoping, securing, or debugging an MCP server, or when a hook or allow rule on an MCP tool never fires. Covers config scope, secrets, exact tool names for rules and hooks, resources, and in-process versus subprocess hosting. Not for writing tool descriptions or schemas (use tool-interface-design); not for building a server from scratch (use mcp-builder); not for permission precedence (use deterministic-enforcement)."
when_to_use: "add an MCP server, .mcp.json, MCP hook not firing, MCP allow rule ignored, MCP secret in config, project vs user scope"
license: MIT
---

# MCP integration

MCP is a way to distribute tools, and an MCP tool needs the same design care as any other tool.
That design work belongs to tool-interface-design. This skill covers the wiring: where the config
lives, how secrets get in, what names the tools end up with, and the mistakes specific to the
protocol.

Work in this order of preference:

1. Evaluate an existing server before writing one.
2. Expose data as a resource before writing a tool that fetches it.
3. Improve a tool's description before adding another tool.

## 1. Put each server in the scope that matches its audience

| Scope | Where it is stored | Who gets it |
| --- | --- | --- |
| `local` (the default) | `~/.claude.json`, under that project | You, in this project only |
| `project` | **`.mcp.json`** at the repo root, committed | The whole team |
| `user` | `~/.claude.json` | You, in every project |

- Team servers go in `.mcp.json`. Personal and experimental servers stay out of it.
- `claude mcp add --scope <scope>` writes to the correct file for you.
- `settings.json` has no key for defining servers. It only has keys that govern them:
  `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `allowedMcpServers`, `deniedMcpServers`,
  and the managed-only restriction keys.

If the same server name appears in more than one place, one entry wins: local beats project, which
beats user, then plugin-provided servers, then claude.ai connectors, and managed MCP ranks above all
of them. The winning entry is used whole and nothing is merged across sources, so you cannot
partially override a server. Either copy the full entry or don't define it twice.

## 2. Reference secrets instead of embedding them

In `.mcp.json`, `${VAR}` and `${VAR:-default}` are expanded in `command`, `args`, `env`, `url` and
`headers`. This lets the config be committed safely while each developer supplies their own
credential.

- **An unset variable with no default does not stop the server.** The server still loads, with the
  literal `${VAR}` text in place, and then fails in confusing ways. `claude mcp list` and `/mcp`
  both show a missing-variable warning, so check one of them after onboarding.
- **Some variables are always read as empty in a remote server's `url` and `headers`.** Claude
  Code's own credentials, such as `ANTHROPIC_API_KEY`, and some cloud and registry tokens are
  blanked there, so that a project cannot send them to a remote server. Pass the server's token
  under a name of its own.
- **In a plugin, declare secrets in `userConfig` with `sensitive: true`.** Claude Code prompts the
  user when the plugin is enabled, keeps the value in secure storage (the macOS Keychain, otherwise
  `~/.claude/.credentials.json`) rather than `settings.json`, and substitutes it as
  `${user_config.KEY}` in the plugin's MCP config.

A token hardcoded in a committed `.mcp.json` stays in git history even after you remove it.

## 3. Pick the transport

- **stdio**: a local process. `claude mcp add <name> -- <command> [args...]`.
- **`http`**: recommended for remote servers. `streamable-http` is accepted as an alias.
- **`ws`**: WebSocket. Configure it with `claude mcp add-json`, and authenticate with headers only.
- **`sse`**: deprecated. Move to `http` where the server supports it.

An entry that has a `url` but no `type` is read as stdio and skipped. Always set `type` on remote
entries.

Per-server fields you may need are `timeout`, `headers`, `headersHelper` (which generates headers
at connect time), `oauth` and `alwaysLoad`.

## 4. Expose catalogs as resources, not as discovery calls

Claude Code attaches MCP **resources** referenced as `@server:protocol://path`. Use resources for
anything shaped like a catalog, such as issue boards, schemas and document trees, so the agent
doesn't spend tool calls finding out what exists.

Other MCP features:

- Prompts become commands, run as `/server:prompt` or `/mcp__server__prompt`.
- Elicitation (form and URL dialogs) is supported.
- Sampling is not documented as supported, so do not design a server that needs it.

Two per-tool `_meta` flags are worth knowing:

- `anthropic/requiresUserInteraction: true` prompts on every call.
- `anthropic/alwaysLoad: true` keeps the tool out of tool-search deferral.

For tools that return large results, the output limit is the `MAX_MCP_OUTPUT_TOKENS` environment
variable. A tool can raise its own limit with `_meta["anthropic/maxResultSizeChars"]`. Trim what a
tool returns before raising either limit.

## 5. Host in-process when your application owns the tools

The Agent SDK can host an MCP server inside your process (`createSdkMcpServer` with `tool(...)`
in TypeScript; see [references/in-process-server.md](references/in-process-server.md)).

- **Choose in-process** when the tools are part of your application. There is no subprocess, no
  serialization hop and no separate lifecycle to manage.
- **Choose a subprocess or remote server** when the tools must be reused across clients, deployed
  or scaled on their own, written in another language, or isolated for security.

## 6. Write the exact tool name in every rule and matcher

| Where the server comes from | Tool name Claude sees |
| --- | --- |
| A regular server | `mcp__<server>__<tool>` |
| A plugin-bundled server | `mcp__plugin_<plugin>_<server>__<tool>`, with any character outside `A-Za-z0-9_-` replaced by `_` |

Use that full name in permission rules, `allowed-tools`, a subagent's `tools` list, and hook
matchers. **A matcher on the bare server key never fires**, and a hook that doesn't fire looks
exactly like a hook that allowed the call. Copy the name from a transcript rather than
reconstructing it.

- Allow rules accept a glob only after a literal `mcp__<server>__` prefix, for example
  `mcp__issues__get_*`.
- Deny and ask rules also accept `mcp__*` and similar wider forms.
- A hook matcher becomes a regex as soon as it contains a regex character, so
  `mcp__memory__.*` matches every tool from that server.
- The `server` field of an `mcp_tool` hook takes the registration name, `plugin:<plugin>:<server>`,
  not the `mcp__…` tool name.

For which rule wins when several match, see deterministic-enforcement.

## 7. Tool quality is tool-interface-design's job

When the model reaches for Grep instead of your semantic-search tool, the tool's description is
the bug. How to write descriptions, error results (`isError`), structured content and annotations
all live in tool-interface-design.

## Examples

<example>
A team server in `.mcp.json` with secrets passed by reference:

```json
{
  "mcpServers": {
    "issues": {
      "command": "npx",
      "args": ["-y", "@example/mcp-server-issues"],
      "env": { "ISSUES_TOKEN": "${ISSUES_TOKEN}" }
    },
    "code-search": {
      "type": "http",
      "url": "${SEARCH_MCP_URL:-https://search.example.com/mcp}",
      "headers": { "Authorization": "Bearer ${SEARCH_MCP_TOKEN}" }
    }
  }
}
```

Committed to the repo, so a new hire gets both servers on clone and no credential enters git. The
remote entry sets `type` explicitly.
</example>

<example>
A plugin-bundled server that gets its secret from `userConfig`:

```jsonc
// .claude-plugin/plugin.json (excerpt)
"userConfig": {
  "ledger_token": { "type": "string", "title": "Ledger API token",
                    "description": "Token for the ledger API", "sensitive": true, "required": true }
}
// .mcp.json at the plugin root
{ "mcpServers": { "ledger": {
  "command": "python",
  "args": ["${CLAUDE_PLUGIN_ROOT}/servers/ledger.py"],
  "env": { "LEDGER_TOKEN": "${user_config.ledger_token}" } } } }
```

The user is asked for the token once, and it is stored in secure storage (the macOS Keychain,
otherwise `~/.claude/.credentials.json`), not in `settings.json`.
</example>

<example>
Rules and matchers written against the real tool names:

```json
{
  "permissions": {
    "allow": ["mcp__issues__get_*", "mcp__plugin_directory_people__people_get_reporting_chain"],
    "deny":  ["mcp__issues__delete_*"]
  },
  "hooks": { "PreToolUse": [{
    "matcher": "mcp__plugin_billing_billing__charge_card",
    "hooks": [{ "type": "command", "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/spend-gate.sh" }]
  }] }
}
```

Each of these fails: the matcher `"billing"`, which never fires; the allow rule `"mcp__*__get_*"`,
which is skipped with a warning; and `"billing__charge_card"`, which has no `mcp__` prefix.
</example>

## Failure modes

- **A partial override.** The winning entry is used whole, so every field you didn't restate is
  lost.
- **A personal server in the shared file.** A binary path under one developer's home directory
  breaks every teammate's session.
- **Discovery by tool call.** Listing 40 projects, then 40 issue lists, then 30 issues is 71 round
  trips spent on a catalog that could have been a resource.
- **Forking a community server to improve its descriptions.** Improve them at your own gateway, or
  wrap only the tools you use. A fork falls behind upstream and has no owner.

Porting notes for other MCP clients are in [references/porting.md](references/porting.md).

## Verify

1. Run `claude mcp list` (or `/mcp` in a session). Every server shows as connected, and none shows
   a missing-variable warning.
2. Run `git log -p -- .mcp.json` and search it for token-shaped strings. Removing a secret now does
   not remove it from history.
3. Trigger one call to each gated MCP tool and confirm that the hook fires and the allow rule
   applies. If the hook stays silent, compare the matcher with the tool name shown in the
   transcript.

Without a checkout: work from the `.mcp.json`, settings and transcript excerpts the user pastes,
and list which of these checks the user still needs to run.
