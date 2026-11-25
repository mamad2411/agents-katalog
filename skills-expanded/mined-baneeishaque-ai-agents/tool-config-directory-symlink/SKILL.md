---
name: tool-config-directory-symlink
description: >-
  Generic base skill for migrating any tool's configuration directories (XDG or
  otherwise) from native locations into a managed companion repository, with
  symlinks back from the original paths.
category: Tool-Infrastructure
---

# Tool Config Directory Symlink Protocol (v1)

This base skill owns the generic primitive for relocating one or more tool
configuration directories (config, state, data, cache) from their native
filesystem locations into a managed companion repo (typically
`<private-repo>`), replacing the originals with symlinks. It is
domain-agnostic — it knows nothing about specific tools, file tracking
policies, or recovery-value decisions.

***

## 1. Vocabulary

| Token | Meaning |
|---|---|
| `<source-dir>` | An existing native tool directory (e.g., `~/.config/opencode/`) |
| `<target-dir>` | The corresponding directory inside the companion repo (e.g., `<private-repo>/opencode/config/`) |
| `<private-repo>` | The git repository that will hold the migrated content (e.g., `<private-repo>`) |
| `<symlink-name>` | The path at `<source-dir>` that becomes a symlink pointing at `<target-dir>` |
| `mapping` | A JSON array of `{"source": "<path>", "target": "<path>"}` objects describing each dir to migrate |

***

## 2. Environment & Dependencies

- Python 3.12+ for the shipped scripts
- `diff` (POSIX) for post-copy integrity verification
- The target companion repo MUST exist and be writable

```bash
python3 --version && command -v diff
```

***

## 3. Input Contract

The base scripts accept a JSON mapping via stdin or a `--mapping-file <path>` argument:

```json
[
  {"source": "/path/to/.config/tool", "target": "/path/to/repo/tool/config"},
  {"source": "/path/to/.local/share/tool", "target": "/path/to/repo/tool/share"},
  {"source": "/path/to/.local/state/tool", "target": "/path/to/repo/tool/state"},
  {"source": "/path/to/.cache/tool", "target": "/path/to/repo/tool/cache"}
]
```

Each entry declares one directory to migrate. The source MUST exist; the
target's parent MUST exist (the script creates the target leaf directory).

***

## 4. Operational Logic

### 4.1 Phase 1 — Copy

For each mapping entry, copy all content from source to target recursively, preserving metadata:

```bash
cp -a "<source-dir>/." "<target-dir>/"
```

### 4.2 Phase 2 — Verify

Diff the source and target recursively. Any difference is a failure — abort before deletion:

```bash
diff -rq "<source-dir>/" "<target-dir>/"
```

### 4.3 Phase 3 — Replace with Symlink

If verification passes, remove the original and create the symlink:

```bash
rm -rf "<source-dir>"
ln -s "<target-dir>" "<source-dir>"
```

### 4.4 Phase 4 — Verify Symlink

Confirm the symlink resolves to the correct target:

```bash
readlink "<source-dir>"
```

The output MUST exactly match `<target-dir>`.

### 4.5 Phase 5 — (External) Selective .gitignore

The base does NOT define file tracking policy — that is the composer's
responsibility. The base ensures content is in the repo; the composer decides
what to track vs. ignore within that content.

***

## 5. Scripts

### 5.1 `scripts/migrate-and-symlink.py`

Executes Phases 1–4 for a mapping provided via stdin or `--mapping-file`.

**Usage:**

```bash
python3 scripts/migrate-and-symlink.py --mapping-file mappings.json
echo '[{"source": "...", "target": "..."}]' | python3 scripts/migrate-and-symlink.py
```

**Exit codes:** 0 on success, 1 if any phase fails (copy error, diff mismatch, symlink failure, or preflight source-not-found).

### 5.2 `scripts/verify-symlinks.py`

Walks a set of symlink paths (provided via stdin or `--symlinks-file`) and reports resolution status for each.

**Usage:**

```bash
printf "/path/to/symlink1\n/path/to/symlink2" | python3 scripts/verify-symlinks.py
```

**Exit codes:** 0 if all symlinks resolve, 1 if any link is broken or points to a non-existent target.

***

## 6. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
|---|---|
| [`opencode-config-preserve`](../opencode-config-preserve/SKILL.md) | Calls `scripts/migrate-and-symlink.py` with opencode's 4 XDG dir mapping; defines tracking policy externally via gitignore. |

***

## 7. Composition Rationale

This skill exists as a base because the copy-verify-symlink workflow is
identical across every tool that stores configuration in the filesystem
(opencode, VS Code, Claude, rclone, etc.). Extracting it here avoids
duplicating the migration mechanics in each tool-specific composer. Multiple
composers already invoke the same primitive; inlining into any single composer
would split the SSOT and silently diverge during bug fixes.

***

## 8. Related Skills

- [`dev-env-private-config-symlink`](../dev-env-private-config-symlink/SKILL.md)
  — The original symlink protocol for app-level `.env`/JSON configs; this base
  skill generalises the directory-level migration subset of that workflow.
- [`vscode-user-settings-symlink`](../vscode-user-settings-symlink/SKILL.md)
  — Concrete example of the same migration pattern for VS Code Insiders.
- [`mcp-cross-tool-config-sync`](../mcp-cross-tool-config-sync/SKILL.md) —
  Another config-symlink lifecycle, focused on MCP server definitions rather
  than tool XDG directories.
- [`opencode-config-preserve`](../opencode-config-preserve/SKILL.md)
  — Concrete example of the same migration pattern for OpenCode CLI/IDE.

***

## 9. Traceability

- Created: 2026-07-02
- Source: OpenCode config preservation session — generalised from the opencode XDG directory migration into `<private-repo>`.
