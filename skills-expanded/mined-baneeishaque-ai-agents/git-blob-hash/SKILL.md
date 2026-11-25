---
name: git-blob-hash
description: >-
  Base skill that computes the git blob SHA-1 (sha1 of "blob <len>\0<content>
  ") for one or more files. This is identical to the Software Heritage `cnt`
  object identifier, so output can be embedded directly in SWH content links.
  Domain-agnostic — reusable by any workflow that needs git-compatible blob
  hashes from a local working tree.
category: General-File
---

# Git Blob Hash Skill (v1)

This is a **base** skill. It computes git blob SHA-1 identifiers (`sha1("blob <len>\0<content>")`)
for files on disk. The output is byte-identical to `git hash-object` and to the
Software Heritage `cnt` object identifier, enabling direct embedding into SWH
browse links without a `git` binary dependency.

***

## 1. Scope & Intent

- **In scope**:
    - Compute git blob SHA-1 for individual files (raw bytes, CRLF-preserving)
    - Compute git blob SHA-1 for all files matched by a glob pattern under a root
    - Output one `<sha>\t<path>` pair per line (tab-separated, path quoted-safe)
    - Optional JSON output (`--json`) with `{"path":..., "sha1":...}` per item
    - Optional `--verify` against a known hash for pre-confirmation
- **Out of scope**:
    - Git tree/directory hashing (use `git write-tree` + `git ls-tree`)
    - Revision/snapshot/swhid assembly (delegated to `swh-content-link-mint`)
    - Network/ingestion checking (delegated to `content-ingestion-check`)

***

## 2. Environment & Dependencies

### 2.1 Runtime
- **Python 3.12+** (Tier 1 per scripting-language-selection-rules)
- No third-party dependencies.

### 2.2 Required Setup
None — pure stdlib (`hashlib`, `glob`, `os.path`, `json`, `argparse`).

### 2.3 Required Skill Loading
The agent MUST load `SKILL.md` before invoking the script.

***

## 3. Protocol

### 3.1 Step 1 — Run Hash Script

```bash
python3 .agents/skills/general/file/git-blob-hash/scripts/compute-blob-sha1.py <file>...
python3 .agents/skills/general/file/git-blob-hash/scripts/compute-blob-sha1.py --glob "src/**/*.py"
python3 .agents/skills/general/file/git-blob-hash/scripts/compute-blob-sha1.py --json docs/
```

### 3.2 Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `<file>...` | One of `<file>` or `--glob` | — | One or more file paths to hash |
| `--glob <pattern>` | No | — | Glob pattern relative to `--root` |
| `--root <dir>` | No | `.` | Root for glob resolution; also prefixes output paths |
| `--json` | No | false | Output JSON array instead of TSV |
| `--verify <sha>,<file>` | No | — | Assert file's blob hash matches; exit 1 on mismatch |

### 3.3 Output Contract

- **stdout** (TSV mode): `<sha1_git>\t<relative-path>` per line
- **stdout** (JSON mode): `[{"path": "...", "sha1": "..."}]`
- **Exit 0**: All hashes computed (and all `--verify` assertions passed)
- **Exit 1**: Any `--verify` assertion failed, or a file could not be read
- **Exit 2**: Argument error

### 3.4 Script

| Script | Language | Purpose |
|--------|----------|---------|
| [`scripts/compute-blob-sha1.py`](scripts/compute-blob-sha1.py) | Python | Core engine: reads files as raw bytes, applies git blob header |

***

## 4. Edge Cases

- **CRLF files**: Hashed as-is (raw bytes). Git's `hash-object` also preserves line endings as stored; if the file has CRLF and the index has `core.autocrlf`, the working-tree hash may differ from the index hash — this script hashes working-tree bytes only.
- **Empty file**: Hash is `sha1("blob 0\0")` = `e69de29bb2d1d6434b8a4f3e0e7ad23c0d2c5d4c`.
- **Symlinks**: Hashed as the link target's bytes (git stores symlinks as blob objects containing the target path text).
- **Glob with no matches**: Exit 1 with a stderr notice.

***

## 5. Composition Rationale

This skill is a **base** primitive: git blob hashing is needed by any workflow
that must reference content by its immutable identifier (SWH `cnt` links,
gitobject verification, content-addressable storage, diff tools). It is
intentionally domain-agnostic, accepting only file paths and a glob pattern.

***

## 6. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
|----------------|----------------------|
| [`swh-content-link-mint`](../../software-heritage/content-link-mint/SKILL.md) | Delegates blob hashing to `git-blob-hash`'s `compute-blob-sha1.py`, then assembles ;origin= ;path= ;lines= qualifiers |

***

## 7. Verification

```bash
python3 scripts/compute-blob-sha1.py --verify \
  "$(\python3 scripts/compute-blob-sha1.py --json README.md | python3 -c 'import sys,json; print(json.load(sys.stdin)[0]["sha1"])')", \
  README.md
# Known SWH GPL3 license blob (from docs): sha1 94a9ed024d3859793618152ea559a168bbcbb5e2
```
