---
name: jbctl
description: |
  Connects to JetBrains IDE (WebStorm, IntelliJ IDEA, GoLand, PyCharm) via MCP
  protocol and exposes 41+ built-in tools as CLI commands. Handles code analysis,
  project-aware search, refactoring, file operations, database queries, and terminal
  execution. Use when the user needs IDE inspections, symbol lookup, rename refactoring,
  database access, or any operation that benefits from IDE-level project understanding.
compatibility: Requires Bun (preferred) or Node.js. Target IDE must have MCP Server plugin enabled.
metadata:
  author: OrdinarySF
  version: "0.2.3"
allowed-tools:
   - Bash
   - AskUserQuestion
---

# jbctl — JetBrains IDE Control

## Hard rules

- MUST run `jbctl inspect <tool>` before calling any tool for the first time — schema changes across IDE versions.
- NEVER include `projectPath` in `--json` — it is auto-injected from `--project`.
- NEVER guess parameter names or values. If `inspect` output is ambiguous, ask the user for clarification.
- NEVER run destructive database operations (DROP, DELETE, TRUNCATE, ALTER) without explicit user confirmation first.
- When `discover` returns `braveMode: false`, warn the user: execution tools (terminal, file write, refactoring) will pop a confirmation dialog in the IDE that blocks until clicked.

## Bootstrap (ALWAYS first)

Run `jbctl tools --json` to list available tools and verify the connection in one step:

```bash
jbctl tools --json
```

If the command fails, check the error:

1. **`command not found`** → CLI not installed. Install globally and retry:
   ```bash
   bun i -g jbctl && jbctl tools --json
   ```
   If `bun` is unavailable, use `npm i -g jbctl`.

2. **Connection error / no tools returned** → Current project not matched to any IDE. Run discovery:
   ```bash
   jbctl discover --json
   ```
   - If **multiple instances** found: use `AskUserQuestion` to show the list and ask the user which IDE to use. Then retry with `-e <endpoint>`.
   - If **one instance** found but project mismatch (e.g. working in a git worktree): ask the user for the IDE's project path, then retry with `-p <project_path>`.
   - If **no instances** found: IDE not running or MCP Server plugin not enabled. Ask the user to check **Settings → Tools → MCP Server → ☑ Enable MCP Server**.

Check the tool count to determine capabilities:
- **40+ tools** → Full capabilities including database MCP tools
- **< 30 tools** → Older IDE version, database requires fallback (see [references/database.md](references/database.md))

## Usage

### Inspect tool schema before calling

```bash
jbctl inspect <tool_name>
```

### Call a tool

```bash
jbctl call <tool_name> --json '{"param":"value"}' --output json
```

Both `--project` and `--endpoint` are auto-detected — you almost never need to specify them manually. Use `jbctl discover` to list all running IDE instances if auto-detection fails.

## Database access

Two paths depending on IDE version. See [references/database.md](references/database.md).

- `doctor` shows 40+ tools → Use MCP DB tools directly (`execute_sql_query`)
- `doctor` shows < 30 tools → Use fallback: read `.idea/dataSources.xml` + direct JDBC

## Gotchas

- Different IDE products/versions expose different tool counts — always check via `doctor` first.
- `--output json` prefers `structuredContent` when available; not all tools return it.
- Auto-detection can fail when multiple IDEs have the same project open — use `jbctl discover` then pass `-e` explicitly.
- Some tool names differ between IDE products (e.g. WebStorm vs IntelliJ). Always use `jbctl tools` to get the actual list.
