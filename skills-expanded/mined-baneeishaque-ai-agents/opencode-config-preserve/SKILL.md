---
name: opencode-config-preserve
description: >-
  Preserve and versionise OpenCode CLI/IDE configuration by migrating its XDG
  directories into <private-repo>, with selective gitignore tracking for
  recovery-critical state and session-versioning roadmap.
category: OpenCode-Configuration
---

# OpenCode Config Preserve Protocol (v1)

This composer skill defines the OpenCode-specific directory mapping,
file-tracking policy, and recovery-value decisions for preserving all four XDG
directories in a companion repo. It composes the generic copy-verify-symlink
flow from
[`tool-config-directory-symlink`](../tool-config-directory-symlink/SKILL.md).

***

## Composition Rationale

This skill is a composer: it does NOT re-implement the directory-migration
mechanics. It delegates the copy → verify → delete → symlink loop to the base
[`tool-config-directory-symlink`](../tool-config-directory-symlink/SKILL.md)
via `scripts/migrate-and-symlink.py`. The composer's value-add is:

1. **OpenCode-specific path mapping** — the 4 XDG directories and their repo counterparts.
2. **Selective gitignore tracking policy** — which files have config value, recovery value, or neither.
3. **Recovery-value documentation** — explaining why `log/`, `snapshot/`,
   `storage/`, `tool-output/` are tracked despite being transient.
4. **Session versioning roadmap** — future work for `opencode.db`.

Inlining these decisions into the base skill would couple a generic primitive to
a single tool's conventions. The base is domain-agnostic; this composer carries
the domain knowledge.

Bidirectional discoverability: the base lists this skill in its `## Composition by Higher-Level Skills` table.

***

## 0. Pre-flight

**Quit all opencode sessions before migrating.** The app writes to these
directories constantly during operation — copying while opencode is running can
produce incomplete or inconsistent state.

Check with:

```bash
ps aux | grep -i opencode
```

If opencode is running, quit it, then proceed.

***

## 1. Directory Mapping

OpenCode stores data across four XDG directories. Each maps to a subdirectory under `<private-repo>/opencode/`:

| XDG directory | Native path | Repo path |
|---|---|---|
| config | `<user-home>/.config/opencode/` | `<private-repo>/opencode/config/` |
| share (data) | `<user-home>/.local/share/opencode/` | `<private-repo>/opencode/share/` |
| state | `<user-home>/.local/state/opencode/` | `<private-repo>/opencode/state/` |
| cache | `<user-home>/.cache/opencode/` | `<private-repo>/opencode/cache/` |

***

## 2. Migration Workflow

### 2.1 Prepare the mapping

```json
[
  {"source": "<user-home>/.config/opencode", "target": "<private-repo>/opencode/config"},
  {"source": "<user-home>/.local/share/opencode", "target": "<private-repo>/opencode/share"},
  {"source": "<user-home>/.local/state/opencode", "target": "<private-repo>/opencode/state"},
  {"source": "<user-home>/.cache/opencode", "target": "<private-repo>/opencode/cache"}
]
```

### 2.2 Run migration

```bash
python3 .agents/skills/tool-config-directory-symlink/scripts/migrate-and-symlink.py \
  --mapping-file opencode-mapping.json
```

### 2.3 Verify symlinks

```bash
python3 .agents/skills/tool-config-directory-symlink/scripts/verify-symlinks.py <<EOF
<user-home>/.config/opencode
<user-home>/.local/share/opencode
<user-home>/.local/state/opencode
<user-home>/.cache/opencode
EOF
```

Each should resolve to `<private-repo>/opencode/<dir>`.

### 2.4 Commit

After symlinks are verified, stage and commit the migration:

```bash
git add opencode/
git commit -m "feat: preserve opencode XDG config in companion repo"
```

This captures the initial baseline. Subsequent changes to opencode
configuration will be visible as normal working-tree changes.

***

## 3. Selective Gitignore Tracking Policy

The root `.gitignore` of the companion repo uses a whitelist pattern: ignore
everything inside `opencode/` by default, then un-ignore only the files with
config or recovery value.

### 3.1 Config files — TRACKED

| File | Rationale |
|---|---|
| `opencode/config/opencode.json` | Primary configuration — all providers, models, permissions |
| `opencode/share/account.json` | Provider accounts + API keys (sensitive — private repo only) |
| `opencode/share/auth.json` | Auth credentials (sensitive — private repo only) |
| `opencode/state/kv.json` | UI/UX preferences — sidebar, thinking mode, timestamps |
| `opencode/state/model.json` | Model selection history and favorites |
| `opencode/state/prompt-history.jsonl` | User prompt history (personal but portable) |
| `opencode/state/session.json` | Pinned sessions |

### 3.2 Recovery directories — TRACKED

| Directory | Size (typical) | Recovery value |
|---|---|---|
| `opencode/share/log/` | ~6 MB | Timestamped app logs — first place to investigate crashes |
| `opencode/share/snapshot/` | ~125 MB | File snapshots at points in time; can recover content before modifications |
| `opencode/share/storage/` (including `session_diff/`) | ~284 KB | DB schema version + session diff JSONs for reconstructing session state if DB corrupts |
| `opencode/share/tool-output/` | ~888 KB | Cached tool call outputs, useful for audit/investigation |

These are tracked for forensic value. The tracking policy uses the
directory-level whitelist pattern (see §3.4) so all current and future content
inside them is versioned.

### 3.3 Ignored — NO tracking value

| File/Dir | Reason |
|---|---|
| `opencode/share/opencode.db` | 650+ MB SQLite database — too large for git; session versioning is a future effort (see §5) |
| `opencode/share/opencode.db-shm` | SQLite shared memory — pure runtime artifact, no standalone recovery value |
| `opencode/share/opencode.db-wal` | SQLite write-ahead log — transient, only meaningful paired with the matching `.db` |
| `opencode/share/repos/` | Empty directory placeholder |
| `opencode/state/frecency.jsonl` | File access frequency — machine-local, churns constantly, low recovery value |
| `opencode/state/locks/` | Empty directory placeholder |
| `opencode/cache/` | Downloaded npm packages (225 MB), cached model definitions, cache version marker — all regenerable |
| `opencode/config/package.json`, `package-lock.json`, `node_modules/` | Tool-managed plugin artifacts, not user configuration |
| `opencode/config/.gitignore` | OpenCode's own gitignore (ignores package.json/node_modules) — left in place |

### 3.4 Root `.gitignore` whitelist pattern

```gitignore
# --- opencode/ ---
opencode/*
!opencode/config/
!opencode/share/
!opencode/state/
!opencode/cache/

# opencode/config/ — only opencode.json
opencode/config/*
!opencode/config/opencode.json

# opencode/share/ — account/auth + recovery dirs
opencode/share/*
!opencode/share/account.json
!opencode/share/auth.json
!opencode/share/log/
!opencode/share/snapshot/
!opencode/share/storage/
!opencode/share/tool-output/

# opencode/state/ — tracked files only
opencode/state/*
!opencode/state/kv.json
!opencode/state/model.json
!opencode/state/prompt-history.jsonl
!opencode/state/session.json

# opencode/cache/ — entirely ignored
opencode/cache/**
```

***

## 4. Recovery Value: SHM & WAL Explained

`opencode.db-shm` and `opencode.db-wal` are SQLite Write-Ahead Log internals:

- **`.db-wal`** — recent uncheckpointed transactions. If the DB crashes without
  checkpointing, the WAL contains the latest writes. Must be paired with the
  matching `.db` file — you cannot use a WAL standalone.
- **`.db-shm`** — shared memory index for coordinating WAL access across processes. Pure runtime; zero recovery value.

Neither is worth tracking standalone. They are included only as a consistency
pair if the `.db` itself is ever versioned (see §5).

***

## 5. Session Versioning (Roadmap)

The `opencode.db` SQLite database contains all conversations, sessions, and file
state (~650 MB). It is too large for conventional git tracking. Future
approaches to consider:

- **Git LFS** — offload the `.db` binary to LFS storage while keeping a pointer
  in the repo.
- **Periodic exports** — use opencode's session export feature to dump
  conversations as markdown, then version those instead of the raw DB.
- **`opencode.db-wal` consistency pairs** — if checkpointing discipline is
  established, the `.db` + `.db-wal` pair could be treated as a unit.

This section is a placeholder; the optimal strategy depends on session volume and recovery requirements.

***

## 6. Related Skills

- [`opencode-jsonc-util`](../opencode-jsonc-util/SKILL.md) — Base JSONC utility for OpenCode config files
- [`tool-config-directory-symlink`](../tool-config-directory-symlink/SKILL.md)
  — Base skill for the generic copy-verify-symlink migration primitive.
- [`opencode-permission-config`](../opencode-permission-config/SKILL.md) —
  Configures opencode's permission system within `opencode.json`.
- [`opencode-provider-persistence-config`](../opencode-provider-persistence-config/SKILL.md)
  — Manages provider API key persistence in `auth.json`.
- [`opencode-google-gemini-config`](../opencode-google-gemini-config/SKILL.md)
  — Google Gemini model configuration (composer of the provider-persistence
  base).
- [`vscode-user-settings-symlink`](../vscode-user-settings-symlink/SKILL.md) —
  Analogous config migration for VS Code Insiders.
- [`opencode-installed-plugin-lookup`](../opencode/opencode-installed-plugin-lookup/SKILL.md)
  — related — read-only plugin registry probe for the preserved config.
- [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
  — Staging and atomic-commit protocol used during the migration.
- [`dev-env-private-config-symlink`](../dev-env-private-config-symlink/SKILL.md)
  — General symlink protocol for app-level configs.

***

## 7. Traceability

- Created: 2026-07-02
- Source conversation: OpenCode XDG directory migration into
  `<private-repo>`, including file-by-file tracking analysis,
  recovery-value assessment, and SHM/WAL explanation.
