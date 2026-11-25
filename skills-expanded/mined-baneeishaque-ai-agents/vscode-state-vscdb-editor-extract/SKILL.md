---
name: vscode-state-vscdb-editor-extract
description: Base primitive — parse a VS Code state.vscdb SQLite database's memento/workbench.parts.editor key, walk the serializedGrid tree, and emit open editor tabs (files, webviews/markdown-preview sources, terminals) in display (tab-bar) order with type tags, group markers, and pinned annotation from the group-level 'sticky' count.
category: VS Code / IDE Configuration
---

# VS Code state.vscdb Editor Extract (v1.1.0)

> **Skill ID:** `vscode-state-vscdb-editor-extract`<br>
> **Version:** 1.1.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Composition Rationale

This skill is a **base skill**: it owns a single generic primitive — parsing a
VS Code `state.vscdb` SQLite database to extract the currently-open editor tab
paths in display (tab-bar) order, with pinned annotation.

The layering test (*"Could a different domain ever need the same primitive?"*)
is **YES**: any workflow that needs to recover, audit, or compare the live editor
state of a VS Code window — stash triage, session-full-change-audit, CI recovery,
environment restore — reuses this parser. The discovery of *which* `state.vscdb`
to read (macOS workspaceStorage mtime heuristic, window-title matching) is
domain-specific and lives in the composer
[`vscode-active-window-editors`](../vscode-active-window-editors/SKILL.md),
which shells out to `scripts/extract-editors.py`.

Bidirectional discoverability: the composer links back here in its
`## Related Skills` section, and this skill lists the composer in
`## Composition by Higher-Level Skills`.

## Description

VS Code persistes the live editor tab state in the running window's
`workspaceStorage/<hash>/state.vscdb` SQLite database. The relevant data is
under memento key `memento/workbench.parts.editor`, whose JSON blob contains
`editorpart.state.serializedGrid.root` — a tree of `branch`/`leaf` nodes where
each `leaf` represents an editor group.

The `editors[]` array on each leaf group is stored in **display order** (the
exact left-to-right order of the tab bar, pinned tabs first). Each editor
entry has an `id` field distinguishing file editors
(`workbench.editors.files.fileEditorInput`) from terminals
(`workbench.editors.terminal`) and webviews (`workbench.editors.webviewEditor`,
e.g. markdown previews and custom editors), plus a `value` field (a JSON
string) containing the resource URI / fsPath.

The default text mode (`--mode all`) emits **every** tab — files, webviews,
and terminals — with a `[type]` tag, `# group` markers between split-view
groups, and a `[pinned]` suffix. Webview tabs resolve their backing source
file (markdown preview source, custom-editor resource) from `value['state']`.
`--mode files` emits the file-only projection (one absolute fsPath per line)
for callers that want just source files.

The **pinned** state is **not** stored per-editor. Instead, each group dict
carries a `sticky: <N>` integer = the number of pinned (sticky) editors.
Editors at array index `< N` are pinned. The `mru` field is an alternative
ordering axis (most-recently-used) and must **not** be confused with display
order.

This skill also documents the key negative finding from its source session:
the `memento/workbench.editors.files.textFileEditor` memento stores
*view-state history* for all editors ever opened in the window — including
closed tabs — and is therefore **not** a reliable source for "currently open"
tabs.

## When to Apply

Apply this skill when:

- You have a VS Code `state.vscdb` file and need to list what is currently
  open in a window's editor tabs — files, webview/markdown-preview sources,
  and terminals — in tab-bar order.
- You need to know which tabs are pinned (sticky), their tab-bar order, or
  which split-view group each tab belongs to.
- You are composing a higher-level workflow that operates on the editor grid
  (e.g. restoring a specific layout, auditing open files).

Apply the **composer** [`vscode-active-window-editors`](../vscode-active-window-editors/SKILL.md)
instead when you do **not** already know the `state.vscdb` path and need to
discover the active window's database automatically on macOS.

Do NOT apply when:

- You need to compare `state.vscdb` across Git refs — use
  [`vscode-state-vscdb-merge`](../../../vscode-state-vscdb-merge/SKILL.md) instead.
- The database file is not a VS Code `state.vscdb` (different schema) — use
  `sqlite3` CLI directly.
- You only need recently-opened history (not currently-open tabs) — read the
  `history.entries` key instead.

## Environment & Dependencies

| Requirement | Minimum | Notes |
| --- | --- | --- |
| Python | 3.12+ | Tier-1; stdlib only (`sqlite3`, `json`, `argparse`) |
| state.vscdb | VS Code 1.x | Any Code-family fork (VS Code, Insiders, VSCodium, Cursor) |
| Read access | — | The `--db` path must be readable; the script opens the DB read-only |

## CLI Contract

| Flag | Required | Description |
| --- | --- | --- |
| `--db` | Yes | Absolute path to a `state.vscdb` SQLite file |
| `--key` | No | Memento key to read (default: `memento/workbench.parts.editor`) |
| `--mode` | No | Text output mode: `all` (default) or `files` |
| `--json` | No | Emit machine-readable JSON to stdout (default: human text) |

**Text output, `--mode all` (default)** — every tab in tab-bar order, one line
per tab, with a `[type]` tag, `# group <id>` markers between split-view groups,
and a `[pinned]` suffix on pinned tabs:

```text
# group 20
[terminal ] opencode.exe [pinned]
[webview  ] /abs/path/preview-source.md
[file     ] /abs/path/file-a.ts
# group 23
[file     ] /abs/path/file-b.ts [pinned]
```

`type` ∈ `file` | `webview` | `terminal` | `other`. The label is the fsPath
(file), the resolved source path or title (webview), the title (terminal), or
the editor id (other).

**Text output, `--mode files`** — the file-only projection: one absolute
fsPath per line, in tab-bar order, `[pinned]`-annotated. Webview and terminal
tabs are omitted; when no file editors exist, non-file tabs are emitted as
`#non-file:` markers:

```text
/abs/path/file-a.ts [pinned]
/abs/path/file-b.ts
#non-file: opencode.exe
```

**JSON output** — structured; every editor record carries `type`, `label`, and
`source_path` in addition to the original fields:

```json
{
  "db_path": "/abs/path/state.vscdb",
  "memento_key": "memento/workbench.parts.editor",
  "key_found": true,
  "groups": [
    {
      "group_id": 20,
      "sticky": 7,
      "size": 0,
      "mru": [25, 23, 24, ...],
      "editors": [
        {"index": 0, "editor_id": "workbench.editors.terminal",
         "type": "terminal", "title": "opencode.exe", "fs_path": null,
         "source_path": null, "label": "opencode.exe", "pinned": true,
         "group_id": 20, "group_sticky": 7},
        {"index": 1, "editor_id": "workbench.editors.webviewEditor",
         "type": "webview", "title": null, "fs_path": null,
         "source_path": "/abs/path/preview-source.md",
         "label": "/abs/path/preview-source.md", "pinned": false,
         "group_id": 20, "group_sticky": 7},
        {"index": 2, "editor_id": "workbench.editors.files.fileEditorInput",
         "type": "file", "title": null, "fs_path": "/abs/path/file-a.ts",
         "source_path": null, "label": "/abs/path/file-a.ts", "pinned": false,
         "group_id": 20, "group_sticky": 7}
      ]
    }
  ],
  "total_editors": 33,
  "total_file_editors": 32
}
```

**Exit codes:**

| Exit | Meaning |
| --- | --- |
| 0 | Success (editors extracted, or key not found with warning) |
| 2 | Database not found / cannot open / usage error |

## Protocol

### Step 1 — Locate the `state.vscdb`

Either pass a known path via `--db`, or use the composer
[`vscode-active-window-editors`](../vscode-active-window-editors/SKILL.md)
to discover the active window's database automatically on macOS.

### Step 2 — Run the extraction script

```bash
python3 .agents/skills/vscode/config/vscode-state-vscdb-editor-extract/scripts/extract-editors.py \
    --db <path-to-state.vscdb>
```

For the file-only projection:

```bash
python3 .agents/skills/vscode/config/vscode-state-vscdb-editor-extract/scripts/extract-editors.py \
    --db <path-to-state.vscdb> \
    --mode files
```

For machine-readable output:

```bash
python3 .agents/skills/vscode/config/vscode-state-vscdb-editor-extract/scripts/extract-editors.py \
    --db <path-to-state.vscdb> \
    --json
```

### Step 3 — Interpret the output

- **Text mode (`all`)**: each line is one tab: `[<type>] <label>`. `[pinned]`
  means the tab is pinned (sticky). `# group <id>` marks the start of each
  split-view group. The order matches the tab bar left-to-right across every
  group.
- **Text mode (`files`)**: each line is an absolute file path. `[pinned]`
  suffix means the tab is pinned (sticky).
- **JSON mode**: inspect the `groups[].editors[]` array. `pinned` is derived
  from `index < group_sticky`. `type` classifies the tab; `source_path` holds
  the webview's backing file. The `mru` array provides an alternative MRU
  ordering if needed.

## Script Reference

`scripts/extract-editors.py`:

1. Opens the `state.vscdb` as a read-only SQLite connection (`file:<path>?mode=ro`).
2. Reads the `ItemTable` row for memento key `memento/workbench.parts.editor`
   (overridable via `--key`).
3. Parses the JSON blob → navigates to `editorpart.state.serializedGrid.root`.
4. Recursively walks the tree (`walk_grid`) collecting every `leaf`-type node
   (editor groups).
5. For each group, iterates `editors[]` in array order (display order), parses
   each editor's `value` JSON string, and classifies it:
   - `file` (`fileEditorInput`) → `extract_fs_path` reads
     `resourceJSON.path` / `resource.path` / top-level `path`.
   - `webview` (`webviewEditor`) → `extract_webview_source_path` reads the
     `state` field (a JSON-encoded string) and resolves its `resource` key —
     a URI dict (`fsPath`/`path`) or a `file://` string — plus top-level
     fallbacks; stored as `source_path`.
   - `terminal` (`terminal`) → title only, no path.
   - `other` → editor id / title.
   Every record also carries a display `label`.
6. Annotates `pinned = index < group['sticky']` (the sticky count is the only
   pinned signal — VS Code does not serialize a per-editor `pinned` flag).
7. Emits text — `--mode all` (every tab with `[type]` tags + `# group`
   markers) or `--mode files` (file-only projection) — or full structured JSON
   with `--json`.

## Edge Cases

- **Key not found**: The script prints a warning to stderr and returns an empty
  `groups` list with `key_found: false`. This happens when the window has never
  saved its editor state (e.g., first launch, or a window that was force-killed
  before flush).
- **Multiple editor groups (split views)**: The grid tree contains multiple
  `leaf` nodes, each a separate group. All are enumerated; in `all` mode each
  group is preceded by a `# group <id>` marker so the output reflects the
  on-screen grid layout.
- **Non-file editors** (terminals, webviews, diff editors): classified as
  `terminal` / `webview` / `other` in `all` mode; in `files` mode they are
  omitted unless no file editors exist, in which case they appear as
  `#non-file:` markers.
- **Webview source path**: webview entries have no top-level
  `resourceJSON`/`resource`. Their backing file lives in `value['state']`
  (JSON-encoded string) → `resource`, which may be a URI dict
  (`path`/`fsPath`) or a `file://` string. The script resolves all three
  shapes. Webviews without a resolvable source (e.g. `html.preview`) fall back
  to their title.
- **`resourceJSON` vs `resource`**: Newer VS Code versions serialize the file
  resource under `resourceJSON`; older versions use `resource`. The script
  checks both.
- **`mru` ≠ display order**: The `mru` field is a most-recently-used index list,
  a different axis from the tab-bar display order stored in `editors[]`.

## Anti-Patterns

| Anti-pattern | Why it's wrong | Correct alternative |
| --- | --- | --- |
| Treating the file-only projection (`--mode files`) as "the open tabs" | It omits webview and terminal tabs, so it never matches the visual tab bar when such tabs are present. | Use the default `--mode all`, which lists every tab with `[type]` tags and `# group` markers. |
| Using `memento/workbench.editors.files.textFileEditor` | Stores view-state *history* for all editors ever opened (including closed tabs), not just currently-open tabs. | Use `memento/workbench.parts.editor` → `serializedGrid` which holds the live editor-group state. |
| Treating `mru` as tab-bar order | `mru` is most-recently-used order, a different axis from display order. | Use the `editors[]` array order, which mirrors the tab bar left-to-right. |
| Looking for a per-editor `pinned` flag | VS Code does not serialize `pinned` per editor in `serializedGrid`. | Use the group-level `sticky: N` count — editors at index `< N` are pinned. |
| Opening the DB read-write | Risks corrupting the running window's state if VS Code is active. | The script opens `file:<path>?mode=ro` (read-only). |

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`vscode-active-window-editors`](../vscode-active-window-editors/SKILL.md) | Shells out to `scripts/extract-editors.py --db <resolved-path> [--mode <mode>] [--json]` after discovering the active window's `state.vscdb` on macOS. |

## Related Skills

- [`vscode-state-vscdb-merge`](../../../vscode-state-vscdb-merge/SKILL.md) —
  compares/merges `state.vscdb` across Git refs; complementary but does not
  extract editor tabs.

***

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Traceability

See [TRACEABILITY.md](TRACEABILITY.md).

***

<!-- Generated by the Skill Factory (skill-factory v1) -->
