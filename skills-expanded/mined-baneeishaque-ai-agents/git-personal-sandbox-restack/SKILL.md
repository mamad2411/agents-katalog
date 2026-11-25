---
name: git-personal-sandbox-restack
description: Composer — restack a personal sandbox branch onto the
    current tip of a moving team / feature / ticket branch via
    rebase, with a six-axis content-equality audit
    (patch-id / files-touched / file-set / per-file bytes /
    tree / tip-byte parity) that proves no personal content was
    lost before the mandatory force-push authorization.
category: Git & Repository Management
---

# Git Personal Sandbox Restack Skill (v1)

> **Skill ID:** `git-personal-sandbox-restack`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A `personal/<purpose>` sandbox branch (created via
[`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md)) is
stacked on top of a team / feature / ticket branch (e.g.,
`<author>-<ticket-id>`) that has since advanced with new team commits. The
author wants the sandbox to sit directly on top of the **current** team-branch
tip so that:

- The sandbox inherits the latest team work transparently (no merge commits).
- Future divergence audits between the sandbox and the team branch surface
  only the personal-only commits, not the stale base.
- The sandbox's force-push to the personal remote replaces the stale history
  without losing any personal-content byte.

This skill orchestrates the restack + audit + push in a way that:

1. Tags both endpoints before any mutation.
2. Runs `git rebase --onto <team-tip> <merge-base> <sandbox>`.
3. Resolves the typical **modify-vs-delete (DU)** conflicts that arise when
   the new base deleted a file that the sandbox modifies, by re-adding the
   sandbox's version.
4. Executes a **six-axis equality audit** between the pre-rebase tip and the
   post-rebase tip — proving that net content is preserved, even when
   patch-ids legitimately differ due to base-context shifts.
5. Gates the force-push behind explicit user authorization.

## Composition Rationale

This skill is a **composer** that orchestrates the following primitives
without reimplementing them:

| Composed Skill | Used for |
|---|---|
| [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md) | The sandbox-creation, dual-remote, and push-hygiene contracts assumed by this skill |
| [`git-divergence-audit`](../git-divergence-audit/SKILL.md) | The merge-base / left-right discovery used to pick the rebase upstream |
| [`git-rebase-standardization`](../git-rebase-standardization/SKILL.md) | The actual `rebase --onto` mechanics, conflict-resolution discipline, and backup protocol |
| [`git-commit-metadata-extraction`](../git-commit-metadata-extraction/SKILL.md) | Per-commit subjects / file lists used by the audit table |
| [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) | Per-push authorization gate |
| [`redaction-portability`](../redaction-portability/SKILL.md) | Sanitizing any artifact produced from this workflow |

The composer **MUST NOT** reimplement rebase mechanics, sandbox provisioning,
or divergence discovery — those are the owners' jobs.

## Related Skills

- [`git-branch-promotion`](../git-branch-promotion/SKILL.md) — analogous
  pattern but for **canonical** branches: promotes a refined branch onto a
  team branch. This skill is its **personal-sandbox sibling**.
- [`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md)
  — when the goal is to **retire** a parallel branch (not restack a personal
  one). Often invoked just BEFORE this skill so the sandbox restacks onto a
  clean canonical tip.
- [`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md)
  — the N-dependent generalization of this skill. Use it when MORE THAN ONE
  branch (e.g., the personal sandbox AND a diagnostics branch AND a feature
  stack) is stacked on a base that just moved. The cascade skill re-uses
  this skill's six-axis parity audit per dependent.
## Composition by Higher-Level Skills

| Composer Skill | Role of this skill in the pipeline |
| --- | --- |
| [`git-personal-content-extraction`](../git-personal-content-extraction/SKILL.md) | This skill is consumed in §Phase 6 to restack the long-lived `personal/sandbox` branch onto each round's purified team tip BEFORE slot-inserting the extracted personal commits at their original chronological position. |
| [`git-personal-team-branch-workflow`](../git-personal-team-branch-workflow/SKILL.md) | This skill is consumed in §3.2 (the incremental restack cycle) — the session-workflow composer triggers `git rebase --onto <team-branch> <merge-base> <personal-branch>` after each team commit, and delegates deep verification (§3 six-axis audit) to this skill when the quick post-restack check fails. |

## Source Rules

| Rule File | Scope Incorporated |
| --- | --- |
| [`ai-rule-standardization-rules.md`](../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First Architecture, Layered Composition Mandate |
| [`git-rebase-standardization/SKILL.md` Step 5–6](../git-rebase-standardization/SKILL.md) | Rebase backup + execution discipline |
| [`git-commit-edit/SKILL.md` Step 7b](../git-commit-edit/SKILL.md) | Push-authorization gate (re-applied to the force-push step) |

***

## 1. When to Apply

Apply this skill when ALL of the following hold:

- A `personal/<purpose>` branch exists on the local clone and on the
  `personal` remote.
- A team / feature / ticket branch (e.g., `<author>-<ticket-id>`) has
  advanced — its tip is now further from the sandbox's merge-base.
- The author wants the sandbox to sit on top of the current team-branch tip.
- The personal sandbox contains ONLY personal-only commits (no team work
  that hasn't already been promoted to the team branch).

Do NOT apply when:

- The team branch is `master` / `main` and the sandbox's personal-only
  commits do not need to track team progress closely — a periodic
  `git rebase` is fine without the six-axis audit.
- The sandbox contains commits that the team branch has not yet absorbed —
  promote those first via
  [`git-branch-promotion`](../git-branch-promotion/SKILL.md).
- The personal sandbox needs full reconstruction (the parallel branch was
  decommissioned out from under it) — use
  [`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md)
  Phase 2's rebuild path instead.

***

## 2. Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.23+ |
| Shell | PowerShell 5.1+ or POSIX shell |
| Auth | Credential Manager (Route A from [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md) §Prerequisites) — `--force-with-lease` requires the same credentials used to create the sandbox |
| Tags | The pre-rebase sandbox tip MUST be tagged (Phase 0) before any rebase command runs |

***

## 3. Step-by-Step Procedure

### Phase 0 — Safety Tag & State Capture

```powershell
$repo='<repo-path>'
$today = Get-Date -Format 'yyyy-MM-dd'
git -C $repo tag "backup/<sandbox>-pre-restack-<ticket>-$today" <sandbox>
git -C $repo status --short  # MUST be empty
```

### Phase 1 — Discovery (delegates to git-divergence-audit §2)

```powershell
$mergeBase = git -C $repo merge-base <sandbox> <team-branch>
git -C $repo rev-list --left-right --count <sandbox>...<team-branch>
git -C $repo --no-pager log --reverse --oneline "${mergeBase}..<sandbox>"
```

Capture: `$mergeBase`, the list of `personal_commits[]` (oldest → newest),
and the team-branch tip SHA.

### Phase 2 — Rebase --onto

```powershell
git -C $repo rebase --onto <team-branch> $mergeBase <sandbox>
```

#### 2a — Modify-vs-Delete (DU) Conflict

Common when the new base **deleted** a file that a sandbox commit
**modifies** (e.g., the team branch cleaned up a skill folder the sandbox is
still editing). Symptom:

```text
CONFLICT (modify/delete): <path> deleted in HEAD and modified in <sha>.
Version <sha> of <path> left in tree.
```

**Resolution — re-add the sandbox's version (`git add`)**, then continue:

```powershell
git -C $repo add <path>            # accept the sandbox's modification
# OR, to honor the deletion:
# git -C $repo rm <path>
git -C $repo status --short        # confirm A or D state
git -C $repo -c core.editor=true rebase --continue
```

The `-c core.editor=true` flag uses the existing message without opening an
editor; the original commit message stays intact across the restack.

### Phase 3 — Six-Axis Equality Audit

Run BEFORE the force-push. Establish the SHA pairing (remote pre-rebase vs
local post-rebase), then verify all six axes for each pair:

> **PowerShell pitfall**: NEVER name a variable `$pid` — it's a read-only
> built-in (process ID). Use `$pidR` / `$pidL` / `$pidEq` etc.

```powershell
$pairs = @(
    @('<remote-sha-1>','<local-sha-1>','Title 1'),
    @('<remote-sha-2>','<local-sha-2>','Title 2'),
    # ...one row per personal commit
)
'{0,-10} {1,-10} {2,-8} {3,-7} {4,-7} {5}' -f 'REMOTE','LOCAL','PatchID','Files','Bytes','Title'
foreach ($p in $pairs) {
    $r=$p[0]; $l=$p[1]; $t=$p[2]
    $pidR = (git -C $repo show $r | git -C $repo patch-id --stable) -split ' ' | Select-Object -First 1
    $pidL = (git -C $repo show $l | git -C $repo patch-id --stable) -split ' ' | Select-Object -First 1
    $pidEq = if ($pidR -eq $pidL) {'EQUAL'} else {'DIFFER'}
    $rf = @(git -C $repo show --pretty=format: --name-only $r | Where-Object { $_ })
    $lf = @(git -C $repo show --pretty=format: --name-only $l | Where-Object { $_ })
    $filesEq = if ((Compare-Object ($rf|Sort-Object) ($lf|Sort-Object)) -eq $null) {'SAME'} else {'DIFF'}
    $bytesEq = 'SAME'
    foreach ($f in $rf) {
        $rc = git -C $repo show "${r}:${f}" 2>$null
        $lc = git -C $repo show "${l}:${f}" 2>$null
        if ((($rc -join "`n") -ne ($lc -join "`n"))) { $bytesEq='DIFF'; break }
    }
    '{0,-10} {1,-10} {2,-8} {3,-7} {4,-7} {5}' -f $r,$l,$pidEq,$filesEq,$bytesEq,$t
}
```

#### 3.1 The Six Axes

| # | Axis | Tool | Pass criterion |
|---|---|---|---|
| 1 | Patch-id | `git patch-id --stable` per side | EQUAL when context unchanged; DIFFER acceptable when base shifted |
| 2 | Files-touched set | `git show --name-only` ∩ `Compare-Object` | SAME (or explained — see §3.2) |
| 3 | Per-file byte content within the commit | `git show <sha>:<path>` byte-compare | SAME for every shared file |
| 4 | Final tree-tip personal-path parity | `git diff --stat <pre> <post> -- <personal-paths>` | empty diff |
| 5 | File-set tip parity | `git ls-tree -r --name-only` Compare-Object | no personal file unique to remote |
| 6 | Tip byte content | `git show <pre-tip>:<path>` vs `git show <post-tip>:<path>` | identical for every personal-owned path |

#### 3.2 Explained Patch-ID Divergence

Patch-id legitimately differs in two well-understood cases — these are NOT
content losses:

- **Modify-vs-Create after a base deletion**: The pre-rebase commit
  modified a file the new base no longer has; the rebase recreates the file
  whole. Patch shape changes from "modify N lines" to "create whole file",
  but the **final byte content at the tip is identical** (verify on Axis 6).
- **Drop-on-no-op when new base already applied the same change**: The
  pre-rebase commit changed an attribute the new base has since
  independently set to the same value; the rebase drops the now-no-op patch
  and the file is omitted from the post-rebase commit. Verify the
  attribute's **final value at the tip is the desired value** (Axis 6).

If neither explanation fits, STOP and re-classify before force-pushing —
the divergence may be a real loss.

### Phase 4 — Force-Push (Authorization Gate)

ONLY after the six-axis audit passes and the user explicitly authorizes:

```powershell
git -C $repo push --force-with-lease personal <sandbox>
```

`--force-with-lease` is MANDATORY. `--force` is FORBIDDEN — it bypasses the
"someone-else-pushed-since-your-last-fetch" safety net.

### Phase 5 — Safety Tag Drop (After External Verification)

The user externally verifies the personal remote (e.g., GitHub Web UI). After
confirmation:

```powershell
git -C $repo tag -d "backup/<sandbox>-pre-restack-<ticket>-$today"
```

***

## 4. Pitfalls & Recovery

### 4.1 Local team branch missing (deleted by earlier cleanup)

Symptom: `fatal: ambiguous argument '<team-branch>': unknown revision`.

Recovery:

```powershell
git -C $repo branch <team-branch> origin/<team-branch>
git -C $repo branch --set-upstream-to=origin/<team-branch> <team-branch>
```

### 4.2 PowerShell `$pid` collision

Symptom: `Cannot overwrite variable PID because it is read-only or constant.`

Cause: `$pid` is a PowerShell built-in (current process ID). Setting any
variable named `$pid` in your audit loop throws on every iteration.

Fix: rename to `$pidR`, `$pidL`, `$pidEq`, `$pidValue`, etc.

### 4.3 Force-push rejected (lease stale)

Symptom: `! [rejected] <sandbox> -> <sandbox> (stale info)`.

Cause: someone (or another machine) pushed to the personal remote since
your last fetch.

Recovery: `git -C $repo fetch personal`, re-run the six-axis audit against
the freshly-fetched remote tip, then re-attempt the force-push. NEVER
escalate to `--force`.

### 4.4 Inherited team-branch fix overrides a personal value

Example from the source session: SWIT-12101's `fix(launch)` commit replaced
a `WORKING_DIRECTORY` attribute in a `.launch` file. The personal sandbox
had been pointing at an older OneDrive path. After restack, the personal
tip inherits the team value (the new, correct one).

This is the **expected behavior** of `rebase --onto` — the team branch is
the new authority. If the user actually wants to keep the personal override,
that's a NEW commit on top of the restacked sandbox, not a regression to
fix.

### 4.5 IDE file-lock kills checkout mid-stream

When VS Code / Eclipse / a JVM is indexing the workspace, `git checkout`
during Phase 2 can fail with `Deletion of directory '<path>' failed.
Should I try again? (y/n)`. Recover with `git reset --hard HEAD`, then
re-run the rebase in an isolated detached worktree (`C:\temp\gitwork-*`)
outside the IDE's watch scope. See
[`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md) §4.6.

### 4.6 PowerShell `Out-File` / `Set-Content` breaks blob-hash parity

When this skill (or a downstream conflict-resolution composer such as
[`git-drop-commit-with-divergent-recreation`](../git-drop-commit-with-divergent-recreation/SKILL.md))
needs to restore a git-tracked file from a known blob, the file MUST be
written byte-exactly. PowerShell's `Out-File`, `Set-Content`, and `>`
redirection re-encode the stream on Windows: BOM injection (`UTF8` ≠
`UTF8NoBOM`), line-ending normalization (LF → CRLF), and multi-byte
mangling for non-ASCII characters. The resulting `git hash-object`
SHA will NOT match the original blob, the Axis-3 per-file byte audit
in Phase 3 will (correctly) fail, and the force-push must be aborted.

Use byte-preserving APIs:

```powershell
# Preferred: Copy-Item is byte-exact.
Copy-Item <source> <dest> -Force

# Fallback: WriteAllBytes from a byte buffer.
[System.IO.File]::WriteAllBytes($dest, [System.IO.File]::ReadAllBytes($source))
```

Verify **immediately** after writing:

```powershell
git hash-object $dest   # MUST match expected blob SHA
```

***

## 5. Acceptance Criteria

The restack is complete when:

1. `<sandbox>` HEAD is a descendant of the current `<team-branch>` tip.
2. All six audit axes pass (or any DIFFER is explained per §3.2).
3. Force-push succeeds under explicit user authorization.
4. The user externally verifies and authorizes the safety tag drop.

***

## 6. Related Conversations & Traceability

- Session 2026-05-16 (`<ticket-system>` ticket `<ticket-id>`): original
  derivation of the six-axis equality audit, including the modify-vs-delete
  (DU) conflict resolution and the PowerShell `$pid` collision diagnosis.

All session logs MUST be sanitized through
[`redaction-portability`](../redaction-portability/SKILL.md) before commit.
