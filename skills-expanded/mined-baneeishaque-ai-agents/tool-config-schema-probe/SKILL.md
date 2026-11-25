---
name: tool-config-schema-probe
description: Discover the on-disk JSON config file path and exact schema shape used by an opaque AI tool (or any
    GUI/TUI application) by writing a sentinel "dummy" entry through the tool's own UI, then inspecting the resulting
    file system change.
category: Tool-Infrastructure
---

# Tool Config Schema Probe Skill (v1)

This is a **base primitive** for reverse-engineering the configuration file format of any tool that:

- Persists user-editable settings to disk in some structured format (JSON / TOML / YAML / XML).
- Exposes a UI command to add an entry (e.g., a slash command in a TUI, a "+" button in a GUI, a wizard).
- Has unclear, undocumented, or out-of-date public documentation about the on-disk file path or schema.

Instead of guessing the schema, you let the tool **show you** by writing a sentinel entry, then comparing the
filesystem before and after.

## 1. When to Apply

Apply this skill when:

- A tool's config file location is undocumented or differs across versions.
- A tool's config schema (top-level key names, value shape) is undocumented.
- The tool has multiple plausible config locations (XDG vs. macOS Application Support vs. legacy dotfile).
- You need to confirm whether two surfaces of the same tool (CLI vs. GUI vs. IDE plugin) share a config file or
    keep separate ones.

Do NOT apply when:

- Official, version-matched documentation already specifies the path AND schema (just read the docs).
- The tool stores config in a binary blob or proprietary format that text-diff can't analyze.
- You don't have permission or UI access to add an entry interactively.

## 2. Operational Logic

### 2.1 Phase 0 — Pre-Probe Snapshot

Before touching the tool, capture the candidate filesystem state so you have a reliable baseline to diff against.

1. **Enumerate candidate roots** for the tool's config (POSIX examples — adapt for Windows):

    | Root | Pattern |
    | :--- | :--- |
    | XDG | `<user-home>/.config/<tool-name>/` |
    | macOS | `<user-home>/Library/Application Support/<tool-name>/` |
    | macOS (Electron) | `<user-home>/Library/Application Support/<vendor>/<tool-name>/` |
    | Legacy dotfile | `<user-home>/.<tool-name>/` or `<user-home>/.<tool-name>rc` |
    | Vendor-shared | `<user-home>/.config/<vendor>/<tool-name>/` |
    | Windows | `%APPDATA%\<vendor>\<tool-name>\` |

2. **Snapshot file lists + mtimes** at each candidate root (use whichever pre-exists):

    ```bash
    for d in \
        "<user-home>/.config/<tool-name>" \
        "<user-home>/Library/Application Support/<tool-name>" \
        "<user-home>/.<tool-name>"; do
        [ -d "$d" ] && find "$d" -type f -printf '%T@ %p\n' 2>/dev/null
    done | sort > /tmp/probe-before.txt
    ```

3. **Pick a sentinel name** that is unmistakably synthetic and trivially greppable, e.g.:
    - `probe-dummy-DELETE-ME`
    - `zzz-schema-probe`
    - Avoid names that collide with real entries the tool may auto-generate.

### 2.2 Phase 1 — Write Through the Tool's Own UI

The cardinal rule: **do not hand-edit any file you suspect**. Use the tool's UI to write, so the tool itself
chooses the path, schema, and serialization format.

Common UI paths to add an entry, by surface family:

| Tool family | UI invocation pattern |
| :--- | :--- |
| TUI / CLI with slash commands | `/mcp`, `/server add`, `/config add` (GitHub Copilot CLI, Claude Code, etc.) |
| IDE plugin | Settings → Tools → "Add server", or right-click context menu in a sidebar |
| Electron GUI | Preferences pane → "+" button under a list |
| Web UI | Account / workspace settings page |

When the UI prompts for fields, supply **structurally minimal but syntactically valid** values:

- Server / endpoint name → the sentinel from §2.1.3.
- URL / command → a known-bogus value that the tool will accept syntactically (e.g., `echo`, `http://localhost:1`).
- Auth token / env var → empty string or `"x"` if required.

The goal is for the tool to **persist** the entry, not for it to actually function.

### 2.3 Phase 2 — Post-Probe Diff

1. **Re-snapshot** with the same `find` command into `/tmp/probe-after.txt`.
2. **Diff**: `diff /tmp/probe-before.txt /tmp/probe-after.txt` shows new files and changed mtimes.
3. **Grep for the sentinel** across all candidate roots:

    ```bash
    grep -rEln "probe-dummy-DELETE-ME" \
        "<user-home>/.config" \
        "<user-home>/Library/Application Support" \
        "<user-home>" 2>/dev/null
    ```

4. The hit identifies the **canonical file path**. The file's content reveals the **canonical schema**:
    - Top-level key (`mcpServers`, `servers`, `context_servers`, etc.).
    - Per-entry shape (`type`, `command`, `args`, `env`, custom fields like `tools` or `transport`).
    - Sibling top-level keys the tool also supports (`inputs`, `theme`, etc.).
    - Whether the tool wrote comments (most JSON tools strip them; some preserve `//`).

### 2.4 Phase 3 — Cleanup

The sentinel entry MUST NOT be left behind. Two safe paths:

1. **Preferred**: use the same UI that created it to remove it (e.g., `/mcp remove probe-dummy-DELETE-ME`).
    The tool then re-serializes the file and you confirm a clean schema.
2. **Fallback**: now that the schema is known, edit the file directly (or `jq` it) to remove the sentinel,
    then trigger a tool reload to confirm the file is still accepted.

### 2.5 Phase 4 — Document the Findings

Persist what you learned so future probes are not needed for the same tool/version. Recommended record fields:

| Field | Example |
| :--- | :--- |
| Tool name + version | `GitHub Copilot CLI v0.0.339` |
| OS | `macOS 14.x` |
| Canonical path | `<user-home>/.copilot/mcp-config.json` |
| Top-level key | `mcpServers` |
| Per-entry required fields | `type`, `command`, `args` |
| Per-entry tool-specific fields | `tools: ["*"]` (access control) |
| Sibling top-level keys | none |
| Reload behavior | re-read on every CLI launch (no restart needed) |
| Source (UI command used) | `/mcp` slash command |

Store the record in the consuming skill's documentation so the probe is a one-time cost per tool.

***

## 3. Failure Modes

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| Diff is empty after UI write | Tool buffered in memory; never wrote | Trigger an action that forces flush (close panel, restart tool, send a message) |
| Sentinel found in multiple files | Tool maintains workspace + global config | Distinguish by inspecting full content of each match; pick the one matching the UI scope you used |
| Tool refuses sentinel | Validation rejects bogus URL/command | Supply a more realistic but still-bogus value (e.g., `http://localhost:65535`) |
| Tool writes to a temp file you can't catch | Atomic-rename pattern — re-snapshot AFTER a few seconds | Re-run §2.3 with a longer delay; or use `fswatch`/`inotifywait` |
| Unicode / encoding looks corrupt | Tool uses UTF-16 BOM or non-UTF-8 | Use `file <path>` to detect, then read with the correct encoding |

***

## 4. Prohibited Behaviors

- **DO NOT** hand-edit any candidate config file before probing — it pollutes the diff and can break the tool.
- **DO NOT** leave the sentinel entry in place — it's noise at best, a foothold at worst.
- **DO NOT** publish probe records that include real user paths — apply
    [Redaction & Portability](../redaction-portability/SKILL.md) before committing.
- **DO NOT** assume the path you find is the same on Windows / Linux — the probe is per-OS.
- **DO NOT** assume two surfaces of the same vendor share a file (e.g., Copilot CLI vs. VS Code Copilot use
    different files and different schemas — confirm with separate probes).

***

## 5. Composition by Higher-Level Skills

Consumers that need to know a tool's config path/schema MUST delegate to this skill rather than re-probing
ad hoc. Known consumers:

- [MCP Cross-Tool Config Sync](../mcp-cross-tool-config-sync/SKILL.md) — uses the probe to find each AI tool's
    MCP config path and schema before generating + symlinking.

***

## 6. Related Skills

- [Folder Comparison](../folder-comparison/SKILL.md) — for richer pre/post diffs across multiple candidate roots.
- [Redaction & Portability](../redaction-portability/SKILL.md) — required before publishing probe records.
- [System-Wide Tool Management](../system-wide-tool-management/SKILL.md) — verify `find`, `grep`, `diff`, `jq`,
    `file` are present.
