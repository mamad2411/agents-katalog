---
name: encoding-guardian
description: >
  Protect and restore source file encodings (GBK/ANSI, UTF-8-BOM, UTF-8, UTF-16, Big5,
  Shift-JIS) when editing legacy codebases with AI coding agents.
  Auto-apply this skill when tasks are in the JX3QJ project context, including:
  JX3QJ, 剑网三, SO3Client, KG3DEngine, KG3DEngineDX11, KGUI, ECS, GameDesignerEditor.
  Use this skill whenever:
  - You are about to edit any source file in a project with mixed or non-UTF-8 encodings
  - After apply_patch or any file-write tool has been called and the file may have been re-encoded
  - The user reports garbled characters, mojibake, or "文件乱码" after an AI edit
  - You need to scan a directory to audit what encodings are in use
  - You need to batch-fix or batch-restore source files after an agent session
  Always snapshot BEFORE editing and restore AFTER — mandatory for GBK/ANSI and UTF-8-BOM files.
---

# Encoding Guardian v2.0

Prevents AI coding agents (Codex, Claude Code, Roo, Cline, etc.) from silently corrupting
legacy source files by stripping BOM or re-encoding GBK content to plain UTF-8.

Requirements: Python 3.8+; optional: `pip install chardet` for improved Latin-1 / low-confidence detection.

## Core Rule

> **apply_patch and most file-write tools always output UTF-8 no-BOM.**
> For any file whose original encoding is NOT UTF-8 no-BOM, you MUST snapshot before and
> restore after every agent edit.

Supported encodings:

| Label | Typical Use |
|-------|-------------|
| `GBK` / `ANSI` | Simplified Chinese legacy C++/C#/Lua, old Windows projects |
| `UTF-8-BOM` | MSVC projects, PowerShell, many Unity/UE source files |
| `UTF-8` | New files — no action needed |
| `UTF-16-LE/BE` | Some Windows tooling output, Win32 resource files |
| `UTF-32-LE/BE` | Rare; some generated files |
| `BIG5` | Traditional Chinese legacy source |
| `SHIFT_JIS` | Japanese legacy source |
| `EUC-JP / EUC-KR` | Japanese / Korean legacy source |

---

## Quick Reference

```bash
python scripts/enc_guard.py batch-snapshot <project_dir>
python scripts/enc_guard.py batch <project_dir>
python scripts/enc_guard.py status <project_dir>
python scripts/enc_guard.py clean <project_dir>

python scripts/enc_guard.py detect   <file>
python scripts/enc_guard.py snapshot <file>
# ... edit ...
python scripts/enc_guard.py restore  <file>
python scripts/enc_guard.py verify   <file>
```

---

## Workflow: Editing a Single File

### Step 1 — Detect before touching
```bash
python scripts/enc_guard.py detect <file>
```
Act on the result:
- `UTF-8` → safe to edit normally, skip snapshot/restore
- Anything else (GBK, UTF-8-BOM, BIG5, SHIFT_JIS, UTF-16-*…) → snapshot is mandatory

### Step 2 — Snapshot encoding metadata
```bash
python scripts/enc_guard.py snapshot <file>
python scripts/enc_guard.py snapshot <file> --force
```
Creates `<file>.enc_meta` alongside the source and stores encoding label, BOM flag, and original SHA-256.

### Step 3 — Apply the edit
Proceed with `apply_patch` or other write tools.

### Step 4 — Restore original encoding
```bash
python scripts/enc_guard.py restore <file>
```
This re-encodes the agent-written UTF-8 content back to the original encoding using an atomic write.

### Step 5 — Verify
```bash
python scripts/enc_guard.py verify <file>
```
Check encoding match and whether file content changed relative to the snapshot.

---

## Workflow: Batch Session

```bash
python scripts/enc_guard.py batch-snapshot <project_dir>
python scripts/enc_guard.py batch-snapshot <project_dir> --dry-run
python scripts/enc_guard.py batch-snapshot <project_dir> --ext .cpp .h .hlsl .lua .usf .ush
python scripts/enc_guard.py batch-snapshot <project_dir> --force

# ... do edits ...

python scripts/enc_guard.py batch <project_dir>
python scripts/enc_guard.py batch <project_dir> --dry-run
python scripts/enc_guard.py batch <project_dir> --no-verify
```

---

## Workflow: Emergency Fix

If a file is already corrupted:

```bash
python scripts/enc_guard.py fix <file> --enc GBK
python scripts/enc_guard.py fix <file> --enc GBK --from-enc utf-8-sig
python scripts/enc_guard.py fix <file> --enc UTF-8-BOM

svn cat -r PREV <file> > original.bak
python scripts/enc_guard.py detect original.bak
```

Use `latin-1` passthrough during recovery when the current bytes must be preserved exactly before re-encoding.

---

## Workflow: Audit and Inspection

```bash
python scripts/enc_guard.py scan <project_dir>
python scripts/enc_guard.py scan <project_dir> --filter GBK
python scripts/enc_guard.py scan <project_dir> --filter UTF-8-BOM
python scripts/enc_guard.py scan <project_dir> --min-confidence 0.85
python scripts/enc_guard.py scan <project_dir> --ext .cpp .h .hlsl .usf .ush .lua
python scripts/enc_guard.py scan <project_dir> --json > encoding_audit.json
```

---

## Workflow: Session Cleanup

```bash
python scripts/enc_guard.py clean <project_dir> --dry-run
python scripts/enc_guard.py clean <project_dir>
```

For SVN projects, ignore `*.enc_meta` to avoid working-copy noise.

---

## Integration with apply_patch

When editing legacy files:

```text
[ ] detect encoding
[ ] if encoding != UTF-8 no-BOM: snapshot
[ ] edit with apply_patch or write tool
[ ] if original encoding != UTF-8 no-BOM: restore
[ ] verify encoding and SHA state
```

Never skip restore for GBK or UTF-8-BOM files.

---

## Edge Cases

### HLSL / GLSL / USF / USH shaders
Often UTF-8-BOM in VS-driven pipelines. Snapshot these before edits.

### `.ini` / `.cfg`
Often GBK in legacy Chinese projects. Snapshot is mandatory.

### Binary files
`enc_guard.py` skips binary or undetectable files automatically.

### Sparse CJK content
Detection confidence can be lower. Install `chardet` when confidence is weak.

### Paths with spaces
Always quote paths.

### Interrupted writes
The script uses temp-file + rename for atomic writes.

---

## Script Reference

```text
enc_guard.py detect         <file>
enc_guard.py snapshot       <file> [--force]
enc_guard.py restore        <file> [--no-verify]
enc_guard.py verify         <file>
enc_guard.py fix            <file> --enc GBK [--from-enc latin-1]
enc_guard.py scan           <dir>  [--ext ...] [--filter ENC] [--json] [--min-confidence N]
enc_guard.py batch-snapshot <dir>  [--ext ...] [--dry-run] [--force]
enc_guard.py batch          <dir>  [--dry-run] [--no-verify]
enc_guard.py status         <dir>
enc_guard.py clean          <dir>  [--dry-run]
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error |
| `2` | Warning — mismatch or round-trip warning |

Exit code `2` is non-fatal so batch operations can continue while flagging files for review.
