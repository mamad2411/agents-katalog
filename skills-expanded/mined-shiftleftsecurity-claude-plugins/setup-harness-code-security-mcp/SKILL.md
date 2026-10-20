---
name: setup-harness-code-security-mcp
description: Install and verify the harness-code-security-mcp npm MCP server. Use when sl_* MCP tools are missing, setup is requested, or Qwiet auth needs diagnosis. After first-time MCP config, tell the user to restart the agent host before calling sl_* tools.
argument-hint: "[--install] [--package harness-code-security-mcp] [--version latest]"
---

# Set up Harness Code Security MCP

Install and connect the **`harness-code-security-mcp`** npm package (`sl_whoami`, `sl_analyze`, triage, AutoFix).

## Doctor

```bash
node scripts/doctor.mjs
```

Install the npm launcher if missing:

```bash
node scripts/doctor.mjs --install
```

## Prerequisites

1. Node.js 20+
2. `sl auth` → `~/.shiftleft/config.json` with `orgId` and `accessToken`
3. MCP server **`harness-code-security-mcp`** configured in the agent

## Claude Code

Terminal or Bash inside a session:

```bash
claude mcp add harness-code-security-mcp -- npx -y harness-code-security-mcp
```

If `--` parsing fails, use JSON:

```bash
claude mcp add-json harness-code-security-mcp '{"type":"stdio","command":"npx","args":["-y","harness-code-security-mcp"]}'
```

**Windows:** `claude mcp add harness-code-security-mcp -- cmd /c npx -y harness-code-security-mcp`

## Cursor and other agents

```json
{
  "mcpServers": {
    "harness-code-security-mcp": {
      "command": "harness-code-security-mcp"
    }
  }
}
```

Use `npx -y harness-code-security-mcp` instead of a global install if preferred. No `env` block required (defaults: `app.shiftleft.io`, `~/.shiftleft`).

## Devin

### Devin CLI

After adding **`release/curness-devin-plugin`** to **`plugin_dirs`** in `~/.config/devin/config.json`, merge hooks once, then start a **new** `devin` session:

```bash
node "/path/to/curness-devin-plugin/handlers/install-harness-sast-devin-hooks.js"
```

(`/update-harness-sast-dependencies` or `handlers/update-handler.js` also merges hooks and installs analysis dependencies.)

If hooks still do not fire, confirm the path in `plugin_dirs` is absolute and points at a built **`release/curness-devin-plugin/`** directory (run `make build && make devin-plugin-dist`), then start a **new** `devin` session.

### Devin Desktop (Devin Local)

With the Curness VSIX and **Devin Local** selected, MCP can be configured in **`~/.config/devin/config.json`** (same as CLI). Bundled MCP comes from **`plugin_dirs`** if **`release/curness-devin-plugin`** is listed there. **Cascade** (default agent) does not use this config file for hooks.

## Restart the agent host (required after MCP config)

MCP servers are loaded when the **agent host starts**. Adding or changing `harness-code-security-mcp` config does **not** reliably attach tools to the **current** running session.

**Agent behavior:** After installing the launcher and writing MCP config, **stop**. Tell the user to restart the host, then verify in a **new** session. Do **not** call `sl_*` tools in this same turn expecting them to work.

| Host | What to do |
|------|------------|
| **Cursor** | Quit and reopen Cursor, or **Developer: Reload Window** |
| **Claude Code** | Fully exit and restart Claude Code (new chat alone is usually **not** enough) |
| **Cursor CLI (`agent`)** | Stop and rerun `agent` after MCP config changes |
| **Devin CLI** | Start a **new** `devin` session after changing **`plugin_dirs`** or MCP config |
| **Devin Desktop** (**Devin Local**) | Restart Devin Desktop or reload the window after MCP config changes; select **Devin Local** (not **Cascade**) |
| **Harness SAST and SCA plugin** | Restart the host after `mcp.json` or MCP settings change |

## Verify (after restart)

In the **new** session: run `/mcp` (Claude Code) or open the MCP tool list (Cursor). Confirm tools such as `sl_whoami` are present (hosts may prefix names, e.g. `mcp__harness-code-security-mcp__sl_whoami`).

Then call `sl_whoami`. Success → `activeOrganizationId` matches config `orgId`.
