---
name: mcp-cross-tool-config-sync
description: Single-canonical MCP server configuration shared across every AI tool (VS Code Copilot, JetBrains
    Copilot, Copilot CLI, Claude Desktop, Cursor, Windsurf, etc.) via a discover → backup → probe → generate →
    symlink → verify lifecycle, so one canonical edit propagates everywhere with zero drift.
category: Tool-Infrastructure
---

# MCP Cross-Tool Config Sync Skill (v2)

This skill establishes a **single source of truth (SSOT)** for MCP (Model Context Protocol) server definitions
and **distributes** schema-correct configs to every AI tool surface via a generator script and symbolic links.
One edit to the canonical file → one script run → every tool sees the new servers.

This is a **composer skill** that orchestrates several base primitives (see §14).

## 1. Problem Statement

The MCP ecosystem has split into multiple top-level JSON schemas:

| Schema key | Tools that use it |
| :--- | :--- |
| `mcpServers` | Claude Desktop, Claude Code, Cursor, Windsurf, Amazon Q, Kilo, Anti Gravity, Gemini CLI, **GitHub Copilot CLI** |
| `servers` | **VS Code GitHub Copilot**, **JetBrains GitHub Copilot** |
| `context_servers` | Zed (nested in `settings.json`) |
| (other) | emerging tools — discover via probe (§6) |

Per-tool divergences:

- VS Code Copilot accepts an `inputs` array (interactive prompts for env values).
- GitHub Copilot CLI requires a per-server `tools: ["*"]` access-control field.
- Most tools accept the same per-server shape (`type`, `command`, `args`, `env`).

Maintaining N hand-edited files is a drift trap. This skill enforces 1 canonical → N generated → N symlinks.

***

## 2. Architecture

```text
<canonical-root>/                          ← e.g., a private dotfile or config tree
├── mcp-servers.json                       ← SSOT (the only file you edit)
├── scripts/
│   └── generate-configs.py                ← generator (rerun after every canonical edit)
├── generated/                             ← never edit by hand; can be gitignored
│   ├── copilot-cli/mcp-config.json        ← `mcpServers` + `tools: ["*"]`
│   ├── jetbrains/mcp.json                 ← `servers`
│   ├── vscode/mcp.json                    ← `servers` + preserved `inputs`
│   └── <future-tool>/<filename>           ← one folder per tool
├── backups/                               ← mirror of each tool's native path
│   ├── copilot-cli/                       ← captured BEFORE first symlink
│   │   ├── mcp-config.json                ← (verbatim original)
│   │   ├── config.json                    ← any sibling files of interest
│   │   └── settings.json
│   ├── github-copilot/intellij/mcp.json
│   └── vscode-insiders/User/mcp.json
└── docs/
    └── tool-schema-records.md             ← cached probe results per tool/version (§5.5)
```

Each tool's native config path is replaced by a symlink → `generated/<tool>/...`.

The **mirrored backup tree** preserves each tool's ancestry on disk, so reverting is just
`cp -r backups/<tool>/* <native-tool-root>/` after deleting the symlink.

***

## 3. Lifecycle Overview

This skill is structured as a 7-phase lifecycle. Skip phases that don't apply (e.g., Phase 2 is no-op if all
target tools are already known schemas).

| Phase | Purpose | Delegates to |
| :--- | :--- | :--- |
| 0 | Inventory: enumerate target AI tools and their native config paths | this skill |
| 1 | Backup: mirror every native file under `backups/` BEFORE any symlink | this skill |
| 2 | Probe: discover schema for any tool with no documented format | [tool-config-schema-probe](../tool-config-schema-probe/SKILL.md) |
| 3 | Wire: add/edit canonical entries; add per-tool generator function | this skill |
| 4 | Generate: produce per-tool files + JSON-lint them | this skill |
| 5 | Symlink: replace native paths with symlinks → generated files | this skill |
| 6 | Verify: per-tool functional smoke test (server visible + callable) | this skill |
| 7 | Lifecycle: add new MCP servers, add new tools, update existing servers | this skill |

***

## 4. Phase 0 — Inventory

Before touching anything, build a **target tool table**. For each AI tool surface the user wants synchronized,
record:

| Tool | Native config path (POSIX example) | Top-level key | Schema status |
| :--- | :--- | :--- | :--- |
| VS Code Copilot (Insiders) | `<user-home>/Library/Application Support/Code - Insiders/User/mcp.json` | `servers` | known |
| VS Code Copilot (Stable) | `<user-home>/Library/Application Support/Code/User/mcp.json` | `servers` | known |
| JetBrains Copilot | `<user-home>/.config/github-copilot/intellij/mcp.json` | `servers` | known |
| GitHub Copilot CLI | `<user-home>/.copilot/mcp-config.json` | `mcpServers` + `tools` | known |
| Claude Desktop (macOS) | `<user-home>/Library/Application Support/Claude/claude_desktop_config.json` | `mcpServers` | known |
| Cursor | `<user-home>/.cursor/mcp.json` | `mcpServers` | known |
| Windsurf | `<user-home>/.codeium/windsurf/mcp_config.json` | `mcpServers` | known |
| Amazon Q | `<user-home>/.aws/amazonq/mcp.json` | `mcpServers` | known |
| Anti Gravity | varies — see [Anti Gravity Version Checker](../antigravity-version-checker/SKILL.md) | `mcpServers` | known |
| Zed | `<user-home>/.config/zed/settings.json` (nested under `context_servers`) | `context_servers` | known |
| OpenCode (Global) | `<user-home>/.config/opencode/opencode.json` | `mcp` | known |
| OpenCode (Project) | `./opencode.json` | `mcp` | known |
| Other / new tool | TBD | TBD | **probe required → §6** |

Cache this table in `<canonical-root>/docs/tool-schema-records.md`. The probe is then a one-time cost per tool.

If a row's "Schema status" is **probe required**, jump to Phase 2 for that tool only; otherwise proceed to
Phase 1.

***

## 5. Phase 1 — Backup (Mirrored Structure)

The cardinal rule: **back up BEFORE creating any symlink**. Once the native path is a symlink, any later
`cat / cp / read` returns the generated content, and the original tool-specific tweaks are lost forever.

### 5.1 Mirror Pattern

For each row in the inventory, mirror the native file's path **under** `backups/<short-tool-id>/` while
preserving meaningful structure. Two mirroring conventions, pick consistently:

1. **Tool-id prefix + bare filename** (compact; preferred for single-file configs):

    ```text
    <canonical-root>/backups/copilot-cli/mcp-config.json
    <canonical-root>/backups/jetbrains-intellij/mcp.json
    <canonical-root>/backups/vscode-insiders-user/mcp.json
    ```

2. **Mirror full sub-path under tool-id** (preferred when sibling files matter):

    ```text
    <canonical-root>/backups/vscode-insiders/User/mcp.json
    <canonical-root>/backups/vscode-insiders/User/settings.json
    <canonical-root>/backups/copilot-cli/mcp-config.json
    <canonical-root>/backups/copilot-cli/config.json          ← auth state
    <canonical-root>/backups/copilot-cli/settings.json
    ```

The skill's reference layout uses convention (2). Pick one and commit to it — mixing breaks `cp -r` reverts.

### 5.2 What to Back Up Per Tool

Don't back up only the MCP file. Back up **anything sibling that the tool may co-modify**, because tools often
rewrite multiple files in the same directory atomically.

| Tool | Files worth backing up |
| :--- | :--- |
| Copilot CLI | `mcp-config.json`, `config.json` (auth/login), `settings.json`, `command-history-state.json` |
| VS Code Copilot | `mcp.json` (only — `settings.json` is governed elsewhere) |
| JetBrains Copilot | `mcp.json` (template often contains comments — preserve them in backup) |
| Claude Desktop | `claude_desktop_config.json` (full file, includes non-MCP keys) |
| Zed | full `settings.json` (MCP shares the file with editor settings) |

For tools where MCP config shares a file with unrelated settings (Zed, Claude Desktop), Phase 5 symlink is
**inappropriate** — instead, the generator must write **a fragment** that you splice in via `jq`. See §9.2.

### 5.3 Backup Command Pattern

```bash
mkdir -p "<canonical-root>/backups/<tool-id>/<sub-path>"
cp -p "<native-path>" "<canonical-root>/backups/<tool-id>/<sub-path>/"
# -p preserves mtimes & permissions so you have authentic forensic timestamps
```

For full-directory backups (e.g., the Copilot CLI dotfile dir):

```bash
mkdir -p "<canonical-root>/backups/copilot-cli"
cp -Rp "<user-home>/.copilot/." "<canonical-root>/backups/copilot-cli/"
```

### 5.4 Backup Verification

```bash
# 1. Listing matches expectations
find "<canonical-root>/backups" -type f | sort

# 2. Sizes are non-zero (catches read-permission failures)
find "<canonical-root>/backups" -type f -size 0

# 3. Content sanity
diff "<native-path>" "<canonical-root>/backups/<tool-id>/<sub-path>/<filename>"
# Empty diff = identical = safe to proceed.
```

If any backup fails, **abort the entire workflow** — do not symlink without a verified backup.

### 5.5 Cache Backup Provenance

Append a row to `<canonical-root>/docs/tool-schema-records.md` for every backed-up file noting: tool name,
version captured, file path, file size, and mtime. This is your forensic trail when reverting later.

***

## 6. Phase 2 — Probe Unknown Tools (delegated)

If Phase 0 left any row marked **probe required**, delegate to the
[Tool Config Schema Probe Skill](../tool-config-schema-probe/SKILL.md). Do NOT inline the probe logic here.

### 6.1 What to Hand Back to This Skill

The probe must return:

1. The **canonical config path** for the tool on this OS.
2. The **top-level key** that holds server entries (`mcpServers` / `servers` / `context_servers` / other).
3. The **per-entry shape** the tool persisted (which keys it kept, which it normalized away).
4. Any **tool-specific extensions** (e.g., Copilot CLI `tools: ["*"]`, VS Code `inputs`).
5. The **reload behavior** (hot-reload vs. restart-required).

### 6.2 MCP-Specific Sentinel Recipe

When using the probe skill against an AI tool that exposes an MCP setup UI, use this concrete sentinel:

| Probe field | Value |
| :--- | :--- |
| Server name | `probe-dummy-DELETE-ME` |
| Type | `stdio` |
| Command | `echo` (universally available, exits 0 immediately) |
| Args | `["probe"]` |
| Env | (empty) |

Steps (mirrors [Probe Skill §2](../tool-config-schema-probe/SKILL.md#2-operational-logic)):

1. Capture pre-snapshot of all candidate config roots (Probe Skill §2.1).
2. Open the tool's MCP UI (e.g., Copilot CLI `/mcp` slash command, VS Code `MCP: Add Server`,
    JetBrains Copilot tool window → Add MCP server).
3. Submit the sentinel above through the UI.
4. Diff the filesystem (Probe Skill §2.3); grep for `probe-dummy-DELETE-ME`.
5. The hit reveals path + schema. Record per Probe Skill §2.5.
6. Remove the sentinel via the same UI (preferred) OR by `jq` editing once schema is known.

### 6.3 Promote Probe Findings into the Inventory

After the probe completes, update the Phase 0 table row from "probe required" to "known", and append the full
record to `docs/tool-schema-records.md` so the next operator (or future you) does not re-probe.

### 6.4 Then Continue Backup

Once you know the path, **immediately** loop back to Phase 1 and back up that file before going further.

***

## 7. Phase 3 — Wire (Canonical + Generator)

### 7.1 Canonical File

The canonical file uses the **dominant** `mcpServers` schema (so the majority of tools are pass-through) with
`inputs` as an optional sibling key for VS Code's prompt mechanism:

```json
{
  "inputs": [
    { "id": "ado_org", "type": "promptString",
      "description": "Azure DevOps organization name", "password": false }
  ],
  "mcpServers": {
    "ssh": {
      "type": "stdio",
      "command": "/opt/homebrew/bin/mise",
      "args": ["x", "node", "--",
               "npx", "--yes", "--package=mcp-ssh", "-c",
               "node \"$(npm root)/mcp-ssh/dist/server.js\""],
      "env": { "SSH_PORT": "8889", "SSH_LOG_LEVEL": "info" }
    }
  }
}
```

#### 7.1.1 Server-Entry Conventions (delegated SSOT)

For absolute-path mandates, env-var naming, alphabetical ordering, and secret hygiene, the
[MCP Server Management Skill](../mcp-management/SKILL.md) §2.2 is the SSOT. This skill does **not** restate those
rules — it consumes them.

#### 7.1.2 npm Package Without `bin` Field (mcp-ssh idiom)

`mcp-ssh` ships no `bin` shim, so `npx mcp-ssh` fails. Use the `--package=<name> -c '<command>'` form, which
installs the package then runs an arbitrary command inside that ephemeral env, and resolve the entry script via
`$(npm root)`. Wrap the whole thing in `mise x node --` so the correct Node toolchain is selected. To verify the
actual `dist/server.js` path before pinning it, run `npm root -g` (or with `mise`: `mise x node -- npm root -g`)
and inspect `<root>/<package>/package.json` for the `main` field. See the
[Mise Tool Management Skill](../mise-tool-management/SKILL.md) for the runtime-wrapping pattern.

#### 7.1.3 Prefer Direct Binary Over `npx`

The `npx` wrapper above is justified **only** because `mcp-ssh` exposes no binary. For any package that ships a
real CLI shim, invoke the binary directly (e.g., `/opt/homebrew/bin/markdownlint-cli2`) — `npx` adds startup
latency and is non-deterministic about which version it runs.

### 7.2 Per-Tool Generator Functions

The generator (`scripts/generate-configs.py`) loads the canonical file once and writes one output per tool.
Each generator function is a pure transform of the same input dict:

| Function | Output | Transform |
| :--- | :--- | :--- |
| `gen_copilot_cli` | `generated/copilot-cli/mcp-config.json` | passthrough `mcpServers`; inject `tools: ["*"]` per server |
| `gen_vscode` | `generated/vscode/mcp.json` | rename `mcpServers` → `servers`; preserve `inputs` |
| `gen_jetbrains` | `generated/jetbrains/mcp.json` | rename `mcpServers` → `servers`; drop `inputs` |
| `gen_claude_desktop` | `generated/claude-desktop/claude_desktop_config.json` | passthrough `mcpServers` |
| `gen_cursor` | `generated/cursor/mcp.json` | passthrough `mcpServers` |
| `gen_windsurf` | `generated/windsurf/mcp_config.json` | passthrough `mcpServers` |
| `gen_opencode` | `generated/opencode/opencode.json` | rename `mcpServers` → `mcp`; preserve structure; handles `type: remote` entries with `url`+`headers` intact |

**Remote-server note**: `gen_opencode` is the only generator that handles servers with `type: remote`, `url`,
and `headers` fields — OpenCode's [remote MCP schema](../opencode-remote-mcp-setup/SKILL.md) supports both
stdio (`type: local`) and HTTP/WebSocket (`type: remote`) servers. The other generators (copilot-cli, VS Code,
JetBrains, Claude Desktop, Cursor, Windsurf) assume stdio-only (`command`/`args`) entries and would produce
invalid configs if passed a remote server. Filter remote entries before feeding the canonical into those
generators, or extend their transform logic.

A `with_stdio_default(server)` helper injects `"type": "stdio"` if a `command` field exists but no `type` is
set, so the canonical file can omit the noise.

A reusable template lives at [`scripts/generate-configs.py`](scripts/generate-configs.py).

#### 7.2.1 Adding a New Tool's Generator Function

Procedure (mandatory order — skipping steps causes silent breakage):

1. **Probe** (Phase 2) → know the path, top-level key, per-entry shape.
2. **Backup** (Phase 1) → mirror the native file under `backups/<tool-id>/`.
3. **Implement** `gen_<tool>(canonical)` in `scripts/generate-configs.py`. Its sole job is to:
    - Rename top-level key if needed.
    - Add tool-specific per-entry fields (e.g., `tools: ["*"]`).
    - Drop fields the tool rejects (e.g., `inputs` for JetBrains).
    - Write to `generated/<tool>/<filename>` via the shared `write_json` helper.
4. **Append** the function to the `GENERATORS` tuple at the bottom of the script.
5. **Run** Phase 4 to generate; **then** Phase 5 to symlink.

Do NOT generate-and-symlink for the new tool until backup is verified.

### 7.3 Script Language Justification

Per the [Script Language Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md) §4 (PowerShell-First),
this script's documented technical justification for Python is:

- The canonical store typically lives in a private user-data tree, not in the PowerShell-managed
    `ai-agent-rules` tree. PowerShell Core is not guaranteed in arbitrary macOS dotfile environments.
- Cross-platform JSON manipulation against arbitrary filesystem paths and POSIX symlinks is more direct in
    Python's `pathlib` and `json` stdlib than in PowerShell on macOS / Linux.
- Zero external dependencies; runs on any system Python ≥ 3.7.

***

## 8. Phase 4 — Generate + JSON-Lint

```bash
cd <canonical-root>
python3 scripts/generate-configs.py
# expected output:
#   canonical: mcp-servers.json
#   output:    generated/
#     wrote generated/copilot-cli/mcp-config.json
#     wrote generated/vscode/mcp.json
#     wrote generated/jetbrains/mcp.json
#     wrote generated/claude-desktop/claude_desktop_config.json
#     wrote generated/cursor/mcp.json
#     wrote generated/windsurf/mcp_config.json
#     wrote generated/opencode/opencode.json
#   done.

# JSON-lint every produced file
for f in $(find generated -type f -name '*.json'); do
    jq empty "$f" && echo "OK $f" || { echo "FAIL $f"; exit 1; }
done
```

If any file fails `jq empty`, the generator has a bug — fix it before symlinking.

***

## 9. Phase 5 — Symlink Distribution

After Phase 1 backup is verified AND Phase 4 generates pass `jq empty`,
each consumer tool's native MCP config file is replaced by a symlink to
the corresponding generated artefact.

**Preferred path: let the generator do it.** Per the [Script-Over-Instruction
Principle](#73-script-language-justification), the generator script
[`scripts/generate-configs.py`](scripts/generate-configs.py) deploys
consumer-side symlinks automatically (relative-path, idempotent, scoped
to the machines where each consumer's parent directory exists). One
canonical edit + one `python3 scripts/generate-configs.py` invocation
generates the per-tool files AND repairs/installs the consumer symlinks
in one deterministic pass. Add new tools' link/target pairs to the
`DEPLOY_TARGETS` map in the script.

Pass `--no-deploy` to generate only (e.g., for CI / dry-run).

| Tool | Native path | Symlink target |
| :--- | :--- | :--- |
| VS Code Insiders Copilot | `<user-home>/Library/Application Support/Code - Insiders/User/mcp.json` | `<canonical-root>/generated/vscode/mcp.json` |
| JetBrains GitHub Copilot | `<user-home>/.config/github-copilot/intellij/mcp.json` | `<canonical-root>/generated/jetbrains/mcp.json` |
| GitHub Copilot CLI | `<user-home>/.copilot/mcp-config.json` | `<canonical-root>/generated/copilot-cli/mcp-config.json` |
| OpenCode (Global) | `<user-home>/.config/opencode/opencode.json` | `<canonical-root>/generated/opencode/opencode.json` |
| OpenCode (Project) | `./opencode.json` | `<canonical-root>/generated/opencode/opencode.json` |

The manual replace pattern below remains documented for bootstrap cases
(brand-new consumer added before the script knows about it) and for
audit / rollback.

### 9.1 Replace Pattern (POSIX)

```bash
# 1. Confirm backup exists (idempotent guard)
test -f "<canonical-root>/backups/<tool-id>/<sub-path>/<filename>" \
    || { echo "ABORT: no backup for <tool>"; exit 1; }

# 2. Remove the native file (parent dir must already exist for the tool)
rm "<native-path>"

# 3. Create the symlink (target path must be ABSOLUTE for portability across shells)
ln -s "<canonical-root>/generated/<tool>/<filename>" "<native-path>"

# 4. Verify
ls -la "<native-path>"            # arrow points to generated file
readlink "<native-path>"          # exact target path
test -f "<native-path>" && echo "resolves OK"
diff "<native-path>" "<canonical-root>/generated/<tool>/<filename>"  # empty
```

### 9.2 Tools That Cannot Be Symlinked Whole

Some tools store MCP servers as a **nested key inside a larger config file** (Zed under `context_servers` in
`settings.json`, Claude Desktop's file may contain non-MCP keys). For these, a whole-file symlink would
overwrite unrelated settings.

Two safe alternatives:

1. **Splice on every regenerate**: extend the generator to read the existing native file, splice in the
    MCP slice via `jq` or Python `dict.update`, and write back. The native file remains a real file (not a
    symlink). Cost: must re-run after editing canonical AND after the user changes other settings.
2. **Sidecar + tool-supported include**: if the tool supports an `include` directive (rare), point the include
    at the generated file and symlink only the included file.

If neither is viable, document the tool as **not synchronizable** and exclude it from the inventory.

***

## 10. Phase 6 — Functional Verification

JSON-validity is necessary but not sufficient. Each tool MUST be confirmed to actually load and use the
synchronized server list.

### 10.1 Per-Tool Smoke Tests

| Tool | Verification |
| :--- | :--- |
| GitHub Copilot CLI | Launch `copilot`; in the TUI run `/mcp`; confirm canonical servers appear. Then trigger a tool that depends on a server (e.g., ssh) and confirm success. |
| VS Code Copilot | Reload window. Open Chat → "MCP Servers" view (Command Palette: `MCP: List Servers`); confirm canonical servers appear with status "Running". |
| JetBrains Copilot | Restart IDE. Open the Copilot tool window → Settings → MCP; confirm servers appear. |
| Claude Desktop | Quit (⌘Q — not just close) and relaunch. Open the developer console (Help menu) and confirm MCP server logs show successful connection. |
| Cursor / Windsurf | Restart the editor; check MCP indicator in status bar. |
| OpenCode | Restop opencode client; check if MCP servers appear in the server list or can be used in chat. |

### 10.2 Failure Triage

If a tool reports zero servers after symlinking:

1. `readlink <native-path>` → did the symlink survive?
2. `cat <native-path>` → does the resolved content have the right top-level key for THIS tool?
3. `jq empty <native-path>` → still valid JSON?
4. Tool's own log / console → does it complain about a specific field?

If a server appears but fails to launch: that's a server-entry problem, not a sync problem — re-derive the
entry per [MCP Server Management](../mcp-management/SKILL.md) and the runtime-wrapping pattern in §7.1.2.

### 10.3 Record What Was Verified

Update `docs/tool-schema-records.md` with a verification timestamp and which servers were confirmed live in
which tool. This is the audit trail.

***

## 11. Phase 7 — Lifecycle (Steady-State Operations)

### 11.1 Adding a New MCP Server

1. Edit `<canonical-root>/mcp-servers.json` — add the new entry to `mcpServers` (alphabetical per
    [MCP Server Management](../mcp-management/SKILL.md) §2.2).
2. `python3 scripts/generate-configs.py`
3. JSON-lint the regenerated files (§8).
4. Reload each tool surface that has an active session.
5. Verify the new server appears in at least one tool (§10.1).

No backup needed for additive changes — backups are required only when **replacing** a native file.

### 11.2 Modifying an Existing MCP Server

Same as §11.1. Tools will pick up the changed `command` / `args` / `env` on next launch (or window reload).

### 11.3 Removing an MCP Server

1. Delete the entry from canonical.
2. Regenerate.
3. If a tool caches MCP server state (some IDEs do), restart fully — a window reload is not always enough.

### 11.4 Adding a New Tool to the Sync

1. Phase 0: add the tool to the inventory table.
2. Phase 2: probe if schema unknown.
3. Phase 1: backup the native file.
4. Phase 7.2.1 of §7: implement `gen_<tool>` and append to `GENERATORS`.
5. Phase 4: regenerate + lint.
6. Phase 5: symlink.
7. Phase 6: verify.

### 11.5 Removing a Tool from the Sync

1. `rm <native-path>` (the symlink).
2. `cp <canonical-root>/backups/<tool-id>/<sub-path>/<filename> <native-path>` to restore the original.
3. Optionally: delete the `gen_<tool>` function and remove the `generated/<tool>/` folder.
4. Optionally: keep the backup in place as historical record.

### 11.6 Reverting a Bad Sync

If a generator change broke a tool:

```bash
rm <native-path>                                              # delete bad symlink
cp <canonical-root>/backups/<tool-id>/<sub-path>/<filename> \
   <native-path>                                              # restore original
```

Then fix the generator and re-run Phases 4–6.

***

## 12. Failure Modes (Aggregated)

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| Tool reports zero MCP servers | Symlink broken, wrong schema key, or tool not reloaded | §10.2 triage |
| Server immediately disconnects with `MCP error -32000: Connection closed` | Package advertises "MCP" but ships an HTTP REST server (e.g., `mcp-ssh` 1.0.1) — never writes JSON-RPC frames to stdout | Before adding any npm package, confirm it depends on `@modelcontextprotocol/sdk` (`npm view <pkg> dependencies.@modelcontextprotocol/sdk`); pipe-test with `echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \| <command> <args>` and expect a JSON-RPC response. Swap to a real stdio MCP server. |
| `npx mcp-ssh` fails with "command not found" | Package has no `bin` field | Use `--package=mcp-ssh -c '<command>'` form (§7.1.2) |
| VS Code Copilot ignores `inputs` | Generated file landed under `mcpServers` not `servers` | Re-run `gen_vscode` |
| Hot-edit to native file silently lost | User edited the symlink target instead of canonical | Always edit `mcp-servers.json` only; revert via §11.6 |
| Tool restart needed but not done | Most IDEs do not hot-reload MCP config | Reload window / restart IDE |
| Backup empty or missing | `cp` ran before the file existed, or wrong path | Re-run Phase 1; do NOT proceed to Phase 5 without verified backup |
| Sentinel "probe-dummy" left in production config | Probe cleanup phase skipped | Remove via tool UI or `jq` edit; see [Probe Skill §2.4](../tool-config-schema-probe/SKILL.md) |
| Tool config file is shared with non-MCP settings | Tool stores MCP nested in a larger settings file | Use splice strategy (§9.2.1), not whole-file symlink |
| Probe returned wrong path | Tool wrote to a workspace-scoped file instead of global | Re-probe in the global UI scope; consult Probe Skill §3 |

***

## 13. Prohibited Behaviors

- **DO NOT** edit any file under `generated/` directly — it will be overwritten on the next generator run.
- **DO NOT** edit a tool's native config path (it's a symlink — your edit lands in `generated/` and is destroyed
    on the next regenerate).
- **DO NOT** symlink without first backing up the original — tool-specific manual tweaks would be lost silently.
- **DO NOT** introduce a new tool by hand-editing `generated/<tool>/...`. Always add a `gen_<tool>` function.
- **DO NOT** invent a schema variant. Discover via the [Probe Skill](../tool-config-schema-probe/SKILL.md), then
    add a generator function — never mutate the canonical schema to fit a new tool.
- **DO NOT** leave dummy / probe / sentinel entries in any generated, native, or canonical file.
- **DO NOT** use relative paths in `ln -s` — symlink targets MUST be absolute, otherwise the link breaks if the
    native path's parent directory differs in depth from the canonical root.
- **DO NOT** symlink files that mix MCP config with unrelated settings (Zed `settings.json`, Claude Desktop's
    full config when it has non-MCP keys) — use the splice strategy (§9.2.1) instead.

***

## 14. Composition Map

This composer skill is built from these primitives. Each primitive owns its domain; this skill only orchestrates.

| Phase | Delegated to base skill | What this skill provides |
| :--- | :--- | :--- |
| 0 Inventory | — (orchestration) | Target tool table format |
| 1 Backup | — (orchestration) | Mirroring conventions, sibling-file rules |
| 2 Probe | [tool-config-schema-probe](../tool-config-schema-probe/SKILL.md) | When to probe, how to feed results back, MCP-specific sentinel recipe |
| 3.1 Server entries | [mcp-management](../mcp-management/SKILL.md) | Canonical file shape |
| 3.1.2 runtime wrapping | [mise-tool-management](../mise-tool-management/SKILL.md) | `mise x` wrapping pattern, `npm root` usage for bin-less packages |
| 3 Generator hygiene | [python-script-generation](../python-script-generation/SKILL.md) (implicit) | Generator template (`scripts/generate-configs.py`) |
| 4 Generate | — (orchestration) | Generator + JSON-lint sequence |
| 5 Symlink | — (orchestration) | Replace pattern, splice fallback |
| 6 Verify | — (orchestration) | Per-tool smoke test matrix |
| 7 Lifecycle | — (orchestration) | Add/modify/remove flows for servers and tools |
| Doc redaction | [redaction-portability](../redaction-portability/SKILL.md) | Applied to `docs/tool-schema-records.md` before commit |
| Tool-presence checks | [system-wide-tool-management](../system-wide-tool-management/SKILL.md) | `jq`, `python3`, `ln`, `find`, `diff` |

***

## 15. Related Skills

- [`mcp-management`](../mcp-management/SKILL.md) — Server-entry SSOT consumed by this skill's canonical schema
- [`opencode-remote-mcp-setup`](../opencode-remote-mcp-setup/SKILL.md) — OpenCode-specific remote MCP server composer
- [`tool-config-schema-probe`](../tool-config-schema-probe/SKILL.md) — Base primitive for discovering new tool schema
- [`opencode-jsonc-util`](../opencode-jsonc-util/SKILL.md) — Base JSONC utility for OpenCode config files

## 16. Related Conversations & Traceability

Session logs for the architectural decisions behind this skill (schema-split discovery, probe-dummy trick,
generator + symlink rollout) live under [`docs/conversations/`](../../../docs/conversations/). Apply the
[Redaction & Portability Skill](../redaction-portability/SKILL.md) before adding new logs.
