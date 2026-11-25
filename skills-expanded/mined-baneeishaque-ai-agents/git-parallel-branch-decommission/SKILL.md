---
name: git-parallel-branch-decommission
description: Composer — decommission a parallel feature branch (e.g.,
    a long-lived `<feature>-ai_demo` sibling of the canonical
    `<feature>` branch) by classifying each unique commit by
    content type and fanning it out to multiple destinations —
    canonical team branch, opt-in team branch for non-default
    instrumentation, personal sandbox for personal-only docs —
    with mixed commits split per file, parity-verified against
    every removable item, and gated authorization before deletion.
category: Git & Repository Management
---

# Git Parallel Branch Decommission Skill (v1)

> **Skill ID:** `git-parallel-branch-decommission`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A parallel feature branch (typically created early in a feature's life as a
"throwaway" sibling — e.g., `<canonical>-ai_demo`, `<canonical>-spike`,
`<canonical>-poc`) has accumulated genuine commits that mix multiple concerns:

- New functional code that belongs on the **canonical team branch**.
- Optional debug / diagnostic instrumentation that the team may want
  **opt-in** but should not pollute the default branch.
- Personal documentation, skill files, and other author-only artifacts
  that belong on a **personal sandbox**, not the team repo.
- One or more **mixed commits** that contain a combination of the above
  in a single SHA.

The author wants to delete the parallel branch but cannot afford to lose any
of its content. This skill orchestrates the N-way fan-out:

1. Audit divergence and classify every unique commit by content type.
2. Verify each destination branch exists (or will be created) and is reachable.
3. Cherry-pick / split commits into the correct destinations in the correct
   order, with conflict-resolution strategies appropriate per destination.
4. Verify every removable item has a verified equivalent on its destination
   (parity gate).
5. Push each destination under a separate authorization, then delete the
   parallel branch from every remote and locally.

## Composition Rationale

This skill is a **composer** that orchestrates the following primitives
without reimplementing them:

| Composed Skill | Used for |
|---|---|
| [`git-divergence-audit`](../git-divergence-audit/SKILL.md) | Identifying merge-base and the per-side unique commit lists |
| [`git-commit-metadata-extraction`](../git-commit-metadata-extraction/SKILL.md) | Extracting subjects, file lists, and dates for classification |
| [`git-branch-promotion`](../git-branch-promotion/SKILL.md) | Inverse composer (single-destination promotion) — referenced for parity-verification mechanics |
| [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md) | The destination personal sandbox layer (creation, dual-remote, push hygiene) |
| [`git-history-refinement`](../git-history-refinement/SKILL.md) | The sandbox-rebuild fallback when the sandbox already contains the parallel-branch history and must be rebuilt on the merge-base |
| [`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md) | Phase 3.5 — cascade-restack every dependent branch still rooted on the pre-decommission canonical tip |
| [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) | Per-push authorization gate (each push is one authorization) |
| [`redaction-portability`](../redaction-portability/SKILL.md) | Sanitizing any artifact produced from this workflow |

The composer **MUST NOT** reimplement divergence audit, cherry-pick mechanics,
sandbox provisioning, or push authorization — those are the owners' jobs.

## Related Skills

- [`git-absorbed-branch-decommission`](../git-absorbed-branch-decommission/SKILL.md)
  — the **absorbed-content** sibling. Use that skill when every unique
  commit on the parallel branch already has a patch-id equivalent on a
  live successor (e.g., the integration team re-cherry-picked your
  fixes into a `_via_rollback` branch). It deletes safely without
  fan-out. Use THIS skill when at least one unique commit needs to be
  preserved.
- [`git-rebase-standardization`](../git-rebase-standardization/SKILL.md) —
  when the parallel branch's commits need re-ordering, not classification.
- [`git-personal-content-extraction`](../git-personal-content-extraction/SKILL.md)
  — the **inverse-direction sibling**. Use that skill when there is NO parallel
  branch to delete: instead, a single team / feature / ticket branch carries
  mixed team + personal commits that must be purified IN PLACE while the
  personal commits are slot-inserted at their original chronological position
  on a long-lived `personal/sandbox` branch. This skill DELETES a parallel
  branch; that skill KEEPS the team branch alive.

## Source Rules

| Rule File | Scope Incorporated |
| --- | --- |
| [`ai-rule-standardization-rules.md`](../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First Architecture, Layered Composition Mandate |
| [`git-commit-edit/SKILL.md` Step 7b / Step 8](../git-commit-edit/SKILL.md) | Push-authorization gate (re-applied per destination) |
| [`git-divergence-audit/SKILL.md` §3](../git-divergence-audit/SKILL.md#3-asset-auditing-unit-by-unit) | Unit-by-unit classification matrix |

***

## 1. When to Apply

Apply this skill when ALL of the following hold:

- A parallel branch exists alongside a canonical branch with a common merge-base.
- The parallel branch has commits unique to it that the author does NOT want
  to discard.
- Those unique commits fall into **two or more** destination categories
  (canonical / opt-in team / personal sandbox).
- One or more of those commits is **mixed** (multiple categories in one SHA).
- The author intends to delete the parallel branch after the fan-out.

Do NOT apply when:

- All parallel-branch commits belong on the same destination — use
  [`git-branch-promotion`](../git-branch-promotion/SKILL.md) instead.
- The parallel branch is to be kept (just rebased / refined) — use
  [`git-rebase-standardization`](../git-rebase-standardization/SKILL.md) or
  [`git-history-refinement`](../git-history-refinement/SKILL.md).
- The parallel branch is throwaway with no salvageable content — just
  `git branch -D` it after authorization.

***

## 2. Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.23+ (for `--show-current`) |
| Shell | PowerShell 5.1+ or POSIX shell |
| Auth | Push permission on all destination remotes; delete permission on the parallel branch's remote(s) |
| Sandbox readiness | If a personal sandbox is a destination, the prerequisites in [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md) §2 are satisfied |

***

## 3. Step-by-Step Procedure

### Phase 0 — Backup & State Capture

#### 0a — Safety tags on EVERY branch that will be mutated

```powershell
$repo='<repo-path>'
$today = Get-Date -Format 'yyyy-MM-dd'
git -C $repo tag "backup/<parallel-branch>-pre-decom-$today"   <parallel-branch>
git -C $repo tag "backup/<canonical>-pre-decom-$today"         <canonical>
# If a sandbox or opt-in branch already exists and will be mutated:
git -C $repo tag "backup/<sandbox>-pre-decom-$today"           <sandbox>
```

These tags are LOCAL ONLY. They are dropped only after the user verifies the
remote state externally (e.g., in the GitHub Web UI).

#### 0b — Working tree must be clean

```powershell
git -C $repo status --short
# Output MUST be empty. If not, stash or commit before proceeding.
```

### Phase 1 — Divergence & Classification

#### 1a — Find merge-base and per-side unique commits

Delegate to [`git-divergence-audit`](../git-divergence-audit/SKILL.md) §2.
The output is two lists, **oldest first**:

- `parallel_unique[]` — commits on `<parallel-branch>` not on `<canonical>`.
- `canonical_unique[]` — commits on `<canonical>` not on `<parallel-branch>`.

#### 1b — Classify each `parallel_unique[i]` by content type

For each commit, inspect file paths and message and assign exactly ONE
**primary destination** plus optional **co-destinations** for mixed commits:

| Content Pattern | Primary Destination |
|---|---|
| Functional source code (production paths) | `<canonical>` |
| Test code that complements functional code | `<canonical>` |
| Debug / diagnostic instrumentation guarded by env var or constant | `<canonical>-diagnostics` (opt-in team branch) |
| Skill files (`.agents/skills/**`), personal docs, IDE artifacts | `<sandbox>` (personal) |
| Mixed (≥2 of the above in one SHA) | **SPLIT** — every category gets a slice |
| Pure style/format with no new logic | `<canonical>` (unless author prefers to drop) |

The author MUST review and authorize the classification table before any
cherry-pick runs. Present it as:

| # | SHA (short) | Title | Files (count) | Primary | Co-Dest | Disposition |
|---|---|---|---|---|---|---|

### Phase 2 — Plan Verification (Parity Pre-flight)

For every commit destined for **DROP** (e.g., because its functional content
already exists on `<canonical>` via an equivalent commit), the agent MUST
**verify content parity BEFORE the commit is dropped**:

```powershell
git -C $repo diff <parallel-sha> <canonical-equivalent-sha> -- <path>
```

The diff MUST be empty (whitespace-only is acceptable only if the author
explicitly authorizes `-w` semantics). **A non-empty diff means the content
is NOT preserved on canonical** — re-classify as KEEP, not DROP.

> **Pitfall — "looks like just a reformat"**: A commit whose `git show` is
> dominated by whitespace may still contain helper additions or signature
> changes hidden inside the reformatting. Always run `git show -w <sha>` to
> isolate non-whitespace changes; if the result is non-empty, treat the
> commit as functional.

### Phase 3 — Fan-Out Execution

Execute destinations in this fixed order: **canonical → opt-in team →
personal sandbox**. This order minimizes downstream merge-base shifts.

#### 3a — Cherry-pick canonical-destined commits onto `<canonical>`

```powershell
git -C $repo checkout <canonical>
foreach ($sha in $canonical_destined) {
    git -C $repo cherry-pick $sha
    # OR with conflict-favoring strategy if the parallel branch has helpers
    # canonical has lost:
    # git -C $repo cherry-pick -X theirs $sha
}
```

> **`-X theirs` rule**: Use only when the parallel branch is known to carry
> functional helpers (e.g., extracted private methods, refactored utility
> calls) that the canonical branch has since deleted via an unrelated
> refactor. Confirm via `git diff -w` first; never use `-X theirs` reflexively.

> **Keep-Both Registry-Conflict pattern (FORBIDDEN to use `-X theirs`)**:
> When the conflict is on an **SSOT registry file** (XML constraint
> registry, JSON manifest, log-config table, dependency-injection module
> list) where BOTH branches added new entries in the same section, neither
> `-X theirs` nor `-X ours` is correct — both would silently drop one
> branch's additions. Manual merge MUST keep ALL additions from BOTH
> sides. Diagnose with:
>
> ```powershell
> # Identify the conflict regions and the entries each side added:
> git -C $repo diff --name-only --diff-filter=U
> foreach ($f in (git -C $repo diff --name-only --diff-filter=U)) {
>     Write-Host "--- $f ---"
>     Select-String -Path (Join-Path $repo $f) -Pattern '^(<<<<<<<|=======|>>>>>>>)'
> }
> ```
>
> Then edit each conflicted file to concatenate the HEAD block + the
> incoming block (deduplicated by entry ID). After all files:
>
> ```powershell
> git -C $repo add <files>
> git -C $repo -c core.editor=true cherry-pick --continue
> ```
>
> Verification: count expected entries in each registry post-merge:
>
> ```powershell
> foreach ($f in $registryFiles) {
>     foreach ($id in $expectedIds) {
>         $c = (git -C $repo show "HEAD:$f" | Select-String -Pattern $id).Count
>         Write-Host "$f $id=$c"
>     }
> }
> ```
>
> Real-world derivation: 2026-05-16 decommission of `<canonical>-skill`
> where canonical's `ICEDAMOS0065` entries and incoming's `ICEDAMOS0038`
> entries collided in 3 XML registries (`IceLogConfig`, `constraints`,
> `specifications_en`). `-X theirs` would have silently dropped 0065.

#### 3b — Cherry-pick opt-in / diagnostic commits onto a separate team branch

```powershell
git -C $repo checkout -b <canonical>-diagnostics <canonical>   # post-3a tip
foreach ($sha in $diagnostic_destined) {
    git -C $repo cherry-pick --no-commit $sha
    # Drop any non-diagnostic files from the staged change:
    git -C $repo reset HEAD <path-to-drop>
    git -C $repo checkout -- <path-to-drop>
    git -C $repo commit -m "<reworded conventional-commits message>"
}
```

The reworded message MUST cite the source SHA and explain why the file was
split, so future archaeologists can trace the lineage.

#### 3c — Personal sandbox: inspect, then rebuild if necessary

> **Critical pre-check**: The sandbox may **already contain** the parallel
> branch's history (a common artifact of an earlier broad
> `git push --all personal` or of having branched the sandbox off the
> parallel branch itself). If so, a naive cherry-pick will hit empty diffs.

```powershell
git -C $repo branch --contains <parallel-sha> | Select-String <sandbox>
```

If the SHA is contained, the sandbox needs a **rebuild on the merge-base**,
not a series of cherry-picks onto its existing tip:

```powershell
# Rebuild on the merge-base, keep ONLY the destined commits + pre-existing
# personal-only commits.
git -C $repo checkout -b <sandbox>-rebuild <merge-base>
foreach ($sha in $sandbox_destined)       { git -C $repo cherry-pick $sha }
foreach ($sha in $sandbox_pre_existing)   { git -C $repo cherry-pick $sha }

# Verify the rebuilt branch contains NONE of the canonical-destined files:
git -C $repo --no-pager log --oneline <merge-base>..HEAD -- <canonical-paths>
# Output MUST be empty.

# Swap the real sandbox over and delete the temp branch:
git -C $repo branch -f <sandbox> <sandbox>-rebuild
git -C $repo checkout <sandbox>
git -C $repo branch -D <sandbox>-rebuild
```

For split commits on the sandbox side, repeat the
`cherry-pick --no-commit` → `reset HEAD <other-files>` →
`checkout -- <other-files>` → reworded `commit` pattern from §3b.

### Phase 3.5 — Dependent-Branch Restack Cascade

When Phase 3 advanced `<canonical>` (or any base branch) by cherry-picking
new commits onto it, ANY other branch (diagnostics, opt-in instrumentation,
personal sandbox, downstream feature stack) still rooted on the
pre-decommission canonical tip is now stale and MUST be restacked before
its next force-push.

Delegate to
[`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md)
with:

- `<old-tip>` = the canonical tip captured in the Phase 0a backup tag
  (`backup/<canonical>-pre-decom-<date>`).
- `<new-tip>` = the canonical tip after Phase 3a's cherry-picks.

The cascade discovers all dependents, runs `rebase --onto $new $old <dep>`
per branch, verifies patch-id parity, and gates each force-push. Phase 4
below proceeds in parallel for the canonical and opt-in destinations.

### Phase 4 — Per-Destination Push (Authorization Gate)

EVERY push requires its own explicit user authorization. NEVER batch.

| # | Destination Branch | Push Command | Notes |
|---|---|---|---|
| 1 | `<canonical>` | `git push origin <canonical>` | Fast-forward — should never need `--force` |
| 2 | `<canonical>-diagnostics` | `git push origin <canonical>-diagnostics` | New branch — `* [new branch]` expected |
| 3 | `<sandbox>` | `git push --force-with-lease personal <sandbox>` | History rewrite via rebuild — `--force-with-lease` MANDATORY, `--force` FORBIDDEN |

### Phase 5 — Parallel Branch Deletion (Authorization Gate)

ONLY after all three pushes succeed AND the user authorizes:

```powershell
git -C $repo push origin --delete <parallel-branch>
git -C $repo branch -D <parallel-branch>
# Personal remote may also carry the parallel branch from prior `--all` pushes:
git -C $repo ls-remote --heads personal <parallel-branch>
# If non-empty:
git -C $repo push personal --delete <parallel-branch>
```

### Phase 6 — Verification & Cleanup

#### 6a — External verification (user-driven)

The user externally verifies (e.g., GitHub Web UI):

- `<canonical>` has the new SHAs at HEAD.
- `<canonical>-diagnostics` exists with the diagnostic commit.
- `<sandbox>` history is clean (no canonical paths touched).
- `<parallel-branch>` is gone from every remote.

#### 6b — Drop the safety tags (only after step 6a passes)

```powershell
git -C $repo tag -d "backup/<parallel-branch>-pre-decom-$today" `
                   "backup/<canonical>-pre-decom-$today"       `
                   "backup/<sandbox>-pre-decom-$today"
```

***

## 4. Pitfalls & Recovery

### 4.1 Eclipse / IDE file lock during `git checkout`

Symptom: `Deletion of directory '<package>/src' failed. Should I try again?`
loop during a branch switch. Cause: an open IDE (Eclipse PDE, IntelliJ) holds
a handle on a directory that the branch switch needs to delete (typically
`src/` containing a `.gitkeep`).

Recovery (without closing the IDE):

```powershell
# Stage 1: let the partial checkout abort, then restore the working tree.
git -C $repo checkout -- <package>/src/.gitkeep
# Stage 2: manually remove the directory (IDE will recreate it as needed).
Remove-Item "$repo\<package>\src" -Recurse -Force
# Stage 3: re-run the checkout.
git -C $repo checkout <target-branch>
```

### 4.2 Cherry-pick conflict on a "should be parity" file

Indicates the canonical branch has diverged from the parallel branch on that
file. **Stop and re-classify** — the commit may carry more than the surface
diff suggests. See [`git-commit-details-audit`](../git-commit-details-audit/SKILL.md)
for forensic inspection before deciding `-X theirs` vs manual merge.

### 4.3 LFS-locking warning on first push to a new destination

Cosmetic only:

```text
Locking support detected on remote "<remote>". Consider enabling it with:
  $ git config lfs.<url>/info/lfs.locksverify true
```

Push still succeeds. Do NOT enable lock verification reactively — that's a
team-policy decision, not a side effect of this workflow.

### 4.4 SHA hallucination challenge

If the user asks "are these SHAs real?", verify with a single loop and show
the output verbatim:

```powershell
foreach ($sha in $all_planned_shas) {
    $line = git -C $repo --no-pager log -1 --oneline $sha 2>&1
    if ($LASTEXITCODE -eq 0) { "OK   $line" } else { "MISS $sha" }
}
```

Never proceed with a plan that references a `MISS` SHA.

***

## 5. Acceptance Criteria

The decommission is complete when:

1. Every `parallel_unique[i]` commit has either been cherry-picked to its
   classified destination OR has a verified-parity equivalent already on
   that destination (DROP justified).
2. Every destination branch pushes cleanly under its own user authorization.
3. The parallel branch is deleted from every remote and locally.
4. The user externally verifies the destination state and authorizes safety
   tag deletion.

***

## 6. Related Conversations & Traceability

- Session 2026-05-16 (`<ticket-system>` ticket: feature decommission of
  `<canonical>-ai_demo`): original derivation of the N-way fan-out pattern,
  including the sandbox-already-contains-parallel-history edge case and the
  Eclipse `.gitkeep`-directory file-lock workaround.

All session logs MUST be sanitized through
[`redaction-portability`](../redaction-portability/SKILL.md) before commit.
