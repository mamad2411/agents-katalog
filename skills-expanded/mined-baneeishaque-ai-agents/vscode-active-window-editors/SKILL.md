---
name: vscode-active-window-editors
description: Composer — discover the active VS Code window's state.vscdb on macOS (workspaceStorage mtime + workspace.json title match) and delegate to vscode-state-vscdb-editor-extract to list open editor tabs (files, webviews, terminals) in pinned/display order with type tags, group markers, and pinned annotation.
category: VS Code / IDE Configuration
---

# VS Code Active Window Editors (v1.1.0)

> **Skill ID:** `vscode-active-window-editors`<br>
> **Version:** 1.1.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Composition Rationale

This skill is a **composer**: it does NOT re-implement VS Code `state.vscdb`
parsing or `serializedGrid` tree traversal. It owns the macOS-specific
discovery layer and delegates to the base skill
[`vscode-state-vscdb-editor-extract`](../vscode-state-vscdb-editor-extract/SKILL.md):

1. **Discovery** (this skill): locate the Code-family app's
   `~/Library/Application Support/<app>/User/workspaceStorage/` directory, sort
   entries by `mtime` descending (newest = active window), read `workspace.json`
   for title cross-check, and resolve `<entry>/state.vscdb`.
2. **Parsing** (base skill): shell out to the base script
   `extract-editors.py --db <resolved-path>` which opens the SQLite DB, reads
   `memento/workbench.parts.editor`, walks `serializedGrid`, and emits editor
   paths in display order with `sticky`-derived pinned annotation.

The layering test *"Could a different domain ever need the same primitive?"*
passes for the base (any tool parsing a vscdb's editor grid), but the
discovery heuristic is macOS + VS Code-specific — so it stays in the composer.
The composer verifies the base script exists (via anchored relative path) and
exits non-zero with a clear error if it is missing.

## Description

When a user wants to list what is currently open in a VS Code window's editor
tabs — files, webview/markdown-preview sources, and terminals — ordered by
their tab-bar (pinned-first) position, the only reliable source is the
**running window's** `state.vscdb`, not the view-state memento key. This skill
finds that database file automatically on macOS (without the user needing to
know the workspace hash) and delegates parsing to the base skill.

### The discovery method

VS Code stores per-window state under:

```text
~/Library/Application Support/<Code-app>/User/workspaceStorage/<workspace-hash>/state.vscdb
```

The `<workspace-hash>` directory is a SHA-256 of the workspace path with no
human-readable name inside it (a `workspace.json` sibling file has the folder
URI). The **actively running window** is reliably identified by sorting these
directories by **modification time** (`mtime` descending) — VS Code flushes
the window state to `state.vscdb` on state change, so the most-recently-touched
entry is the currently active window. The `workspace.json` `folder`/`workspace`
field confirms which workspace it belongs to.

### Why not JXA / accessibility?

**Lesson — applies to any skill that tries to read VS Code's open tabs via macOS
UI automation:** JXA / System Events can *control* VS Code as an application
(launch, focus, menus, keystrokes) exactly like any other macOS app, but it
**cannot enumerate the open editor tabs**. VS Code is an Electron app, and its
web-rendered tab content is not exposed to the macOS accessibility API in a
structured way — the accessibility tree returns empty for tab elements. The
source workflow confirmed this and pivoted to reading the `state.vscdb` SQLite
database directly, which is both more reliable and faster. Any future attempt to
list VS Code tabs through JXA/accessibility will hit the same wall — read
`state.vscdb` instead.

## When to Apply

Apply this skill when:

- You are on macOS and need what is open in the editor tabs of the **active**
  VS Code window — files, webview/markdown-preview sources, terminals — in
  tab-bar (pinned-first) order.
- You want to discover the active window's `state.vscdb` automatically (no need
  to know the workspace hash).
- You are composing a workflow that needs the live editor set of a running VS
  Code instance.

Apply the **base** [`vscode-state-vscdb-editor-extract`](../vscode-state-vscdb-editor-extract/SKILL.md)
directly when you already know the `state.vscdb` path and do not need
discovery.

Do NOT apply when:

- Running on Linux/Windows (the workspaceStorage path layout differs).
- VS Code is not currently running (the most-recent `mtime` entry may be stale).
- You only need recently-opened history, not currently-open tabs.

## Environment & Dependencies

| Requirement | Minimum | Notes |
| --- | --- | --- |
| Platform | macOS 12+ | workspaceStorage path layout is macOS-specific |
| Python | 3.12+ | Tier-1; stdlib only (`pathlib`, `json`, `subprocess`) |
| VS Code | Insiders / Stable / VSCodium / Cursor | Any Code-family app with `workspaceStorage` |
| Base skill | — | `vscode-state-vscdb-editor-extract/scripts/extract-editors.py` must exist |

## CLI Contract

| Flag | Required | Description |
| --- | --- | --- |
| `--app` | No | Code-family app name (default: auto-detect — tries `Code - Insiders`, `Code`, `VSCodium`, `Cursor`, `Code - Insiders Beta`, `Code - Exploration`) |
| `--db` | No | Override: use a specific `state.vscdb` path (skips discovery) |
| `--mode` | No | Pass `--mode` to the base extractor: `all` (default) or `files` |
| `--json` | No | Pass `--json` to the base extractor for machine-readable output |

**stdout** — the open editor tabs in tab-bar order (or JSON when `--json` is
passed — the base script's structured output). In `--mode all` (default), each
line is one tab: `[<type>] <label>` with `# group <id>` split-view markers and
a `[pinned]` suffix. `--mode files` emits the file-only projection (one
absolute fsPath per line).

**stderr** — discovery diagnostics (`App:`, `DB:`, `Workspace:` header lines),
including any warnings about missing apps or stale entries.

**Exit codes** — forwarded from the base script (0 = success, 2 = database /
usage error). Exit 2 also if discovery fails to find any Code-family app with
a `state.vscdb`.

## Protocol

### Step 1 — Run the discovery + extraction script

```bash
python3 .agents/skills/vscode/config/vscode-active-window-editors/scripts/list-active-window-editors.py
```

For the file-only projection:

```bash
python3 .agents/skills/vscode/config/vscode-active-window-editors/scripts/list-active-window-editors.py \
    --mode files
```

For machine-readable JSON:

```bash
python3 .agents/skills/vscode/config/vscode-active-window-editors/scripts/list-active-window-editors.py \
    --json
```

### Step 2 — Interpret the output

The script prints discovery info to stderr (`App:`, `DB:`, `Workspace:`), then
the base script's output to stdout. In `--mode all` (default), each line is one
tab — `[<type>] <label>` with `[pinned]` suffix; `# group <id>` markers denote
split-view groups. In `--mode files`, each line is an absolute file path with
an optional `[pinned]` suffix. In JSON mode, use the base skill's JSON schema
(groups, editors, `type`/`label`/`source_path` fields, `pinned` flag, `sticky`
count).

### Step 3 — (Optional) Override the database path

If discovery selects the wrong window (e.g., you have multiple VS Code instances
and want a specific one):

```bash
python3 .agents/skills/vscode/config/vscode-active-window-editors/scripts/list-active-window-editors.py \
    --db <path-to-specific-state.vscdb>
```

## Script Reference

`scripts/list-active-window-editors.py`:

1. Resolves the base script path via an anchored relative path
   (`__file__` / `../..` / `vscode-state-vscdb-editor-extract/scripts/extract-editors.py`)
   and verifies it exists (exit 2 if missing).
2. If `--db` is given, skips discovery and uses that path directly.
3. Otherwise, iterates `CODE_APP_NAMES` trying each Code-family app name in
   priority order, resolving `~/Library/Application Support/<app>/User/workspaceStorage/`.
4. For the first matching app, sorts workspaceStorage entries by `st_mtime_ns`
   descending and returns the newest entry that has a `state.vscdb`.
5. Reads `workspace.json` from that entry (for the `folder`/`workspace` URI
   cross-check, printed to stderr).
6. Invokes the base script via `subprocess.run([sys.executable, base_resolved,
   --db, db_path, [--mode, <mode>], [--json]])` and forwards its return code.

## Edge Cases

- **No Code-family app found**: exits 2 with an error listing the tried names.
- **Multiple windows**: the mtime heuristic picks the most-recently-flushed
  window. Use `--db` for an explicit path if this is wrong.
- **Multiple Code-family apps installed** (e.g., both stable and Insiders):
  tries them in `CODE_APP_NAMES` priority order; the first with a
  `workspaceStorage` is used. Override with `--app`.
- **Base script missing**: exits 2 with a clear message (the relative path is
  anchored to the composer script's own location, so it works regardless of
  `cwd`).
- **stale window state**: if VS Code was force-killed (not closed cleanly), the
  `mtime` may be old and the editor tab state stale. The script does not detect
  this — the user should verify the `Workspace:` line in stderr.
- **Terminal / webview tabs**: these are included in the default `--mode all`
  output (with `[type]` tags); use `--mode files` for a file-only projection
  if terminals/webviews are not wanted.

## Composition by Lower-Level Skills

| Primitive | Composition Mechanism |
| --- | --- |
| [`vscode-state-vscdb-editor-extract`](../vscode-state-vscdb-editor-extract/SKILL.md) | Shells out to `extract-editors.py --db <resolved-path> [--mode <mode>] [--json]` via `subprocess.run`; forwards return code. This base does all state.vscdb parsing; the composer only adds macOS window discovery. |

## Related Skills

- [`vscode-state-vscdb-merge`](../../../vscode-state-vscdb-merge/SKILL.md) —
  compares/merges `state.vscdb` across Git refs (complementary; not used by
  this workflow).

***

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Traceability

See [TRACEABILITY.md](TRACEABILITY.md).

***

<!-- Generated by the Skill Factory (skill-factory v1) -->
