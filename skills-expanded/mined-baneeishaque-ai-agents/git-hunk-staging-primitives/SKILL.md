---
name: git-hunk-staging-primitives
description: Generic Git hunk-staging primitives for commit construction and history refinement.
category: Git & Repository Management
---

# Git Hunk Staging Primitives

> **Skill ID:** `git-hunk-staging-primitives`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Provides domain-agnostic, deterministic Git primitives for staging file
content via `git update-index --cacheinfo` or `git apply --cached`. These
primitives isolate the mechanical work of constructing index blobs from
HEAD, working tree, or diff hunks — leaving the working tree untouched.

Every skill doing commit construction, history refinement, patch
manipulation, or submodule sync SHOULD compose these primitives rather
than re-implementing them.

## Environment & Dependencies

| Requirement | Minimum |
|---|---|
| Git | 2.x |
| Python | 3.12+ |

Verify:

```bash
git --version
python3 --version
```

## Scripts (Public CLI Contract)

All scripts are deterministic Tier-A primitives per
`script-over-instruction-decomposition`. They read from HEAD / working
tree / diff, write a new blob via `git hash-object -w` or apply a
filtered patch via `git apply --cached`, and never mutate the working
tree.

### 1. `agents-md-stage-row.py`

Stage exactly one AGENTS.md table row (alphabetically inserted) from
HEAD or working tree.

```bash
# Dry-run: preview alphabetical position
python3 scripts/agents-md-stage-row.py \
    --row "| My Skill | [path](path) | description |" \
    --dry-run

# Stage from working tree (skill-factory registration)
python3 scripts/agents-md-stage-row.py \
    --mode worktree \
    --row "| My Skill | [path](path) | description |"

# Stage from HEAD + one row (interleaving mandate)
python3 scripts/agents-md-stage-row.py \
    --row "| My Skill | [path](path) | description |"
```

**Modes:**

- `--mode worktree` (default for registration): reads working-tree
  AGENTS.md, inserts row, writes back to working tree for `git add`.
- `--mode staged` (default for interleaving): reads HEAD:AGENTS.md,
  inserts row, stages via `git update-index --cacheinfo`; working tree
  untouched.

### 2. `stage-file-excluding-lines.py`

Stage the working-tree version of a file MINUS lines matching
`--exclude` / `--exclude-regex`.

```bash
# Dry-run
python3 scripts/stage-file-excluding-lines.py \
    --file AGENTS.md \
    --exclude "deferred-skill" \
    --dry-run

# Stage working tree minus deferred cross-reference row
python3 scripts/stage-file-excluding-lines.py \
    --file .agents/skills/X/SKILL.md \
    --exclude "../Y/SKILL.md" \
    --blank-context 1
```

**Key behavior:** Reads CURRENT working-tree file, removes matching
lines, stages resulting blob via `git update-index --cacheinfo`.
Working tree is NEVER modified — deferred lines persist on disk for
later `git add`.

### 3. `stage-head-synthesize.py`

Stage HEAD version of a file with mechanical `--replace` /
`--regex-replace` substitutions.

```bash
# Dry-run
python3 scripts/stage-head-synthesize.py \
    --file .agents/skills/X/SKILL.md \
    --replace "old-path|new-path" \
    --dry-run

# Stage HEAD with literal replacement
python3 scripts/stage-head-synthesize.py \
    --file dev-env/SKILL.md \
    --replace "<private-config-repo>|<private-repo>"
```

**Key behavior:** Reads HEAD:`<file>`, applies substitutions in order,
stages resulting blob via `git update-index --cacheinfo`. Working
tree NEVER modified.

### 4. `stage-hunk-from-diff.py`

Stage ONLY hunks matching `--match` / `--match-regex` from the file's
diff (unstaged or staged).

```bash
# Dry-run
python3 scripts/stage-hunk-from-diff.py \
    --file SKILL.md \
    --match "Phase 1g" \
    --check

# Stage matching hunks from unstaged diff
python3 scripts/stage-hunk-from-diff.py \
    --file SKILL.md \
    --match "submodule" \
    --match "live editor"

# Stage from staged diff
python3 scripts/stage-hunk-from-diff.py \
    --file SKILL.md \
    --match "submodule" \
    --cached
```

**Key behavior:** Runs `git diff [--cached] -- <file>`, parses hunks,
keeps only those where ANY line matches the pattern, stages filtered
patch via `git apply --cached`. Working tree untouched.

### 5. `stage-specific-hunks.py`

Stage specific hunk indices (0-based) from the file's diff against
HEAD.

```bash
# Dry-run
python3 scripts/stage-specific-hunks.py \
    --file SKILL.md \
    --hunks 0 2 4 \
    --dry-run

# Stage hunks 0, 2, 4 from HEAD diff
python3 scripts/stage-specific-hunks.py \
    --file SKILL.md \
    --hunks 0 2 4
```

**Key behavior:** Runs `git diff HEAD -- <file>`, parses hunks,
selects by index, stages filtered patch via `git apply --cached`.
Working tree untouched.

---

## Complementary Primitives Table

| Script | Action | Input Source |
|---|---|---|
| `agents-md-stage-row.py` | Stage exactly one AGENTS.md row | HEAD or working tree |
| `stage-file-excluding-lines.py` | Stage file MINUS matching lines | Working tree |
| `stage-head-synthesize.py` | Stage HEAD with substitutions | HEAD |
| `stage-hunk-from-diff.py` | Stage ONLY matching hunks | Unstaged or staged diff |
| `stage-specific-hunks.py` | Stage ONLY specific hunk indices | HEAD diff |

---

## Safety

All scripts:

- Refuse to run outside a Git repository.
- Report replacement/stage counts to stderr for audit.
- Exit non-zero on zero matches (override with `--allow-empty-match`).
- Never modify the working tree — only the index.

---

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
|---|---|
| `git-atomic-commit-construction` | Invokes all 5 scripts via relative paths for commit-preview mandates (§2f.1, §3i, §3i.1, §13), deferred cross-references, adjacent-lines fallback, and HEAD-synthesis. |

---

## Related Skills

- `git-atomic-commit-construction` — Composer: orchestrates primitives for atomic commit workflows.
- `git-history-refinement` — Composer: uses primitives for commit splitting/refinement.
- `git-pre-execution-safety-stash` — Uses staging primitives for safety snapshots.
- `script-over-instruction-decomposition` — Mandates Tier-A extraction for all primitives.

---

## Source Rules

- `git-atomic-commit-construction-rules.md` (all phases)
- `git-operation-rules.md` (Phase 0, 1, sections 2–4)
- `script-over-instruction-decomposition` skill (Tier-A extraction mandate)

---

## Traceability

- Created: 2026-07-03
- Source: git-atomic-commit-construction §2f.1, §3i, §3i.1, §13 primitives extracted per Layered Composition Mandate.
