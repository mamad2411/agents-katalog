---
name: git-submodule-selective-init-no-lfs
description: Provides coupled guarantees for initializing Git submodules selectively while excluding LFS.
category: Git-Operations
---

# Git Submodule Selective Init (No-LFS) Skill (v1)

> **Skill ID:** `git-submodule-selective-init-no-lfs`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Two coupled guarantees, both first-class to this skill:

1. **Selective scope** — initialize **exactly** the submodule paths the user names; no `--recursive`, no transitive init, other submodules stay uninitialized (`-` prefix in `git submodule status`).
2. **No-LFS contract** — guarantee zero LFS object bytes are fetched during the checkout by applying ALL of: `GIT_LFS_SKIP_SMUDGE=1` in the child env, plus inline `-c filter.lfs.smudge=` / `-c filter.lfs.process=` / `-c filter.lfs.required=false` overrides (the env var alone is insufficient when the submodule's own `.gitattributes` declares LFS filters).

Post-state is verified for **both** guarantees: each named path is checked out (no `-` prefix); `.git/modules/<path>/lfs/objects` is empty or absent.

This is the per-path, LFS-skipped counterpart to [`git-lfs-selective-clone`](../git-lfs-selective-clone/SKILL.md) — which handles the *clone-time* LFS skip but mandates `--recursive` for ALL submodules at init time. Use **this** skill when only a subset is wanted AND the LFS-free property must be preserved through init.

## Composition Rationale

Atomic primitive owning the (per-path + no-LFS) coupling. Composed by:

| Composer Skill | Used for |
|---|---|
| [`git-lfs-selective-clone`](../git-lfs-selective-clone/SKILL.md) §3b | Per-path init after the LFS-skipped clone, when the user does not want the full `--recursive` walk |
| [`git-submodule-misconfiguration-audit-and-revert`](../git-submodule-misconfiguration-audit-and-revert/SKILL.md) Phase 1 prerequisite | Materialize the submodule before auditing its URL / divergence |

## Related Skills

- [`git-submodule-uninitialized-handler`](../git-submodule-uninitialized-handler/SKILL.md) — the recursive-sweep remediation half of an audit/handler pair: consumes an audit report and drives every uninitialized pointer in the tree to a terminal state (Initialized / Recovered-via-Fork / Removed). Reach for it when you want a full-tree sweep off an audit; reach for **this** skill when you have a specific user-named subset to initialize directly.
- [`git-submodule-uninitialized-audit`](../git-submodule-uninitialized-audit/SKILL.md) — the audit half that produces the report the handler above consumes; not a peer of this skill, but worth knowing as the precursor of the alternative path.

## Source Rules

| Rule File | Scope Incorporated |
| --- | --- |
| [`ai-rule-standardization-rules.md`](../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First, SSOT, No-Embedded-Script |
| [`scripting-language-selection-rules.md`](../../../ai-agent-rules/scripting-language-selection-rules.md) §2 | Tier-1 Python default for the verification script |

***

## 1. When to Apply

ALL must hold:

- The superproject is already cloned (typically via `git-lfs-selective-clone`).
- The user named one or more SPECIFIC submodule paths (subset, not all).
- **LFS objects MUST NOT be fetched during checkout** — this is non-negotiable; if LFS bytes are wanted, do not use this skill.
- `--recursive` is NOT wanted (no transitive init).

Do NOT apply when:

- The user wants ALL submodules initialized → use `git-lfs-selective-clone` §3 directly (still LFS-skipped, but `--recursive`).
- The user WANTS LFS objects fetched → do not use this skill; use vanilla `git submodule update --init -- <path>` (no `GIT_LFS_SKIP_SMUDGE`).
- The submodule has already been initialized and you just need to fetch updates → vanilla `git submodule update`.

***

## 2. Prerequisites

| Requirement | Minimum |
|---|---|
| Git | 2.23+ |
| Python | 3.12+ (for the verification script) |
| Working tree state | Superproject clean |
| LFS | `git-lfs` installed (we will configure-around it, not omit it) |

***

## 3. Step-by-Step Procedure

### Phase 1 — Selective Init

Invoke the script:

```bash
python3 <skills-root>/git-submodule-selective-init-no-lfs/scripts/selective-submodule-init.py \
    --repo /path/to/superproject \
    --submodule path/to/sub-one
```

`--submodule` is repeatable for multiple paths.

### Phase 2 — Verification (built into the script)

The script post-checks each named path:

1. `git submodule status -- <path>` no longer prefixed `-` (i.e., the path is now checked out).
2. `.git/modules/<path>/lfs/objects/` is empty or absent (no LFS blobs landed).

The script exits non-zero if either check fails.

***

## 4. Pitfalls

### 4.1 `--no-recursive` is not a valid flag for `submodule update`

`git submodule update --no-recursive ...` exits with usage error. Recursion is OFF by default for `update`; just omit `--recursive`.

### 4.2 Forgetting `filter.lfs.*` neutralization

`GIT_LFS_SKIP_SMUDGE=1` alone is insufficient when the submodule has LFS hooks installed via `.gitattributes` clean/smudge filters. The script applies the full `-c filter.lfs.smudge= -c filter.lfs.process= -c filter.lfs.required=false` trio.

### 4.3 Wrong path separator on Windows

`.gitmodules` uses forward slashes; the script normalizes via `pathlib.PurePosixPath`.

***

## 5. Acceptance Criteria

- **Selective**: each named submodule path's `git submodule status -- <path>` line starts with a space (initialized + at pinned SHA), not `-`. Other (un-named) submodules remain uninitialized (`-` prefix).
- **No-LFS**: `.git/modules/<path>/lfs/objects` is empty or absent for every named path. The script asserts both; non-zero exit otherwise.

***

## 6. Source Recipe Reference

Originally derived from session 2026-05-30 on `<ORG-USER>/<REPO>`: clone the superproject LFS-skipped, then init only the `<SUBMODULE>` submodule (also LFS-skipped). Sanitized via [`redaction-portability`](../redaction-portability/SKILL.md).
