---
name: git-ref-artifact-extract
description: >-
  Composer — capture a file at any git ref (HEAD, branch, tag, or stash commit)
  into the session-scoped scratch folder with the
  `<purpose>_<ref-slug>_<full-sha>` naming scheme. Composes
  scratch-artifact-naming for path+name resolution and repo-scratch-output-capture
  for the underlying capture doctrine.
category: Git-Audit
---

# Git Ref Artifact Extract (v1)

> **Skill ID:** `git-ref-artifact-extract`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer

## Scope & Intent

**In scope:**
- Capture a single file exactly as it exists at any git ref — `HEAD`, a branch,
  a tag, or a stash commit — into the session-scoped scratch folder.
- Use the confirmed git-ref naming scheme `<purpose>_<ref-slug>_<full-sha>`
  (no timestamp — the full SHA is the unique discriminator).
- Derive the ref slug deterministically: for a stash ref, the stash subject up
  to the first colon (e.g. `WIP on stash/changes-on-macOS` →
  `wip-on-stash-changes-on-macos`); otherwise the ref string itself, lower-case
  kebab.
- Verify the written artifact byte-for-byte against
  `git cat-file -s <ref>:<path>` before reporting success.

**Out of scope:**
- The naming/session-folder formula itself — owned by
  [`scratch-artifact-naming`](../general/file/scratch-artifact-naming/SKILL.md);
  this script delegates to its `resolve-scratch-path.py`.
- The `.out`/`.err` pairing and generic output capture — owned by
  [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md).
- Applying or making commits from the captured ref (read-only extraction).

## Environment & Dependencies

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.12+ | Stdlib only — no pip dependencies |
| Git | any | `git rev-parse`, `git cat-file -s`, `git show`, `git stash list` |
| `scratch-artifact-naming` | present | Resolved from this script's parent dirs (same repo) |

## CLI Contract

```text
python3 scripts/extract-ref-artifact.py --repo <path> --ref <rev> --path <file>
    --purpose <slug> [--session-id <id>] [--force]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--repo <path>` | Yes | Repo root (relative or absolute) |
| `--ref <rev>` | Yes | `HEAD`, `stash@{N}`, branch, tag, or commit SHA |
| `--path <file>` | Yes | File path inside the repo (repo-root relative) |
| `--purpose <slug>` | Yes | Lower-case-kebab purpose slug |
| `--session-id <id>` | No | Passthrough to scratch-artifact-naming (auto when omitted) |
| `--force` | No | Overwrite an existing artifact |

**Output:** `<abs-path> | <full-sha> | <ref-slug>` on stdout.

**Exit codes:**
- `0` — success (artifact written and byte-verified)
- `1` — not a git repo / unresolvable ref / file missing at ref / artifact exists /
  byte-count mismatch
- `2` — argparse usage error

## Protocol

1. Pick the repo, ref, in-repo file path, and a purpose slug.
2. Run
   `python3 .agents/skills/git-ref-artifact-extract/scripts/extract-ref-artifact.py
   --repo <repo> --ref <rev> --path <file> --purpose <slug>`.
3. Confirm the printed path under `<repo>/scratch/<session-id>/` and the byte verify.

## Edge Cases

- **Duplicate artifact**: re-running the same purpose+ref on the same session
  overwrites only with `--force`; otherwise exits 1.
- **Stash with no ref-slug-able subject**: an empty/structured subject
  degrades to the raw `stash@{N}` string lower-cased.
- **Non-UTF8 file content**: captured as bytes (`git show` binary-safe) and
  byte-verified; no text decoding performed.
- **`ses_` prefixed session**: passed through to scratch-artifact-naming which
  strips the prefix for the folder name.

## Prohibited Actions

- Do NOT re-derive the `<purpose>_<ref-slug>_<sha>` formula in a caller —
  delegate via `--purpose` + this script.
- Do NOT write the timestamp variant; ref captures must carry the full SHA.
- Do NOT capture into `scratch/` root or `/tmp` — always the session folder.

## Script Reference

`extract-ref-artifact.py`:
1. Verifies the repo root has `.git`.
2. `git rev-parse --verify <ref>^{commit}` → full 40-hex SHA.
3. `git stash list --format=%H|%gs` → pre-colon subject lower-kebab slug
   (fallback: raw ref lower-cased).
4. Compose to `scratch-artifact-naming/resolve-scratch-path.py`
   with `--ref-name --ref-sha`.
5. `git cat-file -s <ref>:<path>` → expected byte count; refuse overwrite
   without `--force`.
6. `git show <ref>:<path>` (binary) → write; compare size; print
   `<path> | <sha> | <slug>`.

## Composition by Higher-Level Skills

This composer sits at the top of the scratch-export layer and is itself a leaf
workflow — no higher skill composes it yet.

## Related Skills

- [`scratch-artifact-naming`](../general/file/scratch-artifact-naming/SKILL.md) — the base it composes for path+name resolution.
- [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md) — sibling base; owns the `.out`/`.err` capture doctrine for the same session-scoped tree.
- [`git-commit-metadata-extraction`](../git-commit-metadata-extraction/SKILL.md) — adjacent git-ref plumbing primitive.
