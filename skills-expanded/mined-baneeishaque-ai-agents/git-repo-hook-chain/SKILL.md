---
name: git-repo-hook-chain
description: Configure repo-level hooks via core.hooksPath, with
    lib.bash single-entry dispatch and thin hook wrappers for
    pre-commit/pre-push/pre-merge-commit/pre-rebase.
category: Git-Infrastructure
---

# Git Repo Hook Chain — General Infrastructure

> **Skill ID:** `git-repo-hook-chain`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

This skill provides the **repository-level hook plumbing** for a
standardized git hook chain. It owns:

1. **`setup-repo-hooks.bash`** — sets `git config core.hooksPath
   scripts/githooks` (repo-local config, overrides global hooksPath for
   this repo only).
2. **`lib.bash`** — a single entry point that all hook wrappers exec.
   It determines the caller (which hook or alias invoked it), runs the
   configured check script (via `GATE_CHECK_SCRIPT` env var), and
   dispatches: blocks `pre-*` hooks on check failure, falls through to
   `git status` for the status alias.
3. **Hook wrappers** — four thin files (`pre-commit`, `pre-push`,
   `pre-merge-commit`, `pre-rebase`), each is 3 lines that exec
   `lib.bash "$0"`.

The skill knows nothing about what the check script does. That is
injected via the `GATE_CHECK_SCRIPT` environment variable, set by the
domain composer (e.g., `claude-config-change-gate`).

## Composition Rationale

This skill is a **standalone general infrastructure** skill. It owns
the dispatch mechanism only. Composers set `GATE_CHECK_SCRIPT` to
wire a domain-specific check; this skill runs whatever check it receives.

| Composer | Composition Mechanism |
| --- | --- |
| [`git-operation-blocking-hooks`](../git-operation-blocking-hooks/SKILL.md) | Composes this skill's repo hook chain + global hook bootstrap + alias preflight into a complete blocking gate. Sets `GATE_CHECK_SCRIPT` via the repo's `scripts/setup-hooks.bash`. |

## Environment

| Requirement | Minimum |
| --- | --- |
| Shell | Bash 4+ (hooks execute in shell context; no pwsh dependency) |
| Git | 2.x+ |

## Operational Logic

### 4.1 — Bootstrap (one-time per repo)

Run `scripts/setup-repo-hooks.bash` to activate repo-level hooks:

```bash
bash scripts/setup-repo-hooks.bash
```

This runs:

```text
git config core.hooksPath scripts/githooks
```

This is a **repo-local** config (stored in `.git/config`, not
`~/.gitconfig`). It overrides the global `core.hooksPath` for this
repository only. All executable files in `scripts/githooks/` become
active git hooks.

**Idempotent:** running again overwrites the same config value.

### 4.2 — lib.bash — Single Entry Point

`scripts/githooks/lib.bash` is the single file that all hook wrappers
exec. It is also invoked by the `git status` alias (from
`git-alias-preflight`).

**Dispatch logic:**

```text
1. CALLER=$(basename "$1")   // "pre-commit", "status", etc.
2. GATE_CHECK_SCRIPT="${GATE_CHECK_SCRIPT:-}"
3. If GATE_CHECK_SCRIPT is set and executable:
      run it, capture exit code
4. Switch on CALLER:
      pre-commit | pre-push | pre-merge-commit | pre-rebase:
        if check failed → exit 1 (BLOCK), else exit 0
      status:
        print check result, exec real git status
      *:
        exit 0 (unknown caller — allow)
```

**Key property:** `lib.bash` knows NOTHING about the check logic. It
runs whatever `GATE_CHECK_SCRIPT` points to. This is how different
domains inject different checks.

**Key property:** The check script is responsible for printing its own
diagnostics. `lib.bash` only prints the pass/fail verdict line.

### 4.3 — Hook Wrappers

Each wrapper file in `scripts/githooks/` is a thin 3-line script:

```bash
#!/bin/bash
exec bash "$(git rev-parse --show-toplevel)/scripts/githooks/lib.bash" "$0"
```

The wrappers exist because git hook filenames are hard-coded (git looks
for `pre-commit`, `pre-push`, etc.). Each wrapper passes its own name
(`$0`) to `lib.bash` so the dispatcher knows which hook fired.

Files shipped with this skill:

| File | Git hook name | Invoked by |
| --- | --- | --- |
| `scripts/githooks/pre-commit` | `pre-commit` | `git commit` |
| `scripts/githooks/pre-push` | `pre-push` | `git push` |
| `scripts/githooks/pre-merge-commit` | `pre-merge-commit` | `git merge` (automatic commit) |
| `scripts/githooks/pre-rebase` | `pre-rebase` | `git rebase` |

### 4.4 — Wiring a Check Script

The domain composer (or admin) sets the `GATE_CHECK_SCRIPT` environment
variable, typically in the repo's `scripts/setup-hooks.bash`:

```bash
# Inside scripts/setup-hooks.bash:
export GATE_CHECK_SCRIPT="$PWD/scripts/check-claude-trivial.bash"
```

`lib.bash` reads this variable on each invocation. If it is unset or
empty, no check runs and all hooks pass through (allow).

### 4.5 — Verifying the Hook Chain

```bash
# Confirm hooksPath is set
git config core.hooksPath
# Should print: scripts/githooks

# Confirm hooks are executable
ls -la scripts/githooks/pre-commit scripts/githooks/pre-push
# Should show -rwxr-xr-x

# Test a hook invocation (simulate)
bash scripts/githooks/lib.bash pre-commit
# Should run the check and exit 0 (allow) or 1 (block)
```

## Script Reference

| Script | Purpose | Invocation |
| --- | --- | --- |
| [`scripts/githooks/lib.bash`](scripts/githooks/lib.bash) | Single entry point — dispatch by caller | `bash .../lib.bash <caller>` |
| [`scripts/githooks/pre-commit`](scripts/githooks/pre-commit) | Wrapper — exec lib.bash | Automatic via git |
| [`scripts/githooks/pre-push`](scripts/githooks/pre-push) | Wrapper — exec lib.bash | Automatic via git |
| [`scripts/githooks/pre-merge-commit`](scripts/githooks/pre-merge-commit) | Wrapper — exec lib.bash | Automatic via git |
| [`scripts/githooks/pre-rebase`](scripts/githooks/pre-rebase) | Wrapper — exec lib.bash | Automatic via git |
| [`scripts/setup-repo-hooks.bash`](scripts/setup-repo-hooks.bash) | Bootstrap — set hooksPath | `bash scripts/setup-repo-hooks.bash` |

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`git-operation-blocking-hooks`](../git-operation-blocking-hooks/SKILL.md) | Composes this skill's repo hook chain + global bootstrap + alias preflight. The `setup-repo-hooks.bash` script is called by the repo's `scripts/setup-hooks.bash` on every checkout (triggered by the global post-checkout hook). |

## Related Skills

| Skill | Relationship |
| --- | --- |
| [`git-global-hook-bootstrap`](../git-global-hook-bootstrap/SKILL.md) | Upstream — the global `post-checkout` hook triggers `setup-repo-hooks.bash` on every checkout. |
| [`git-alias-preflight`](../git-alias-preflight/SKILL.md) | Companion — registers the `git status` alias that invokes `lib.bash status` in the same dispatch pattern. |

## Verification

```bash
# Run the bootstrap
bash scripts/setup-repo-hooks.bash
# Expected: "Set core.hooksPath = scripts/githooks"

# Confirm config
git config core.hooksPath
# Expected: scripts/githooks

# Simulate a pre-commit invocation
GATE_CHECK_SCRIPT="" bash scripts/githooks/lib.bash pre-commit
# Expected: exit 0 (no check configured = allow)

# Simulate status alias invocation
GATE_CHECK_SCRIPT="" bash scripts/githooks/lib.bash status
# Expected: runs "git status" after check output
```
