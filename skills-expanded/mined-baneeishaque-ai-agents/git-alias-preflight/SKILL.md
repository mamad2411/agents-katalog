---
name: git-alias-preflight
description: "Create git aliases that run a pre-flight check before the real command. Canonical: git status to check + real status."
category: Git-Infrastructure
---

# Git Alias Preflight — General Infrastructure

> **Skill ID:** `git-alias-preflight`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

This skill provides the **alias plumbing** for pre-flight check chaining.
It owns a `register-alias.bash` script that creates a git alias (e.g.,
`git status`) that runs a pre-flight check script before falling through
to the real command.

**Pattern:**

```text
git config alias.<name> "!bash <script> <caller>"
```

The `!` prefix tells git to execute a shell command instead of a
subcommand. The script runs the check, prints the result, then
`exec git <name>` falls through to the real command. This means the
user sees the check output AND the real command output in one
invocation — no extra typing.

**Canonical alias:** `git status`

```bash
git config alias.status "!bash scripts/githooks/lib.bash status"
```

Now `git status` runs the check (via `lib.bash`), then `exec git status`
shows the real status.

## Composition Rationale

This skill is a **standalone general infrastructure** skill. It owns
the alias registration pattern. Composers integrate it into larger
workflows:

| Composer | Composition Mechanism |
| --- | --- |
| [`git-operation-blocking-hooks`](../git-operation-blocking-hooks/SKILL.md) | Composes this skill's alias registration + global hook bootstrap + repo hook chain. The `scripts/setup-hooks.bash` calls `register-alias.bash` on every checkout. |

## Environment

| Requirement | Minimum |
| --- | --- |
| Shell | Bash 4+ |
| Git | 2.x+ |

## Operational Logic

### 5.1 — Alias Pattern

The `!` prefix in git config alias values tells git to execute the
remainder as a shell command. The standard form:

```text
git config alias.<name> "!bash <path-to-script> <caller-identifier>"
```

The script runs the check (or dispatch), then `exec git <name>` falls
through to the real command.

This pattern ensures:

- The alias produces both check output AND command output.
- The check script's exit code is visible to the user.
- The real command is never skipped (always executed after the check).

### 5.2 — Canonical: git status

The primary alias defined by this skill is `git status`:

```bash
git config alias.status "!bash scripts/githooks/lib.bash status"
```

When the user types `git status`:

1. Git intercepts via the alias and runs:
   `bash scripts/githooks/lib.bash status`
2. `lib.bash` sees caller = `status`, runs the check script.
3. Check output is printed: `--- [gate preflight check] --- ...`
4. `lib.bash` executes `exec git status`, which shows real status.

### 5.3 — Registration

Run `scripts/register-alias.bash` to set up aliases for the current repo:

```bash
bash scripts/register-alias.bash
```

This is typically called from `scripts/setup-hooks.bash` (the repo
bootstrap script) on every checkout. Idempotent — running again
overwrites the same alias value with no side effects.

### 5.4 — Other Aliases

The same pattern works for any git command:

```bash
git config alias.log "!bash scripts/githooks/lib.bash log"
```

Where `lib.bash` would need a `log)` case in its dispatcher. This
skill ships only the `status` alias; extending to other commands
follows the same pattern.

## Script Reference

| Script | Purpose | Invocation |
| --- | --- | --- |
| [`scripts/register-alias.bash`](scripts/register-alias.bash) | Register git status alias | `bash scripts/register-alias.bash` |

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`git-operation-blocking-hooks`](../git-operation-blocking-hooks/SKILL.md) | Composes this skill's alias into the blocking gate. The `scripts/setup-hooks.bash` calls `register-alias.bash` on every checkout. |

## Related Skills

| Skill | Relationship |
| --- | --- |
| [`git-repo-hook-chain`](../git-repo-hook-chain/SKILL.md) | Companion — the alias invokes `lib.bash status`, which uses the same dispatch pattern as the hook wrappers. |
| [`git-global-hook-bootstrap`](../git-global-hook-bootstrap/SKILL.md) | Upstream — the global `post-checkout` triggers repo bootstrap, which registers the alias. |

## Verification

```bash
# Register the alias
bash scripts/register-alias.bash

# Confirm alias is set
git config alias.status
# Expected: "!bash scripts/githooks/lib.bash status"

# Invoke the alias (simulates user typing "git status")
git status
# Expected: check output + "--- [gate preflight check] ---" + real status
```
