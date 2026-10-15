---
name: claude-symlink-agent-individual-skills
description: Mirror each individual skill under `.agents/skills/<name>/` into a `.claude/skills/<name>` relative symlink so Claude Code's harness auto-discovers it — but only for skills that don't already have a correct link. Idempotent and non-destructive — existing correct symlinks pass, wrong symlinks are flagged as conflicts (or replaced with --force), and real files/directories are never clobbered. Uses a zero-dependency native script (Node .mjs or Python 3). Use when a SKILL.md under .agents/skills/ is invisible to the harness, when bulk-onboarding a repo that adopts the `.agents/` convention, or after pulling new skills into `.agents/skills/`.
tier: project
---

# Claude Symlink Agent Individual Skills

Claude Code's harness auto-discovers skills under `.claude/skills/`. Skills authored or
vendored under `.agents/skills/<name>/SKILL.md` are invisible to it until each one is
linked into `.claude/skills/`. This skill creates exactly those missing links.

For every directory `.agents/skills/<name>/` that contains a `SKILL.md`, it ensures a
**relative** symlink exists at `.claude/skills/<name>` →  `../../.agents/skills/<name>`.
The link is relative on purpose: it stays valid no matter where the repo is checked out,
and never bakes a host-specific absolute path into the tree.

## Core behavior

The operation is a *diff-and-fill*, never a sync that deletes:

| Situation at `.claude/skills/<name>` | Result |
|--------------------------------------|--------|
| Nothing there | **CREATE** the relative symlink |
| Correct symlink already present | **PASS** — left untouched (idempotent) |
| Symlink pointing somewhere else | **CONFLICT** — reported; replaced only with `--force` |
| A real file or directory | **CONFLICT** — never clobbered, even with `--force` |

Exit code is `0` when nothing is left unresolved, `1` when any CONFLICT remains.

## How to run

Both implementations are byte-for-byte equivalent in behavior — pick whichever runtime
is handy. They are native / standard-library only (no `npm install`, no `pip install`).
They prefer `git rev-parse --show-toplevel` for the repo root, falling back to `$PWD`.

```bash
# Node (zero deps)
node .agents/skills/claude-symlink-agent-individual-skills/bin/link-skills.mjs

# Python 3 (zero deps)
python3 .agents/skills/claude-symlink-agent-individual-skills/bin/link_skills.py
```

### Recommended workflow

1. **Preview first** with `--dry-run` — confirm the CREATE/CONFLICT verdicts:
   ```bash
   node .../bin/link-skills.mjs --dry-run
   ```
2. **Apply** by re-running without `--dry-run`.
3. If a `CONFLICT` is a stale/wrong symlink you want corrected, re-run with `--force`
   (this replaces wrong **symlinks** only — it will still refuse to delete a real
   directory or file).

### Flags

| Flag | Effect |
|------|--------|
| `[root]` | Operate on a specific repo root instead of the detected one |
| `--dry-run` | Report verdicts; create/replace nothing |
| `--force` | Replace a wrong-target symlink (never a real path) |
| `--json` | Emit a machine-readable report (for CI / piping) |
| `--quiet` | Print only the summary line |

## Safety guarantees

- **Never deletes a real file or directory.** A non-symlink occupant is always a
  CONFLICT, even under `--force`.
- **Only ever removes a symlink** when `--force` is set and it points at the wrong target.
- **Relative links only** — no absolute, host-specific paths written into the repo.
- **Idempotent** — running repeatedly converges and reports already-correct links as PASS.

## GitHub operations

When this skill's work needs to be committed, branched, or turned into a PR/issue, use
the **`gh` CLI** (`gh pr create`, `gh issue create`) rather than any MCP GitHub tool.

## Relationship to other skills

This is the project-local, self-hosted variant for this repo (it links its own
`agent-skill-kit-*` skills). The user-global equivalent is the `agentskills-mirror-to-claude`
skill, which applies the same `.agents/skills → .claude/skills` mirroring at `$HOME` scope.
