---
name: git-absorbed-branch-decommission
description: Composer — safely delete a stale branch whose content
    has been fully absorbed by a sibling / successor branch, via
    a two-step audit (cheap ancestor check, then patch-id
    equivalence + tip file-set parity when SHAs differ). Distinct
    from `git-parallel-branch-decommission` (which fans out content
    to multiple destinations) and `git-branch-promotion` (which
    replaces canonical with a refined branch).
category: Git & Repository Management
---

# Git Absorbed Branch Decommission Skill (v1)

> **Skill ID:** `git-absorbed-branch-decommission`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A stale branch `<stale>` is a candidate for deletion because its content
has already been **absorbed** by a successor branch `<live>`. Absorption
happens via one of two mechanisms:

1. **Direct ancestor** — `<live>` is strictly ahead of `<stale>` and
   contains every `<stale>` commit by SHA. Confirmed via
   `git rev-list --count <live>..<stale> == 0`. This is the trivial case
   produced by a clean merge / fast-forward / squash-then-merge of
   `<stale>` into `<live>` or a trunk that `<live>` later inherited.
2. **Patch-id equivalence** — `<live>` was created via a rollback /
   cherry-pick workflow that re-applied every `<stale>` commit under new
   SHAs. `<stale>` is NOT an ancestor (`rev-list` count > 0), but every
   unique commit has a patch-id match on `<live>`. Common when an
   integration team starts a clean replacement branch (e.g.,
   `<feature>_via_rollback`) and re-cherry-picks contributors' fixes onto it.

This skill verifies absorption with the cheapest test that suffices, then
deletes `<stale>` from every remote and locally with a backup tag retained
until external verification by the author.

## Composition Rationale

This skill is a **composer**. It orchestrates the following primitives
without reimplementing them:

| Composed Skill | Used for |
|---|---|
| [`git-divergence-audit`](../git-divergence-audit/SKILL.md) | Merge-base / left-right ahead-behind discovery |
| [`git-branch-promotion`](../git-branch-promotion/SKILL.md) §2 | The `git log --cherry-pick --left-only` patch-id equivalence query (reused, not reimplemented) |
| [`git-commit-metadata-extraction`](../git-commit-metadata-extraction/SKILL.md) | Per-commit subject + file list in the audit table |
| [`redaction-portability`](../redaction-portability/SKILL.md) | Sanitizing any artifact produced from this workflow |

The composer **MUST NOT** reimplement merge-base discovery, patch-id
computation, or rebase mechanics — those are the owners' jobs.

## Related Skills

- [`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md)
  — the **fan-out** sibling. Use that skill when `<stale>` has commits
  that DO NOT have equivalents on `<live>` and must be distributed across
  canonical + opt-in + personal-sandbox destinations. Use **this skill**
  when every `<stale>` commit is already absorbed by `<live>`.
- [`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md)
  — run AFTER this skill if `<stale>` had any dependents.

## Source Rules

| Rule File | Scope Incorporated |
| --- | --- |
| [`ai-rule-standardization-rules.md`](../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First Architecture, Layered Composition Mandate |
| [`git-branch-promotion/SKILL.md` §2](../git-branch-promotion/SKILL.md) | Patch-id equivalence query |
| [`git-commit-edit/SKILL.md` Step 7b](../git-commit-edit/SKILL.md) | Deletion-authorization gate |

***

## 1. When to Apply

Apply this skill when ALL of the following hold:

- A branch `<stale>` is a candidate for deletion.
- A sibling / successor branch `<live>` is claimed to contain all of
  `<stale>`'s content (directly or via re-cherry-pick).
- The author wants explicit verification before deleting.

Do NOT apply when:

- `<stale>` has unique commits that are NOT on `<live>` and the author
  wants to KEEP that work — use
  [`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md)
  to fan it out instead.
- `<stale>` IS the live branch and the goal is to promote a refined
  branch on top of it — use
  [`git-branch-promotion`](../git-branch-promotion/SKILL.md).
- The branch is `main`, `master`, `develop`, a release branch, or any
  branch consumed by an integration / CI / downstream team — STOP and
  confirm with the consumers first regardless of audit results.

***

## 2. Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.23+ |
| Shell | PowerShell 5.1+ or POSIX shell |
| Auth | Delete permission on every remote that hosts `<stale>` |
| State | Local clone has up-to-date refs (`git fetch <remote> --prune` already run) |

***

## 3. Step-by-Step Procedure

### Phase 0 — State Capture

```powershell
$repo='<repo-path>'
$stale='origin/<stale>'        # or 'personal/<stale>' as applicable
$live='origin/<live>'
git -C $repo fetch --all --prune | Out-Null
git -C $repo log -1 --oneline $stale
git -C $repo log -1 --oneline $live
```

### Phase 1 — Cheap Ancestor Check (Tier 1)

```powershell
$ahead  = git -C $repo rev-list --count "$live..$stale"
$behind = git -C $repo rev-list --count "$stale..$live"
"$stale  ahead=$ahead  behind=$behind  vs  $live"
```

| Outcome | Meaning | Next step |
|---|---|---|
| `ahead = 0` | `<stale>` is an ancestor of `<live>` — every commit is contained by SHA | **Skip to Phase 3** (deletion is trivially safe) |
| `ahead > 0` | `<stale>` has commits not on `<live>` by SHA | **Proceed to Phase 2** (those commits may still exist by patch-id) |

### Phase 2 — Patch-ID Equivalence + Tip Parity (Tier 2)

Required only when `ahead > 0`. Proves that every "unique" commit on
`<stale>` has a patch-id match on `<live>`, AND that `<live>`'s tip has
no missing files relative to `<stale>`'s tip.

#### 2a — Patch-ID Equivalence Audit

Delegate to [`git-branch-promotion`](../git-branch-promotion/SKILL.md) §2
or run inline:

```powershell
$mb = git -C $repo merge-base $stale $live
# Truly unique on stale after patch-id filtering:
$trulyUnique = git -C $repo log --cherry-pick --left-only --no-merges `
                   --format='%H' "$stale...$live"
$count = ($trulyUnique | Measure-Object).Count
"Truly unique on $stale (after patch-id) : $count"
```

If `$count > 0`, STOP — those commits would be lost. Either:

- Re-classify and apply [`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md)
  to fan them out, OR
- Confirm with the author that the truly-unique commits are
  intentionally obsolete before continuing.

For full forensic detail (per-commit pairing with the equivalent SHA on
`<live>`), build the patch-id map:

```powershell
$livePids = @{}
git -C $repo log --format='%H' "$mb..$live" | ForEach-Object {
    $pid_ = (git -C $repo show $_ | git -C $repo patch-id --stable).Split(' ')[0]
    if ($pid_) { $livePids[$pid_] = $_ }
}
'{0,-12} {1,-12} {2,-7} {3,-7} {4}' -f 'SRC','DEST','Files','Bytes','Subject'
foreach ($sha in (git -C $repo log --reverse --format='%H' "$live..$stale")) {
    $pid_ = (git -C $repo show $sha | git -C $repo patch-id --stable).Split(' ')[0]
    $subj = git -C $repo log -1 --format='%s' $sha
    $dest = $livePids[$pid_]
    if ($dest) {
        $sf = @(git -C $repo show --pretty=format: --name-only $sha  | Where-Object { $_ })
        $df = @(git -C $repo show --pretty=format: --name-only $dest | Where-Object { $_ })
        $fEq = if ((Compare-Object ($sf|Sort-Object) ($df|Sort-Object)) -eq $null) {'SAME'} else {'DIFF'}
        $bEq = 'SAME'
        foreach ($f in $sf) {
            $sc = git -C $repo show "${sha}:${f}"  2>$null
            $dc = git -C $repo show "${dest}:${f}" 2>$null
            if ((($sc -join "`n") -ne ($dc -join "`n"))) { $bEq='DIFF'; break }
        }
        '{0,-12} {1,-12} {2,-7} {3,-7} {4}' -f $sha.Substring(0,10), $dest.Substring(0,10), $fEq, $bEq, $subj
    } else {
        '{0,-12} {1,-12} {2,-7} {3,-7} {4}' -f $sha.Substring(0,10), 'MISS', '-', '-', $subj
    }
}
```

> **PowerShell pitfall**: NEVER name the patch-id variable `$pid` — it's
> a read-only built-in (process ID). Use `$pid_`, `$pidR`, `$pidL`. See
> [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) §4.2.

Any `MISS` row is a real loss — STOP and re-classify.

#### 2b — Tip File-Set Parity

A branch can have full patch-id equivalence yet still hold files
`<live>` lacks (e.g., `.project`, IDE artifacts, build configs). Verify
the tip file-set:

```powershell
$staleFiles = git -C $repo ls-tree -r --name-only $stale | Sort-Object
$liveFiles  = git -C $repo ls-tree -r --name-only $live  | Sort-Object
$diff = Compare-Object $staleFiles $liveFiles
$diff | ForEach-Object { "$($_.SideIndicator)  $($_.InputObject)" }
```

| Side-indicator | Meaning | Action |
|---|---|---|
| `<=` (left-only, on `$stale`) | File would be LOST if `$stale` is deleted | STOP — extract those files via [`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md) Phase 3c (personal sandbox) before deleting |
| `=>` (right-only, on `$live`) | `$live` strictly supersedes `$stale` | Safe — deletion loses nothing |
| empty | Tip file-sets identical | Safe |

> **Subtle case**: Even when `<=` rows exist, deletion may still be
> intentional (e.g., the missing files are obsolete IDE artifacts the
> author is fine to discard). The skill does NOT decide — the author
> decides after seeing the list.

### Phase 3 — Backup Tag (Recovery Handle)

```powershell
$today = Get-Date -Format 'yyyy-MM-dd'
$safeName = $stale -replace '^.*?/', ''   # strip 'origin/' prefix
git -C $repo tag "backup/${safeName}-pre-decom-$today" $stale
git -C $repo tag --list "backup/${safeName}-pre-decom-$today"
```

LOCAL ONLY. Dropped only after Phase 5 external verification.

### Phase 4 — Deletion (Authorization Gate)

The author MUST explicitly authorize the deletion AFTER reviewing the
Phase 1 (Tier 1) and/or Phase 2 (Tier 2) audit output.

```powershell
# Remote deletion:
git -C $repo push origin --delete <stale-branch-name>
# If <stale> also exists on the personal remote (e.g., from a prior
# 'git push --all personal' incident), delete it there too:
git -C $repo ls-remote --heads personal <stale-branch-name>
# If non-empty:
# git -C $repo push personal --delete <stale-branch-name>

# Prune stale tracking refs:
git -C $repo fetch --all --prune | Out-Null

# Local branch deletion (only if a local copy exists):
git -C $repo branch -D <stale-branch-name> 2>$null
```

### Phase 5 — External Verification & Cleanup

The author externally verifies (e.g., GitHub Web UI):

- `<stale>` is absent from every remote.
- `<live>` is unaffected.
- No CI / integration / downstream consumer reports a broken reference.

Then drop the backup tag:

```powershell
git -C $repo tag -d "backup/${safeName}-pre-decom-$today"
```

***

## 4. Pitfalls & Recovery

### 4.1 `<stale>` is referenced by an open PR

Symptom: GitHub returns `422 Branch is the base/head of an open PR`.

Fix: close or retarget the PR first, then re-attempt deletion. Never
force-delete via the API to bypass.

### 4.2 `<stale>` has dependents (other branches rooted on it)

Symptom: After deletion, a dependent's `merge-base` query against the
remote fails or its next rebase loses context.

Fix: BEFORE running this skill, enumerate dependents via
[`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md)
§Phase 1 with `<stale>` as the `<moved-branch>`. Restack every dependent
onto `<live>` first, then proceed.

### 4.3 Tip file-set diff shows files unique to `<stale>`

Symptom: Phase 2b shows `<=` rows.

Decision tree:

1. If the files are PRODUCTION SOURCE → STOP. Fan-out via
   [`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md).
2. If the files are PERSONAL ARTIFACTS (IDE configs, build configs,
   skills, docs) → extract via
   [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md)
   and then proceed.
3. If the files are LEGITIMATELY OBSOLETE (e.g., a `.target` for an
   abandoned Eclipse version, a discarded experiment) → author confirms,
   then proceed.

### 4.4 Recovery from accidental deletion

```powershell
# Restore from the backup tag:
git -C $repo branch <stale-branch-name> "backup/${safeName}-pre-decom-$today"
git -C $repo push origin <stale-branch-name>
```

Recovery is possible until BOTH:

- The backup tag is dropped (Phase 5).
- The remote runs `git gc` and the dangling commits expire from its
  reflog (typically 30 days for a quiet repo).

***

## 5. Acceptance Criteria

The decommission is complete when:

1. Tier 1 (`ahead == 0`) or Tier 2 (patch-id `truly unique == 0` AND tip
   file-set has no `<=` rows OR all `<=` rows are author-confirmed
   obsolete).
2. Backup tag created.
3. Author explicitly authorized deletion.
4. `<stale>` is absent from every remote and locally.
5. Author externally verified the remote and authorized backup tag drop.

***

## 6. Related Conversations & Traceability

- Session 2026-05-16 (cleanup of personal-named branches in team repo):
  Tier 1 verification deleted 0 branches (4 stale `<author>-<ticket>`
  branches were KEPT per author preference despite `ahead=0`). Tier 2
  verification successfully decommissioned `eclipse_4_33` after proving
  all 19 unique commits had patch-id equivalents on
  `eclipse_4_33_via_rollback` (19/19 SAME files, SAME bytes) and the tip
  file-set diff showed all unique files were on rollback's side (none on
  the stale branch). Original derivation of the two-tier audit pattern as
  a distinct composer separate from `git-parallel-branch-decommission`.

All session logs MUST be sanitized through
[`redaction-portability`](../redaction-portability/SKILL.md) before commit.
