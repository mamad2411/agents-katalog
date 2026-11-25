---
name: git-commit-identity-rewrite
description: Composer — rewrite the author and committer identity
    (name, email, optional dates) of one or more historical commits
    by copying from a source commit, delegating rebase mechanics to
    git-commit-edit and handling the cross-repo submodule-pointer
    cascade.
category: Git & Repository Management
---

# Git Commit Identity Rewrite Skill

> **Skill ID:** `git-commit-identity-rewrite`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Rewrite the **author** and **committer** identity (and optionally the
author/committer dates) of one or more historical commits, copying
the identity from a designated source commit. Supports cross-repo
operations where one or more targets live in a Git submodule and the
parent repository's gitlink must be re-staged after the submodule
rewrite.

This skill owns the **identity-copy concern**: source-identity
discovery, the committer-override env-var dance, date-preservation
modes, and submodule-pointer cascade handling. The mechanics of
pausing on a target commit and replaying descendants are owned by
the base [`git-commit-edit`](../git-commit-edit/SKILL.md) skill.

Unlike `git-commit-edit` §3e (which only documents single-field
`--author=` correction), this skill rewrites **both** author and
committer in lock-step, preserves dates per a user-confirmed scope,
and coordinates rewrites across a parent repo and one of its
submodules in a single workflow.

## Composition Rationale

This is a **composer** over [`git-commit-edit`](../git-commit-edit/SKILL.md).

| Concern | Owner |
|---|---|
| Locate target commit, verify branch, descendant count, remote divergence | [`git-commit-edit`](../git-commit-edit/SKILL.md) §0 |
| Backup branch (local, optional remote) | [`git-commit-edit`](../git-commit-edit/SKILL.md) §0e |
| Interactive rebase with `edit` action, descendant replay, conflict handling | [`git-commit-edit`](../git-commit-edit/SKILL.md) §2, §5 |
| Stash protocol for dirty working tree | [`git-commit-edit`](../git-commit-edit/SKILL.md) §1, §6 |
| Force-push authorization gate | [`git-commit-edit`](../git-commit-edit/SKILL.md) §7b |
| Backup-branch cleanup gate | [`git-commit-edit`](../git-commit-edit/SKILL.md) §8 |
| **Source-commit identity discovery** | **this skill** |
| **Date-scope decision (name+email only / +author date / full)** | **this skill** |
| **Author + committer combined override via env vars** | **this skill** |
| **Cross-repo submodule-pointer cascade** | **this skill** |

The composer **MUST NOT** reimplement the rebase mechanics; it provides
the identity payload as input to the base skill's `edit` flow and
delegates every backup, push, and cleanup gate.

## Source Rules

| Rule File / Skill | Scope Incorporated |
|---|---|
| [`git-commit-edit/SKILL.md`](../git-commit-edit/SKILL.md) | All rebase, backup, push, and cleanup mandates (transitive) |
| [`git-operation-rules.md`](../../../ai-agent-rules/git-operation-rules.md) | Sections 2–4 (commit/push/stash protocols) — inherited via `git-commit-edit` |
| [`git-submodule-pointer-repair/SKILL.md`](../git-submodule-pointer-repair/SKILL.md) | §5 Mass Pointer Reconciliation — invoked when the submodule rewrite cascades through multiple parent commits |

## Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ or Bash 4+ |
| Access | Write access to all repositories involved (parent + submodule, if applicable) |
| State | Clean working tree (or willingness to stash) in every repo |
| Source commit | Must be reachable in the parent repo (or a repo accessible to the user); only its `%an / %ae / %aI / %cI` are read |

## When to Apply

Apply this skill when:

- A user asks to "change the author" or "fix the committer" of one or
  more existing commits and identifies a **source commit** whose
  identity should be copied.
- The same identity must be applied to commits across a parent repo
  and one of its submodules in a coordinated rewrite.
- Both author **and** committer must be rewritten in lock-step
  (single-field `--author=` correction is insufficient).
- The user wants to preserve the original author/committer **dates**
  of each target while changing only the identity strings.

Do NOT apply when:

- Only the message needs changing — use
  [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md).
- File contents need changing — use
  [`git-commit-edit`](../git-commit-edit/SKILL.md) directly.
- The author field alone is wrong and committer is correct — `git-commit-edit` §3e
  (single-field `--author=`) is sufficient.
- The target commit has ≥2 parents (merge commit) — abort and re-plan
  with `git rebase -i --rebase-merges` per §0c.

---

## Step-by-Step Procedure

### Step 0 — Pre-Edit Discovery & Scope Confirmation

#### 0a — Capture Source Identity

Read the source commit's identity in **all four** dimensions:

```powershell
git -C <source-repo> show -s --pretty="Author: %an <%ae>%nAuthorDate: %aI%nCommit: %cn <%ce>%nCommitDate: %cI" <source-sha>
```

**Flag-by-flag (Deep Command Explanation Mandate):**

- `-C <repo>` — execute the command as if `cd`-ed into `<repo>` first.
- `show -s` — `--no-patch`; suppress diff, show only commit metadata.
- `--pretty="..."` — custom format string. Placeholders:
  - `%an` author name
  - `%ae` author email
  - `%aI` author date in strict ISO-8601
  - `%cn` committer name
  - `%ce` committer email
  - `%cI` committer date in strict ISO-8601
- `%n` — literal newline.

#### 0b — Capture Each Target's Original Dates

For each target commit, capture its current author/committer dates so
they can be preserved through the amend:

```powershell
git -C <repo> show -s --pretty="%aI%n%cI" <target-sha>
```

These two timestamps become the literal payload for `--date=` and
`$env:GIT_COMMITTER_DATE` in §3.

#### 0c — Merge-Commit Guard (CRITICAL)

The simple `pick→edit` flip used by `git-commit-edit` §2 loses parent
topology on merge commits. Run, **for every target**:

```powershell
git -C <repo> show -s --pretty=%P <target-sha>
```

If the output contains 2+ SHAs, **ABORT**. Re-plan with
`git rebase -i --rebase-merges` (out of scope for this skill — see
[`git-rebase-standardization`](../git-rebase-standardization/SKILL.md))
or use `git replace --graft` + `git filter-repo`.

#### 0d — Cross-Repo Dependency Analysis

If targets span both a parent repo and its submodule, determine
**ordering**:

1. List every parent commit in the rebase horizon
   (`<oldest-parent-target>~1..HEAD`).
2. For each, run:
   ```powershell
   git -C <parent-repo> show --stat <parent-sha> | Select-String "^ <submodule-path> "
   ```
3. If any parent commit modifies the submodule gitlink at an SHA
   that the submodule rewrite will produce, the **submodule rewrite
   MUST run first**, and the parent rewrite MUST stage the new
   gitlink before amending (see §5).

#### 0e — Date-Scope Decision (User-Gated)

The agent **MUST** ask the user — and wait for an answer — before
proceeding:

| Scope | Author Identity | Committer Identity | Author Date | Committer Date |
|---|---|---|---|---|
| **Identity-only** (default) | source `%an`/`%ae` | source `%an`/`%ae` | target's original `%aI` | target's original `%cI` |
| **+ Author date** | source `%an`/`%ae` | source `%an`/`%ae` | source `%aI` | now (`git`'s default) |
| **Full** | source `%an`/`%ae` | source `%an`/`%ae` | source `%aI` | source `%cI` |

#### 0f — Present the Edit Plan

Per `git-commit-edit` §0f, present a consolidated plan listing every
target, the source identity payload, the chosen date scope, the
rebase ordering, and the force-push horizon. **Do NOT begin until
the user confirms.**

---

### Step 1 — Per-Target Loop

For each target, in dependency order (submodule before parent if
§0d flagged a cascade):

1. Delegate **Steps 0e – 2c of `git-commit-edit`**: stash if dirty,
   create `backup/pre-author-edit-<n>` (offer remote push), build the
   sequence-editor script that flips `pick <target>` → `edit <target>`,
   launch `git rebase -i <target>~1`, verify the rebase paused on the
   correct commit.
2. Execute Step 3 of this skill (the identity-override block).
3. Execute Step 4 of this skill (tree-parity verification).
4. If this target is the parent of a cascade, execute Step 5 of this
   skill (submodule pointer staging) **before** the amend in Step 3.
5. Delegate **Steps 5 – 7 of `git-commit-edit`**: `git rebase --continue`,
   stash pop, cleanup of the temp script.

---

### Step 3 — The Identity-Override Block

This is the core mechanic this skill owns. Plain
`git commit --amend --author="Name <email>"` rewrites only the author;
the committer is taken from the runtime environment. To rewrite both
deterministically, set the three `GIT_COMMITTER_*` env vars **before**
the amend, then explicitly remove them so they do not leak into the
next command:

**Identity-only scope (default):**

```powershell
$env:GIT_COMMITTER_NAME  = '<source-name>'
$env:GIT_COMMITTER_EMAIL = '<source-email>'
$env:GIT_COMMITTER_DATE  = '<target-original-cI>'
git commit --amend --author='<source-name> <<source-email>>' `
    --date='<target-original-aI>' --no-edit
Remove-Item Env:\GIT_COMMITTER_NAME, Env:\GIT_COMMITTER_EMAIL, Env:\GIT_COMMITTER_DATE
```

**Flag-by-flag (Deep Command Explanation Mandate):**

- `$env:GIT_COMMITTER_NAME` / `_EMAIL` / `_DATE` — Git's documented
  override hooks for the committer trailer. They are read **only**
  by `git-commit-tree` (which `git commit --amend` invokes
  internally), so setting them on the line immediately before the
  amend is sufficient.
- `--amend` — replaces `HEAD` with a new commit object built from the
  current index and the supplied identity payload.
- `--author='Name <email>'` — overrides the author trailer. The angle
  brackets around the email are mandatory per RFC 5322; PowerShell
  needs them outside the single quotes only if `<` or `>` would be
  interpreted by the parser, which inside a single-quoted argument
  they are not.
- `--date='<ISO-8601>'` — overrides the **author** date. (There is no
  `--committer-date` flag; that channel exists only as the env var
  above.)
- `--no-edit` — do not launch the editor; reuse the existing message
  verbatim.
- `Remove-Item Env:\...` — explicit cleanup. **MANDATORY**: leftover
  `GIT_COMMITTER_*` vars will silently corrupt the next commit in the
  same shell session.

**+ Author-date scope:** replace `<target-original-aI>` with the
source's `%aI`, and omit `GIT_COMMITTER_DATE` entirely so Git uses
"now".

**Full scope:** replace `<target-original-aI>` with source `%aI` and
`<target-original-cI>` with source `%cI`.

#### 3a — Verify Identity Override

```powershell
git -C <repo> show -s --pretty=fuller HEAD
```

The output MUST show `Author:` and `Commit:` lines both equal to the
source identity, and `AuthorDate` / `CommitDate` matching the chosen
scope.

---

### Step 4 — Tree-Parity Verification

Identity rewrite MUST NOT alter file content. Verify per repo:

```powershell
$old = git -C <repo> rev-parse '<backup-branch>^{tree}'
$new = git -C <repo> rev-parse 'HEAD^{tree}'
if ($old -eq $new) { "PARITY: tree IDENTICAL" } else { git -C <repo> diff <backup-branch> HEAD --stat }
```

Expected outcomes:

| Repo | Expected diff |
|---|---|
| Submodule | **Empty** — trees identical (only metadata changed) |
| Parent (no cascade) | **Empty** — trees identical |
| Parent (with cascade) | **Exactly one line** — the submodule gitlink updated to the new submodule SHA; nothing else |

Any other diff is a failure: abort, restore from
`backup/pre-author-edit-<n>`, and re-plan.

---

### Step 5 — Submodule Pointer Cascade (Conditional)

Execute **only** when §0d flagged a parent commit that gitlinks the
rewritten submodule SHA.

**Single-commit cascade (most common):** the parent's amended commit
needs to point at the new submodule HEAD. Between §1 step 4 and the
amend in §3:

```powershell
git -C <parent-repo> add <submodule-path>
git -C <parent-repo> status --short   # MUST show only `M <submodule-path>`
```

Then proceed with the §3 amend in the parent.

**Multi-commit cascade:** if more than one parent commit references
pre-rewrite submodule SHAs (i.e., the cascade spans multiple parent
commits — the rewritten submodule commit is **not** at the parent
repo's `HEAD`), this skill's per-target loop is insufficient.
**Delegate to** [`git-submodule-pointer-repair` §5 Mass Pointer
Reconciliation](../git-submodule-pointer-repair/SKILL.md#5-mass-pointer-reconciliation-full-history-rewrite-recovery)
with the old→new SHA map produced by §1. The parent repo's old
submodule SHAs MUST remain resolvable for the duration of that
repair (the `backup/pre-author-edit-<n>` branch in the submodule
guarantees this).

---

### Step 6 — Push Gate (Delegated)

When all rewrites are complete, delegate to
[`git-commit-edit` §7b](../git-commit-edit/SKILL.md). Mandatory
ordering for cross-repo cascades: **submodule pushed first**, parent
second, so the parent's gitlink resolves remotely.

The agent MUST present each `git push --force-with-lease` command
verbatim and wait for explicit per-repo "yes". Auto-push is
**PROHIBITED**.

---

### Step 7 — Backup Cleanup Gate (Delegated)

Delegate to [`git-commit-edit` §8](../git-commit-edit/SKILL.md).
Auto-deletion of `backup/pre-author-edit-<n>` /
`backup/pre-force-push-<n>` is **PROHIBITED**.

---

## Scope Coverage

| Category | Convention |
|---|---|
| Source-identity discovery | `git show -s --pretty="%an <%ae>%n%aI%n%cn <%ce>%n%cI"` |
| Author override | `git commit --amend --author='Name <email>'` |
| Committer override | `$env:GIT_COMMITTER_NAME / _EMAIL` env vars |
| Author-date preservation | `--date='<target-original-aI>'` |
| Committer-date preservation | `$env:GIT_COMMITTER_DATE='<target-original-cI>'` |
| Date-scope toggle | User-gated decision in §0e (identity-only / +author-date / full) |
| Submodule + parent cascade (single commit) | Stage gitlink in parent before amend |
| Submodule + parent cascade (multi-commit) | Delegate to `git-submodule-pointer-repair` §5 |
| Backup, push, cleanup | Delegated to `git-commit-edit` §0e / §7b / §8 |

---

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Using `--author=` alone** when both author and committer must
  change — leaves committer trailer wrong.
- **Omitting `Remove-Item Env:\GIT_COMMITTER_*`** after the amend —
  the env vars will silently corrupt the next commit in the same
  shell.
- **Rewriting the parent before the submodule** when §0d flagged a
  cascade — produces an orphaned gitlink mid-rebase.
- **Skipping the date-scope question (§0e)** — the user MUST confirm
  before any amend.
- **Skipping the merge-commit guard (§0c)** — `pick→edit` on a merge
  commit silently loses topology.
- **Auto-pushing** — every push gate in `git-commit-edit` §7b applies
  transitively and requires explicit user authorization.
- **Auto-deleting backup branches** — `git-commit-edit` §8 applies
  transitively.
- **Using `--force` instead of `--force-with-lease`** — same as base
  skill's prohibition.

---

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| `--author=` alone leaves committer wrong | Use the env-var block in §3; verify with `git show -s --pretty=fuller`. |
| `GIT_COMMITTER_*` leaks into next commit | Always `Remove-Item Env:\GIT_COMMITTER_NAME, Env:\GIT_COMMITTER_EMAIL, Env:\GIT_COMMITTER_DATE` immediately after the amend. |
| PowerShell `git stash push --include-untracked -m "..."` without explicit pathspec leaves WT dirty | Re-issue with explicit pathspec list (`-- <file1> <file2> <dir>/`); verify with `git status --short`. |
| Parent rebase fails with "object not found" mid-cascade | Submodule rewrite must run first AND its `backup/pre-author-edit-<n>` branch must remain (it keeps the old submodule SHAs reachable for §5 multi-commit cascade). |
| Tree parity diff shows unexpected files | Identity rewrite leaked a content change — abort, reset to `backup/pre-author-edit-<n>`, re-plan. |
| Bash equivalent needed | Replace `$env:NAME='val'` with `NAME='val'` prefixed inline on the `git commit` line (single-line scope) or `export NAME='val'; ...; unset NAME`. |

---

## Composition by Higher-Level Skills

(None yet. When a domain-specific composer is added — e.g.,
"normalize all commits in a range to a canonical author" — register
it here per skill-factory §2.0 bidirectional discoverability.)

---

## Related Skills

- [`git-commit-edit`](../git-commit-edit/SKILL.md) — base; owns rebase
  mechanics, backup, push, cleanup gates.
- [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md) —
  sibling composer over the same base, owns the message-only concern.
- [`git-submodule-pointer-repair`](../git-submodule-pointer-repair/SKILL.md) —
  delegated to in §5 for multi-commit submodule cascades.
- [`git-rebase-standardization`](../git-rebase-standardization/SKILL.md) —
  consult when §0c detects a merge-commit target.
