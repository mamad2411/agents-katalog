---
name: opencode-tools
license: CC-BY-4.0
compatibility: >-
  OpenCode custom tools (`tool()` from @opencode-ai/plugin) and the opencode.json
  `mcp`, `lsp`, and `permission` keys; checked against v1.18.33 docs and source on
  2026-09-29. Package versions: opencode-sdk.
description: >-
  Add capabilities to OpenCode: standalone custom tools in `.opencode/tools/*.ts`,
  MCP servers (`mcp` key), and LSP servers (`lsp` key). Use for overriding a
  built-in tool, `environment` vs `env` spellings, namespaced MCP tools and their
  gating, `lsp` true/false/object, or `apply_patch`/`patchText`. Tools registered
  from plugin code → opencode-dev:plugin; permission rules → opencode-dev:policies.
argument-hint: "e.g. 'add a custom .opencode tool that overrides bash' or 'wire a remote MCP server'"
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# OpenCode: extending tools (custom tools, MCP, LSP)

OpenCode's API moves fast and predates the model's training cutoff — before
writing tools code, read `references/custom-tools.rst`, `references/mcp-servers.rst`,
`references/lsp.rst`, `references/tools.rst` AND re-check
https://opencode.ai/docs/custom-tools/ (and the `/mcp-servers/`, `/lsp/`, `/tools/`
pages) for drift.

**Three distinct extension mechanisms — pick one:**

| Want | Mechanism | Where | Surface |
|---|---|---|---|
| Your own callable function | **Custom tool** | file `.opencode/tools/<name>.ts` | `tool()` from `@opencode-ai/plugin` |
| An external MCP toolset | **MCP server** | `mcp` key in `opencode.json` | config only |
| Diagnostics for the agent | **LSP server** | `lsp` key in `opencode.json` | config only |

**Checked against** OpenCode `v1.18.33` docs and source (2026-09-29); `tool` /
`tool.schema` come from `@opencode-ai/plugin`, whose version tracks OpenCode. Package
provenance is owned by `/opencode-dev:sdk`. If the installed OpenCode differs,
re-check the pages above before relying on a key name.

**Facet boundary:** this skill covers **filesystem-discovered** standalone tools.
Registering a tool **programmatically from inside a plugin** (the `tool` map hook)
is `/opencode-dev:plugin` — both import `tool` from `@opencode-ai/plugin`, but
don't duplicate the plugin route here. Permission rules (keys, defaults, pattern
order) are owned by `/opencode-dev:policies`.

## 1. Custom tools — the filename/override traps

```ts
// .opencode/tools/database.ts  → tool name is "database" (filename == tool name)
import { tool } from "@opencode-ai/plugin"
export default tool({
  description: "Query the project database",
  args: { query: tool.schema.string().describe("SQL query to execute") },
  async execute(args, context) { return `ran: ${args.query}` },
})
```

- **Dir:** `.opencode/tools/` (project) or `~/.config/opencode/tools/` (global);
  top-level `*.ts`/`*.js` only. Plural is documented; v1.18.33 also scans `tool/`.
- **Filename = tool name.** `database.ts` → `database`.
- **A file named after a built-in OVERRIDES it.** Drop `bash.ts` in
  `.opencode/tools/` and your tool replaces the built-in `bash` (keyed by name).
  This is the supported way to sandbox/restrict a built-in.
- **Multiple named exports → `<filename>_<export>`.** `math.ts` exporting `add`
  and `multiply` yields `math_add` and `math_multiply` (NOT `add`/`multiply`).
- Args use `tool.schema` (Zod re-export). Plain-object form is allowed if you
  `import { z } from "zod"` yourself.
- `execute(args, context)` — `context` = `{ agent, sessionID, messageID,
  directory, worktree }`. Shell out to any language via `Bun.$` (see
  `references/custom-tools.rst` Python example).

## 2. MCP servers — `mcp` key, two transports

```jsonc
{ "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "local-srv":  { "type": "local",  "command": ["npx","-y","my-mcp"],
                    "enabled": true, "environment": { "MY_VAR": "v" } },
    "remote-srv": { "type": "remote", "url": "https://x.com", "enabled": true,
                    "headers": { "Authorization": "Bearer KEY" } } } }
```

- **Local env key is `environment`** (full word). This is the #1 trap — see §4.
- `type` (`"local"`/`"remote"`) is required. Non-obvious optionals: `timeout`
  (ms, default **5000**), plus `cwd` and `oauth`.
- **OAuth:** omit it and OpenCode auto-detects 401 → Dynamic Client Registration
  (RFC 7591). `"oauth": {}` triggers DCR explicitly; `"oauth": false` disables it.
  CLI: `opencode mcp add|list|auth|logout|debug`.
- **MCP tools are namespaced by the server name as prefix** — server `sentry`
  exposes `sentry_*`. You reference and gate them by that prefix.
- Caveat: MCP servers add to context; enabling a heavy one (e.g. GitHub MCP) can
  blow the context window.

### Gating MCP tools

Gate by the prefixed name. The MCP docs still show the legacy boolean `tools` map
(`"tools": { "sentry_*": false }`, re-enabled per agent under
`agent.<name>.tools`). Since v1.1.1 that map is deprecated and **converted into
`permission`** (`false` → `deny`, `true` → `allow`; an explicit `permission` entry at the
same level wins), so the current form is `"permission": { "sentry_*": "deny" }` —
which also allows `"ask"`. Rule order and defaults: `/opencode-dev:policies`.

## 3. LSP servers — `lsp` key is boolean-or-object

Disabled by default. The `lsp` key accepts a **boolean OR an object**:

| Value | Effect |
|---|---|
| `true` | Enable all built-in servers |
| omitted | All LSP disabled (the default) |
| `false` | Disable all LSP |
| `{}` | Keep built-ins + add/override custom entries |
| `{ "<srv>": { "disabled": true } }` | Disable one server, keep the rest |

```json
{ "$schema": "https://opencode.ai/config.json",
  "lsp": { "typescript": { "disabled": true },
           "custom-lsp": { "command": ["custom-lsp-server","--stdio"],
                           "extensions": [".custom"] } } }
```

Per-server fields beyond the example: `env` (object — NOT `environment`; see §4)
and `initialization` (object). Suppress auto-download with
`OPENCODE_DISABLE_LSP_DOWNLOAD=true`.

## 4. The two cross-cutting traps

**`environment` vs `env` — same concept, two spellings:**

| Layer | Env key |
|---|---|
| MCP local server (`mcp.<srv>`) | **`environment`** (full word) |
| LSP server (`lsp.<srv>`) | **`env`** (short) |
| Custom tool `tool()` | neither — use `Bun.$` / `process.env` in `execute` |

**`lsp` is overloaded three ways — keep them separate:**

| `lsp` as… | What it is |
|---|---|
| top-level **config key** | wires LSP *servers* (boolean-or-object, §3) |
| built-in **tool** named `lsp` | experimental; needs `OPENCODE_EXPERIMENTAL_LSP_TOOL=true` (or `OPENCODE_EXPERIMENTAL=true`) |
| **permission** key `lsp` | gates that tool's actions (policies facet) |

## 5. Built-in tools + the `apply_patch` / `edit` trap

Built-in tool names (this is the permission/gating vocabulary): `bash`, `edit`,
`write`, `read`, `grep`, `glob`, `lsp` (experimental), `apply_patch`, `skill`,
`todowrite`, `webfetch`, `websearch`, `question`.

- **`edit`, `write`, and `apply_patch` share ONE `edit` permission** — denying
  `edit` blocks all three (repeated here because the tool names suggest otherwise;
  permission rules are owned by `/opencode-dev:policies`).
- The patch tool is **`apply_patch`**, NOT `patch`. Its argument is
  **`output.args.patchText`** (NOT `filePath`) — relevant when a plugin's
  `tool.execute.before` inspects patch operations. Marker lines
  (`*** Add File:` / `*** Update File:` / `*** Delete File:`) carry relative
  paths inside `patchText`.
- `grep`/`glob` are powered by ripgrep and respect `.gitignore`; add a `.ignore`
  with `!node_modules/` to allow ignored paths.
- `todowrite` is disabled for subagents by default; `websearch` needs the OpenCode
  or OpenCode Go provider, or `OPENCODE_ENABLE_EXA` / `OPENCODE_ENABLE_PARALLEL` set.

## Assets
- `assets/custom-tool.ts` — minimal standalone tool template.
- `assets/mcp.json` — local + remote MCP server config (note `environment`).
- `assets/lsp.json` — custom + disabled LSP server config (note `env`).
