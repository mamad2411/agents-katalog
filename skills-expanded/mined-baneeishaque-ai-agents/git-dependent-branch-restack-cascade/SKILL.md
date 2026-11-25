---
name: git-dependent-branch-restack-cascade
description: Composer — after a base branch advances (via cherry-pick
    promotion, decommission fan-out, or amend), discover every local
    and remote branch still rooted on the OLD tip, and cascade
    `rebase --onto <new-tip> <old-tip> <dependent>` across all of
    them with per-dependent patch-id parity verification and a
    per-push authorization gate. Generalizes the personal-sandbox
    restack pattern to diagnostic, feature-stack, and PR-review
    dependents.
category: Git & Repository Management
---

# Git Dependent Branch Restack Cascade Skill (v1)

> **Skill ID:** `git-dependent-branch-restack-cascade`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A base branch — typically a team / feature / ticket branch (e.g.,
`<author>-<ticket-id>`, `develop`, `main`) — has just moved from `<old-tip>`
to `<new-tip>` because one of the following ran:

- [`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md)
  fanned out commits from a parallel branch onto the canonical.
- [`git-branch-promotion`](../git-branch-promotion/SKILL.md) promoted a
  refined branch onto canonical.
- A manual cherry-pick / `commit --amend` / interactive rebase advanced the tip.

Any other branch (diagnostics, opt-in instrumentation, personal sandbox,
PR-review fork branch, downstream feature stack) that was **rooted on
`<old-tip>`** is now stale: its merge-base with the moved branch is still
`<old-tip>` instead of `<new-tip>`.

This skill discovers every such dependent and cascades the restack across
all of them with the same six-axis content-equality discipline that
[`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md)
applies to a single dependent — then gates each force-push behind explicit
user authorization.

## Composition Rationale

This skill is a **composer**. It orchestrates the following primitives
without reimplementing them:

| Composed Skill | Used for |
|---|---|
| [`git-divergence-audit`](../git-divergence-audit/SKILL.md) | Discovering candidate dependents via `merge-base` and per-branch unique-commit lists |
| [`git-rebase-standardization`](../git-rebase-standardization/SKILL.md) | The actual `rebase --onto` mechanics and conflict-resolution discipline |
| [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) | The per-dependent six-axis parity audit pattern (patch-id / files / bytes / tree / tip) |
| [`git-commit-metadata-extraction`](../git-commit-metadata-extraction/SKILL.md) | Per-commit subjects + file lists in the dependent inventory table |
| [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) | Per-push authorization gate (each dependent's force-push is one authorization) |
| [`redaction-portability`](../redaction-portability/SKILL.md) | Sanitizing any artifact produced from this workflow |

The composer **MUST NOT** reimplement merge-base discovery, rebase mechanics,
or parity-audit logic — those are the owners' jobs.

## Related Skills

- [`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md)
  — the most common upstream caller. Its Phase 4.5 hands off to this skill
  to restack any branch that was rooted on the canonical's pre-decommission tip.
- [`git-branch-promotion`](../git-branch-promotion/SKILL.md) — the inverse
  caller, also moves a canonical tip and therefore has the same dependent
  cascade obligation.
- [`git-personal-content-extraction`](../git-personal-content-extraction/SKILL.md)
  — round-based caller. After each purification round resets the team branch
  tip, this cascade restacks every dependent (personal sandbox, diagnostics,
  feature stacks) rooted on the pre-round tip before the gated force-push.

## Source Rules

| Rule File | Scope Incorporated |
| --- | --- |
| [`ai-rule-standardization-rules.md`](../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First Architecture, Layered Composition Mandate |
| [`git-rebase-standardization/SKILL.md`](../git-rebase-standardization/SKILL.md) | Backup-tag-before-rebase discipline |
| [`git-personal-sandbox-restack/SKILL.md` §3](../git-personal-sandbox-restack/SKILL.md) | Six-axis parity audit re-used per dependent |

***

## 1. When to Apply

Apply this skill when ALL of the following hold:

- A base branch tip has just moved: known `<old-tip>` SHA → known `<new-tip>` SHA.
- The new commits on the moved branch are **on top of** the old tip (the move
  was a fast-forward; if it was a rewrite, use
  [`git-rebase-standardization`](../git-rebase-standardization/SKILL.md) first).
- One or more other branches (local or remote) were last stacked on the moved
  branch at or before `<old-tip>`.
- The author wants those dependents to inherit the new commits transparently
  without a merge commit.

Do NOT apply when:

- There is exactly one dependent AND it is a `personal/<purpose>` sandbox
  — use [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md)
  directly (this skill would add only ceremony).
- The dependent intentionally diverged on purpose (e.g., it pins an old
  base for reproduction) — restacking would defeat that intent.
- The moved branch's history was rewritten (not fast-forwarded). Restacking
  needs a known `<old-tip>` to use as the `--onto` boundary; if the old tip
  is gone from the moved branch's history, recover it from `git reflog`
  first.

***

## 2. Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.23+ |
| Shell | PowerShell 5.1+ or POSIX shell |
| Tip handles | Both `<old-tip>` (e.g., from a backup tag or reflog) and `<new-tip>` SHAs in scope |
| Auth | Push permission on every dependent's remote (typically `origin` and/or `personal`) |
| State | Working tree clean (`git status --short` empty) |

***

## 3. Step-by-Step Procedure

### Phase 0 — State Capture

```powershell
$repo='<repo-path>'
$old='<old-tip-sha>'   # e.g., from backup/<branch>-pre-<operation>-<date>
$new='<new-tip-sha>'   # current tip of the moved branch
git -C $repo status --short              # MUST be empty
git -C $repo log --oneline "$old..$new"  # the new commits on the moved branch
```

### Phase 1 — Dependent Discovery

A branch `B` is a **dependent** if its merge-base with the moved branch's
new tip is exactly `<old-tip>` (or an ancestor of it that has not been
amended).

```powershell
# Inventory all candidate branches (local + remote, excluding the moved branch itself):
$candidates = git -C $repo for-each-ref --format='%(refname:short)' refs/heads refs/remotes |
              Where-Object { $_ -notmatch '^(origin/HEAD|<moved-branch>|origin/<moved-branch>)$' }

$dependents = @()
foreach ($b in $candidates) {
    $mb = git -C $repo merge-base $b $new 2>$null
    if ($mb -eq $old) { $dependents += $b }
}
$dependents
```

For each dependent, capture its unique commits relative to `<old-tip>`:

```powershell
foreach ($d in $dependents) {
    Write-Host "--- $d ---"
    git -C $repo log --oneline "$old..$d"
}
```

Build the **Dependent Inventory** table and present it to the author for
authorization BEFORE any mutation:

| # | Dependent | Remote | Unique commits | Owner | Notes |
|---|---|---|---|---|---|

> **Local vs remote duplicates**: When a local branch `B` and its remote
> tracking branch `origin/B` (or `personal/B`) both appear, restack ONLY
> the local one; the force-push in Phase 4 propagates the new history to
> the remote.

### Phase 2 — Per-Dependent Backup Tags

```powershell
$today = Get-Date -Format 'yyyy-MM-dd'
foreach ($d in $dependents) {
    $safe = ($d -replace '[/\\]', '-')
    git -C $repo tag "backup/$safe-pre-restack-$today" $d
}
git -C $repo tag --list "backup/*-pre-restack-$today"
```

Backup tags are LOCAL ONLY. They are dropped only after Phase 5 external
verification by the author.

### Phase 3 — Per-Dependent Restack

For each dependent in the inventory:

```powershell
# If the dependent is a remote-only branch, materialize it locally first:
# git -C $repo checkout -B <local-name> <remote>/<branch-name>

git -C $repo rebase --onto $new $old <dependent>
```

#### 3a — Conflict resolution

Most cascade restacks are conflict-free because the dependents typically
touch disjoint files from the new commits. When a conflict does occur:

- **Modify-vs-Delete (DU)** — delegate to
  [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) §2a
  recipe (`git add` to keep the dependent's modification, `git rm` to honor
  the deletion, then
  `git -c core.editor=true rebase --continue` to preserve the message).
- **Content conflict** — STOP. The dependent and the moved branch genuinely
  touch the same lines. Restart with the author in the loop; do not silently
  apply `-X theirs` or `-X ours`.

#### 3b — Per-dependent six-axis parity audit

Delegate to [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) §3.

A minimal subset that suffices for short dependents (≤ 3 commits):

```powershell
$oldTag = "backup/$($d -replace '[/\\]','-')-pre-restack-$today"
$oldIds = git -C $repo log --reverse --format='%H' "$old..$oldTag" |
          ForEach-Object { (git -C $repo show $_ | git -C $repo patch-id --stable).Split(' ')[0] }
$newIds = git -C $repo log --reverse --format='%H' "$new..$d" |
          ForEach-Object { (git -C $repo show $_ | git -C $repo patch-id --stable).Split(' ')[0] }
for ($i=0; $i -lt $oldIds.Count; $i++) {
    $eq = if ($oldIds[$i] -eq $newIds[$i]) {'EQUAL'} else {'DIFFER'}
    Write-Host ("pair {0}: {1}" -f ($i+1), $eq)
}
```

For longer dependents (≥ 4 commits) or when any pair shows DIFFER, run the
full six-axis audit from
[`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) §3
and apply the legitimate-divergence rubric (§3.2) before proceeding.

> **PowerShell `$pid` pitfall**: Variable names starting with `$pid` shadow
> PowerShell's read-only built-in process-ID variable. Use `$pidR`, `$pidL`,
> `$pidEq`, `$pidValue`. See
> [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) §4.2.

### Phase 4 — Per-Dependent Force-Push (Authorization Gate)

Force-pushes MUST be gated. They MAY be presented as a single batched
authorization (one prompt covering all dependents) when all parity audits
in Phase 3b passed — this avoids friction for the common case (5+ clean
restacks).

```powershell
# Example batch — author authorizes all at once after audit passes:
git -C $repo push --force-with-lease origin   <dependent-1>
git -C $repo push --force-with-lease personal <dependent-2>
git -C $repo push --force-with-lease origin   <dependent-3>
```

`--force-with-lease` is MANDATORY. `--force` is FORBIDDEN — it bypasses the
"someone-else-pushed-since-your-last-fetch" safety net.

If ANY parity audit in Phase 3b showed unexplained DIFFER, that dependent's
push MUST be gated SEPARATELY with the audit table presented to the author.

### Phase 5 — External Verification & Safety Tag Drop

After all force-pushes succeed, the author externally verifies (e.g.,
GitHub Web UI):

- Each dependent's remote tip equals the local post-restack tip.
- No reflog rescue is needed.

Then drop the safety tags:

```powershell
git -C $repo tag --list "backup/*-pre-restack-$today" |
    ForEach-Object { git -C $repo tag -d $_ }
```

***

## 4. Pitfalls & Recovery

### 4.1 Remote-only dependent never materialized locally

Symptom: Phase 1 lists `origin/<branch>` but `git rebase --onto ... origin/<branch>`
operates on a detached HEAD without updating the remote-tracking ref.

Fix: materialize a local branch first:

```powershell
git -C $repo checkout -B <branch> origin/<branch>
git -C $repo rebase --onto $new $old <branch>
git -C $repo push --force-with-lease origin <branch>
```

### 4.2 Dependent's merge-base is not exactly `<old-tip>`

Symptom: `git merge-base <dep> <new>` returns an SHA earlier than `<old-tip>`.

Cause: the dependent was rooted further back than the operation assumed.
Restacking onto `<new-tip>` with `--onto <old-tip>` would skip legitimate
commits that lived between the dependent's true base and `<old-tip>`.

Fix: use the dependent's true merge-base as the `--onto` boundary:

```powershell
$trueBase = git -C $repo merge-base <dep> <old-tip>
git -C $repo rebase --onto $new $trueBase <dep>
```

### 4.3 LFS-locking warning on first push to a new destination

Cosmetic only — push still succeeds. See
[`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md) §4.3.

### 4.4 Force-push rejected (lease stale)

Symptom: `! [rejected] <dep> -> <dep> (stale info)`.

Cause: someone (or an earlier session) pushed to that remote ref since the
last fetch.

Fix:

```powershell
git -C $repo fetch <remote> <dep>
# Re-run the merge-base / parity check before re-attempting the force-push.
```

Do NOT escalate to plain `--force` to bypass the lease.

### 4.5 Recovery — I forgot to cascade (chain broken by independent rebases)

Symptom: A chain `A ⊂ B ⊂ C` (where each `⊂` means "is contained in") was
rewritten one layer at a time — for example, the same surgical edit (drop a
file, reword a commit) was applied via independent `rebase -i` on each
branch instead of editing the base once and cascading. Result:

- All three branches' tips changed in the desired way (file gone, message
  fixed).
- BUT the chain is broken: `git merge-base B A` and `git merge-base C B` no
  longer return each other's tips — they point back to a common ancestor
  from BEFORE the edit. Each branch is now its own divergent line.

This is structurally invisible to a per-branch check (each tip looks fine);
it only surfaces when you ask the relational question `head..base` /
`base..head`.

**Diagnosis** — run the chain integrity check:

```powershell
foreach ($pair in @(
    @('origin/<mid>',  'origin/<base>'),
    @('origin/<head>', 'origin/<mid>')
)) {
    $head = $pair[0]; $base = $pair[1]
    $ah   = git rev-list --count "$base..$head"
    $bh   = git rev-list --count "$head..$base"
    "{0,-50} ahead={1} behind={2}" -f "$head vs $base", $ah, $bh
}
```

If any pair shows `behind > 0`, the chain is broken (the dependent contains
commits the base does not — the inverse of subset).

**Recovery** — rebuild each layer on top of its corrected ancestor by
patch-id-based cherry-picking, NOT by `rebase --onto` (because the OLD-TIP
boundary that `--onto` needs no longer exists on the rewritten branches).

Step 1 — identify each layer's unique-to-this-layer commits via `git cherry`
(compares by patch-id, so it correctly skips commits that were re-applied
to the new base):

```powershell
# Commits on <mid> NOT on <base> (by patch-id):
git cherry -v origin/<base> origin/<mid> | Where-Object { $_ -match '^\+' }

# Commits on <head> NOT on <mid> (by patch-id):
git cherry -v origin/<mid> origin/<head> | Where-Object { $_ -match '^\+' }
```

`git cherry` output: lines starting with `+` are commits unique to the head;
`-` means "already on base by patch-id, skip". The `+` SHAs are the
recipe.

Step 2 — verify author and intent for each unique SHA before cherry-picking
(some commits may be team-mate work or legitimately discardable noise):

```powershell
foreach ($sha in $uniqueShas) {
    git log -1 --format='%h  %an  %ad  %s' --date=short $sha
}
```

Step 3 — rebuild each layer in an isolated worktree (per §4.6), starting
from the corrected base:

```powershell
# In the isolated worktree:
git checkout -B <mid>  origin/<base>         # NEW base
git cherry-pick <mid-unique-shas-in-order>   # from Step 1

git checkout -B <head> HEAD                  # new <mid> tip
git cherry-pick <head-unique-shas-in-order>
```

Step 4 — verify chain restored, then push each layer with `--force-with-lease`:

```powershell
# Should show 0 behind everywhere:
foreach ($pair in @(
    @('<mid>',  'origin/<base>'),
    @('<head>', '<mid>')
)) {
    $h = $pair[0]; $b = $pair[1]
    $ah = git rev-list --count "$b..$h"
    $bh = git rev-list --count "$h..$b"
    "{0,-40} ahead={1} behind={2}" -f "$h vs $b", $ah, $bh
}

git push origin <mid>  --force-with-lease
git push origin <head> --force-with-lease
```

**Why `git cherry` instead of `merge-base`**: After independent rebases, the
dependent's pre-rebase SHAs no longer exist in any branch's reachable
history — only their patch-equivalent counterparts do. `merge-base` finds
the last common ancestor by SHA (which is now ancient pre-edit history),
which would re-apply the entire rewritten history and double-apply the
edits. `git cherry` compares by stable patch-id, correctly identifying
which commits are genuinely unique to each layer.

**Prevention**: ALWAYS apply this skill (or its single-dependent ancestor
[`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md))
immediately after any base-branch edit when dependents exist. The cost of a
Phase 1 dependent discovery is seconds; the cost of recovery is minutes plus
risk of misclassifying authorship.

### 4.6 Worktree isolation for branch operations under IDE lock contention

Symptom: `git checkout`, `git rebase`, or `git cherry-pick` in the main
working tree fails with `Deletion of directory '<path>' failed. Should I
try again? (y/n)` — typically when VS Code / Eclipse / a JVM is indexing
the workspace.

Fix: perform the operation in a detached throwaway worktree outside the
IDE's filesystem watch scope:

```powershell
$wt = 'C:\temp\gitwork-<purpose>'
if (Test-Path $wt) { Remove-Item $wt -Recurse -Force }
git -C $repo worktree add --detach $wt
Push-Location $wt

# do the rebase / cherry-pick here

Pop-Location
git -C $repo worktree remove $wt --force
```

When the target branch is already checked out in the main worktree, the
worktree's `git checkout -B <branch> <remote>/<branch>` will fail with
`fatal: '<branch>' is already used by worktree at ...`. In that case, work
in detached HEAD and push by SHA:

```powershell
# In the isolated worktree, detached HEAD on the target ref:
git checkout --detach origin/<branch>
# ... do the rebase / cherry-pick ...
$newTip = git rev-parse HEAD
git push origin "${newTip}:refs/heads/<branch>" --force-with-lease
```

The `<sha>:refs/heads/<branch>` push form updates the remote branch ref
without needing a local branch ref to advance.

After Phase 5, sync the main-worktree branch to the remote tip:

```powershell
git -C $repo checkout <branch>
git -C $repo reset --hard origin/<branch>
```

### 4.7 Dependent rooted on a non-tip commit that was rewritten by the upstream history edit

**Symptom** (preserved verbatim from session 2026-05-30 on `<ORG-USER>/<REPO>`; sanitized via [`redaction-portability`](../redaction-portability/SKILL.md)):

> Branch **A** has commit **X** on top of commit **H**, and **H** is in `master` (NOT the tip).
> Branch **B** has commit **Y** on top of `master` tip.
>
> A naive cascade — `git rebase --onto <new-master> <old-master> <branch>` for every dependent — puts **both** X and Y on top of the new master tip.
>
> - For **B**: correct (its old parent WAS the old tip; the new tip is the rewritten equivalent of that old tip).
> - For **A**: WRONG. X must land on **H'**, the rewritten equivalent of H *inside* the new master, NOT on the new tip. Otherwise X is silently lifted past commits it never lived on top of.

**When this fires**: an upstream operation **rewrote** mid-history (e.g., this skill's caller dropped or split a commit with `git rebase --onto`, OR a `cherry-pick` chain replaced a range), not just appended new tip commits. Dependents whose merge-base with the moved branch was an *interior* commit are at risk; dependents whose merge-base WAS exactly `<old-tip>` are safe under standard §3.

**Diagnosis**:

```powershell
# Fast check: is the dependent's old parent still reachable from the new tip?
git merge-base --is-ancestor <H> <new-master>
# Non-zero exit ⇒ H was rewritten away; you need H'.
```

**Locating H' (SSOT — use existing primitives, do NOT write a new equivalence script)**:

1. **Fast path — subject grep**. Single-line commit subjects survive most rewrites verbatim:

    ```powershell
    git log --format='%H %s' <new-master> |
        Select-String -SimpleMatch '<H-subject>'
    ```

    Exactly one hit ⇒ that SHA is H'. Multiple or zero hits ⇒ fall through.

2. **Patch-equivalence path — `git cherry`** (already documented in §4.5, which uses it for the chain-break case):

    ```powershell
    git cherry -v <old-base> <new-master> |
        Where-Object { $_ -match '^- ' }
    ```

    `git cherry` lines starting with `-` are commits present on `<new-master>` by patch-id that have an equivalent ancestor in `<old-base>` — among those is H'. Cross-reference by subject or author/date to identify it.

3. **Full audit path — pairwise patch-id walk**: invoke
   [`git-commit-comparison-audit/scripts/equivalence-check.ps1`](../git-commit-comparison-audit/scripts/equivalence-check.ps1)
   pairing each old-master commit against new-master commits by patch-id. Owned by `git-commit-comparison-audit` — do not duplicate here.

**Fix**:

```powershell
git rebase --onto <H'> <H> <branch-A>
```

Then run the standard Phase 3b parity audit. The pre/post unique-commit patch-id sequence MUST equal — if not, the chosen H' is wrong and you should iterate (often by stepping back to candidate H'+1 or H'-1).

**Force-push gate** (Phase 4): when a dependent required §4.7 treatment (not just §3), its push MUST be authorized **separately** from the batch push, with the diagnosis (chosen H', parity result) presented to the author. This is the same separate-gate rule that §3b applies to DIFFER parity.

**Distinction from §4.2 and §4.5**:

- §4.2 (merge-base earlier than `<old-tip>`): dependent was rooted *further back* than the operation assumed, but H itself is still reachable from `<new-tip>`. Fix uses the dependent's *true* merge-base directly — no equivalent-finding needed.
- §4.5 (independent-rebase chain break): the chain `A ⊂ B ⊂ C` was rewritten one layer at a time; recovery rebuilds via `git cherry`-driven cherry-pick. §4.7 is upstream-side: ONE rewrite, multiple dependents — one of which lands wrong if cascade is naive.

**Composition by Higher-Level Skills**:

- [`git-submodule-misconfiguration-audit-and-revert`](../git-submodule-misconfiguration-audit-and-revert/SKILL.md) Phase 6 — invokes this cascade skill and explicitly classifies each dependent as "old-tip-rooted" (§3) vs "mid-history-rooted" (this §4.7) before per-dependent restack.

***

## 5. Acceptance Criteria

The cascade is complete when:

1. Every dependent's merge-base with the moved branch's new tip equals
   `<new-tip>` (no longer `<old-tip>`).
2. Every dependent's patch-id sequence matches the pre-restack sequence —
   or any DIFFER is explained by the legitimate-divergence rubric.
3. Every dependent's force-push succeeded with `--force-with-lease`.
4. The author externally verified each remote and authorized safety tag drop.

***

## 6. Related Conversations & Traceability

- Session 2026-05-16 (decommission of `<canonical>-skill`): the canonical
  `<author>-<ticket>` branch advanced by one cherry-pick (`ICEDAMOS0038`)
  while both `personal/sandbox` (9 personal commits) and
  `<author>-<ticket>-diagnostics` (1 diagnostic commit) were still rooted on
  the pre-decommission tip. Both restacked cleanly via `rebase --onto`,
  patch-id parity verified per dependent, force-pushed under a single
  batched authorization. Original derivation of the cascade pattern as a
  distinct composer separate from `git-personal-sandbox-restack`.

All session logs MUST be sanitized through
[`redaction-portability`](../redaction-portability/SKILL.md) before commit.
