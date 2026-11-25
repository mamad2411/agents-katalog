---
name: git-personal-content-extraction
description: Composer — purify a single mixed team / feature / ticket
    branch IN PLACE by classifying every commit as team / personal /
    mixed, reordering personal commits to the tip, splitting mixed
    commits per file, resetting the team branch to a team-only tip,
    and re-inserting the extracted personal commits into their
    ORIGINAL CHRONOLOGICAL POSITION on a long-lived personal sandbox
    branch (NOT appended at the tip). Distinct from
    `git-parallel-branch-decommission` (which assumes a sibling
    parallel branch exists and gets deleted); this skill keeps the
    team branch alive and never creates a parallel one. Executes in
    risk-managed ROUNDS with per-round backup, authorized push, and
    a master safety-net audit before final backup deletion.
category: Git & Repository Management
---

# Git Personal Content Extraction Skill (v1)

> **Skill ID:** `git-personal-content-extraction`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A single team-facing branch `<team>` (e.g., `<user>-<ticket-id>`)
has accumulated MIXED commits over time:

- **Team commits** — the actual ticket deliverable that integration
  reviews.
- **Personal commits** — build tweaks, IDE `.launch` files,
  personal documentation, skill drafts, telemetry experiments,
  in-progress AI-demo work, etc.
- **Mixed commits** — single commits that touch BOTH team files
  and personal files.

The goal is to **purify `<team>` in place** so integration sees
only team-relevant work, while preserving every personal commit on
a separate `personal/sandbox` branch in its **original chronological
position** (interleaved among pre-existing sandbox content, NOT
appended at the tip).

The reference execution (4 rounds + 1 follow-up Round 5, ~41 backup
commits → 14 team + 27 sandbox + 1 intentional drop + 1 split with
byte-exact per-file preservation) is documented in the project's
work doc. This skill industrializes that pattern as a reusable
composer.

## When to Apply

Apply this skill when ALL of the following hold:

1. A single team-facing branch contains personal commits that
   integration should not see.
2. A long-lived `personal/sandbox` branch (or equivalent) already
   exists on a personal remote — set up via
   [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md).
3. Personal commits MUST land on the sandbox in their original
   chronological position (not appended).
4. Dependent branches (diagnostics, opt-in instrumentation) may be
   rooted on the team tip and need cascading after each round.
5. The work is too large for a single rebase — risk management
   requires ROUNDS.

If a parallel branch (e.g., `<team>-ai_demo`) exists as a separate
sibling and you want to DELETE it after fanning its content out,
use [`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md)
instead — that is the inverse-direction sibling.

## Composition Rationale

This skill is a **composer**. It orchestrates the following primitives
without reimplementing them:

| Composed Skill | Used for |
|---|---|
| [`git-commit-edit`](../git-commit-edit/SKILL.md) | Per-round backup, sequence-editor script authoring, rebase mechanics |
| [`git-rebase-standardization`](../git-rebase-standardization/SKILL.md) | CAM table conventions, modify-vs-delete (DU) conflict discipline, backup-branch naming |
| [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) | Phase 5 sandbox restack onto new team tip + six-axis equality audit |
| [`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md) | Phase 6 cascade onto any diagnostics / opt-in / feature-stack dependents |
| [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md) | Prerequisite — personal remote and sandbox branch must already exist |
| [`git-commit-metadata-extraction`](../git-commit-metadata-extraction/SKILL.md) | Per-commit subject + file list for the classification table |
| [`git-drop-commit-with-divergent-recreation`](../git-drop-commit-with-divergent-recreation/SKILL.md) | Optional follow-up round when sandbox-internal cleanup uncovers a divergent-recreation pattern |
| [`redaction-portability`](../redaction-portability/SKILL.md) | Sanitizing the round-log artifact before commit |

The composer **MUST NOT** reimplement rebase mechanics, restack
audits, or cascade discovery — those belong to the owners listed above.

## Source Rules

| Rule File | Scope Incorporated |
|---|---|
| [`ai-rule-standardization-rules.md`](../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First Architecture, Layered Composition Mandate, Fidelity Mandate |
| [`script-management-rules.md`](../../../ai-agent-rules/script-management-rules.md) | PowerShell sequence-editor authoring |

---

## Step-by-Step Procedure

### Phase 0 — Master Safety Net (run ONCE for the entire purification)

Before Round 1, create the master backup that will survive every
round and only be deleted after the final master audit (Phase 8).

```powershell
git branch backup/<team>-pre-purification-<YYYY-MM-DD>
```

Document the safety-net SHA in a work-doc artifact (recommended:
`<workspace-root>/<ticket-id>-purification-workdoc.md`) — every
subsequent round audit references this baseline.

### Phase 1 — Inventory & Classification (run ONCE)

#### 1a — List every unique commit between merge-base and team tip

```powershell
$base = git merge-base <trunk> <team>
git log --oneline "$base..<team>"
```

Delegate per-commit metadata (subject, file list, author, dates) to
[`git-commit-metadata-extraction`](../git-commit-metadata-extraction/SKILL.md).

#### 1b — Classify each commit by content

Build a classification table in the work doc:

| SHA | Subject | Files touched | Class |
|---|---|---|---|
| `<sha-1>` | … | `<paths>` | TEAM / PERSONAL / MIXED |

**Classification rubric**:

- **TEAM**: every file path is unambiguously team-functional (ticket
  deliverable, src/, configuration consumed by CI/integration).
- **PERSONAL**: every file path is unambiguously personal (`.launch`
  / `Launches/`, `.agents/skills/**`, `AGENTS.md` drafts under
  personal authorship, personal-only docs / build tweaks).
- **MIXED**: at least one file in each bucket. MUST be split per
  file in the round that touches it.

Edge-case files (e.g., `.project` IDE artifacts) MAY be intentionally
DROPPED — flag them separately in the table.

#### 1c — Group commits into ROUNDS

Each round must be **atomic** (all-or-nothing) and **independent**
(one round's failure must not block the next). Recommended grouping:

| Round | Scope | Risk |
|---|---|---|
| 1 | Earliest contiguous block of personal commits at the bottom of the branch + any intentional drops | Low (no descendants depend on these) |
| 2…N-1 | One contiguous personal block per round | Medium |
| Final | Mixed commits requiring per-file split | High (split semantics) |
| Optional N+1 | Sandbox-internal cleanup that surfaced from Round N | See [`git-drop-commit-with-divergent-recreation`](../git-drop-commit-with-divergent-recreation/SKILL.md) |

Smaller rounds with fewer commits per round reduce blast radius if
something goes wrong.

### Phase 2 — Per-Round Backup (run AT THE START of every round)

```powershell
git branch backup/<team>-pre-round<N>-<YYYY-MM-DD>
git branch backup/sandbox-pre-round<N>-<YYYY-MM-DD>
git branch backup/<diagnostics>-pre-round<N>-<YYYY-MM-DD>   # if dependents exist
```

Per-round backups are deleted at the end of each successful round
(after Phase 7 push lands). The master backup from Phase 0 stays
until Phase 8.

### Phase 3 — Reorder Team Branch (Surface Personal at Tip)

Use an interactive rebase with a sequence-editor script that moves
the round's personal commits to the **top** of the team branch's
history (just below `HEAD`), keeping team commits in their original
relative order.

#### 3a — Author the sequence-editor script

PowerShell template (replace `<SHA-LIST>` with the round's
personal-commit SHAs in original-chronological order):

```powershell
# .git/round<N>-reorder.ps1
param([string]$todoFile)
$content = Get-Content -Raw $todoFile
$lines   = $content -split "`r?`n"

# Personal SHAs in their original chronological order:
$personal = @('<sha-a>', '<sha-b>', '<sha-c>')

$personalLines = @()
$teamLines     = @()
foreach ($line in $lines) {
    if ($line -match '^pick\s+(\S+)') {
        $sha = $Matches[1]
        if ($personal | Where-Object { $sha.StartsWith($_) -or $_.StartsWith($sha) }) {
            $personalLines += $line
        } else {
            $teamLines += $line
        }
    } else {
        $teamLines += $line   # preserve comments / blank lines at end
    }
}

$reordered = $teamLines[0..($teamLines.Count-1)] + $personalLines
[System.IO.File]::WriteAllText($todoFile, ($reordered -join "`n"))
```

#### 3b — Execute the rebase

```powershell
$yes = (("y`n") * 500) -join ''
$env:GIT_SEQUENCE_EDITOR = "powershell -NoProfile -File `"$repo\.git\round<N>-reorder.ps1`""
$env:GIT_EDITOR = 'true'
$yes | git rebase -i $base
```

The `$yes` pipe is mandatory on Windows when Defender or an
IDE-indexer file-lock kicks in during checkout — see
[`git-rebase-standardization`](../git-rebase-standardization/SKILL.md)
Common Pitfalls.

#### 3c — Verify the team-branch tip

After the rebase, `git log --oneline -<N+team-count>` MUST show
the round's personal commits at the top (just below any descendants
that were already above the rebase floor). If a commit is misplaced,
abort with `git rebase --abort` and re-author the script.

### Phase 4 — Split Mixed Commits (Final round only)

For each MIXED commit `<M>` in this round:

#### 4a — Mark `<M>` for `edit` via sequence-editor

```powershell
# .git/round<N>-edit-<M>.ps1
param([string]$todoFile)
(Get-Content -Raw $todoFile) -replace '(?m)^pick\s+<M-short>\s+', 'edit <M-short> ' |
    Set-Content -NoNewline $todoFile
```

#### 4b — At the `edit` stop, unstage personal-file changes

```powershell
$personalFiles = @('<personal-path-1>', '<personal-path-2>')
foreach ($f in $personalFiles) {
    git restore --staged $f
    git checkout HEAD~ -- $f   # restore PRE-commit content of the personal file
}
git commit --amend --no-edit   # team-only half is committed
```

#### 4c — Re-stage the personal halves on sandbox (Phase 6 below)

The personal half's blob hash from the original `<M>` was captured
in Phase 1's classification table. Re-apply it byte-exactly on
sandbox in Phase 6 with `git checkout backup/<...>:<path> -- <path>`
(byte-exact) + `git commit -F <msg>` with the original author/committer
dates restored via `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE`.

### Phase 5 — Reset Team Branch to Team-Only Tip

After Phase 3 (and Phase 4 if mixed commits existed), the personal
commits sit at the top of the team branch. Reset the team branch to
the highest team-only commit:

```powershell
git checkout <team>
$yes | git reset --hard <highest-team-only-sha>
```

The personal commits are now orphaned but still reachable via reflog
and the per-round backup branch.

### Phase 6 — Restack Sandbox + Re-Insert Personal Commits

This is the phase that distinguishes this skill from
`git-parallel-branch-decommission`. The personal commits must land
on the sandbox in their **ORIGINAL CHRONOLOGICAL POSITION** — NOT
appended at the tip.

#### 6a — Restack sandbox onto the new team tip

Delegate to [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md)
Phases 1–3 for the rebase mechanics and six-axis equality audit
against the pre-round sandbox backup.

Acceptance: the audit reports patch-id parity for every pre-existing
sandbox commit and an empty per-file blob delta outside the round's
intentional changes.

#### 6b — Author a sandbox sequence-editor script for SLOT INSERTION

The round's personal commits must be inserted at their original
chronological slot among pre-existing sandbox commits. Identify the
slot by comparing the personal commit's `AuthorDate` against the
sandbox log:

```powershell
git log --format='%H %aI %s' personal/sandbox
```

Author a sequence-editor script that:

1. Cherry-picks each personal commit by SHA (from the round backup).
2. Inserts each cherry-pick at the line immediately AFTER the
   sandbox commit whose `AuthorDate` is the latest one earlier than
   the personal commit's `AuthorDate`.

PowerShell template:

```powershell
# .git/round<N>-sandbox-slot.ps1
param([string]$todoFile)
$content = Get-Content -Raw $todoFile
$lines = $content -split "`r?`n"
$out = New-Object System.Collections.Generic.List[string]
foreach ($line in $lines) {
    $out.Add($line)
    if ($line -match '^pick\s+<anchor-sandbox-sha>\s+') {
        $out.Add('pick <personal-sha-1>  # slotted at original chronological position')
    }
    if ($line -match '^pick\s+<anchor-sandbox-sha-2>\s+') {
        $out.Add('pick <personal-sha-2>  # slotted at original chronological position')
    }
}
[System.IO.File]::WriteAllText($todoFile, ($out -join "`n"))
```

#### 6c — Execute the slot-insertion rebase

```powershell
$env:GIT_SEQUENCE_EDITOR = "powershell -NoProfile -File `"$repo\.git\round<N>-sandbox-slot.ps1`""
$env:GIT_EDITOR = 'true'
$yes | git rebase -i <sandbox-merge-base>
```

#### 6d — Re-audit sandbox after slot insertion

Re-run the six-axis audit from [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md)
§3 against `backup/sandbox-pre-round<N>-<date>`. Expected outcome:

- Sandbox tip files = backup tip files ∪ round's personal-half files.
- Every pre-existing sandbox commit retains its patch-id.
- New cherry-picked commits sit at their planned chronological slot.

### Phase 7 — Cascade Dependents + Authorized Push

#### 7a — Cascade

Delegate to [`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md)
for every dependent branch rooted on the old team tip (diagnostics,
opt-in instrumentation, PR-review forks). Each dependent gets its
own per-dependent patch-id parity audit and `--force-with-lease`
gate.

#### 7b — Per-destination push (in this order, each gated)

1. **Team branch** → `origin <team>` with `--force-with-lease` —
   AUTHORIZE.
2. **Dependents** → `origin <diagnostics>` etc. with
   `--force-with-lease` — AUTHORIZE (one at a time).
3. **Sandbox** → `personal personal/sandbox` with
   `--force-with-lease` — AUTHORIZE.

If any push fails (stale lease, network), abort the round, do NOT
continue to the next destination. Stale lease usually means a
dependent moved on another machine — re-fetch, re-audit, then
re-attempt.

#### 7c — Round cleanup

After all three (or more) pushes land:

```powershell
git branch -D backup/<team>-pre-round<N>-<date>
git branch -D backup/sandbox-pre-round<N>-<date>
git branch -D backup/<diagnostics>-pre-round<N>-<date>
```

Master backup from Phase 0 stays.

### Phase 8 — Master Safety-Net Audit + Deletion (run ONCE after final round)

#### 8a — Whole-commit coverage via `git cherry` (bidirectional)

```powershell
$missing_on_team    = git cherry <team>           backup/<team>-pre-purification-<date> | ? { $_ -like '+ *' }
$missing_on_sandbox = git cherry personal/sandbox backup/<team>-pre-purification-<date> | ? { $_ -like '+ *' }
```

For every backup commit, intersect the two lists. The remainder is
either intentionally dropped or correctly split (per-file).

#### 8b — Per-file blob-hash verification for split commits

For each MIXED commit `<M>` split in Phase 4:

```powershell
foreach ($file in $teamFiles) {
    $b = git rev-parse "backup/<...>:$file"
    $n = git rev-parse "<team>:$file"
    if ($b -ne $n) { Write-Host "[DIFF] $file" }
}
foreach ($file in $personalFiles) {
    $b = git rev-parse "backup/<...>:$file"
    $n = git rev-parse "personal/sandbox:$file"
    if ($b -ne $n) { Write-Host "[DIFF] $file" }
}
```

Empty output = full byte-exact preservation.

#### 8c — Hand-back verdict table

| Backup commit class | Count | Coverage |
|---|---|---|
| Whole-commit patch-id match on `<team>` or sandbox | <n> | ✅ |
| Intentionally dropped (`.project` etc.) | <n> | ✅ by design |
| Split commit (per-file byte-exact) | <n> | ✅ verified |
| **Total** | **<sum>** | All accounted for |

#### 8d — Delete the master safety net

ONLY after Phase 8c verdict is fully green:

```powershell
git branch -D backup/<team>-pre-purification-<YYYY-MM-DD>
git branch --list 'backup/*'   # MUST be empty
```

---

## Audit Performance Note

The naive nested-loop patch-id audit (one `git show | git patch-id`
per backup commit per target commit) hangs on Windows due to
subprocess overhead (~2700 process spawns for a 41-commit branch
with 65 candidate targets). Use `git cherry <upstream> <head>`
instead — one git invocation computes all patch-ids and the set
comparison in one pass. Two `git cherry` calls (one for the team
branch, one for sandbox) plus a PowerShell set intersection is the
canonical fast pattern.

---

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| Defender / IDE file-lock blows away the working tree mid-checkout | Pipe `$yes = (("y`n") * 500) -join ''; $yes \| <cmd>` to every working-tree command (rebase, checkout, reset, pull, stash apply). |
| Personal commits appended at the sandbox tip instead of original chronological position | Phase 6b/6c are mandatory. Naïvely cherry-picking onto the sandbox tip produces a chronologically-flat sandbox that loses the "what was I working on when" narrative. |
| Mixed commit split with `Out-File` / `Set-Content` for personal-half restoration | Re-encoding breaks byte-exact blob preservation. Use `git checkout backup/<...>:<path> -- <path>` (byte-exact) or `Copy-Item -Force` from a byte-preserving source. Verify with `git hash-object`. |
| `git commit --amend` used after a Phase 4 split's `git restore --staged` | Risk of folding the team-half resolution into a downstream commit if a rebase is paused. Always do the split OUTSIDE an active rebase or in a dedicated `edit` slot. |
| Master backup deleted before Phase 8 audit passes | Recovery becomes a reflog hunt. Master backup deletion is the LAST step, gated by 8c verdict. |
| Sandbox restack lost a file because `rebase --onto` excluded the split commit as ancestor | Re-add via `git checkout backup/sandbox-pre-round<N>:<path> -- <path>` + `git add` + `git commit` with preserved author date. See [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) §4.4. |
| Dependent cascade skipped after team tip moves | Diagnostics / opt-in branches rooted on the OLD team tip become orphans. [`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md) is mandatory in Phase 7a when any dependent exists. |

---

## Composition by Higher-Level Skills

| Composer | Purpose |
|---|---|
| (none yet) | First adopter — register here when added. |

## Related Skills

- [`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md)
  — the **inverse-direction sibling**. Decommissioning ASSUMES a
  parallel branch exists alongside the canonical and gets DELETED
  after fanning content out. This skill ASSUMES no parallel branch —
  one mixed team branch gets purified in place and is kept alive.
- [`git-history-refinement`](../git-history-refinement/SKILL.md) —
  the generic sibling. Use this skill when the scope is specifically
  team/personal split with chronological sandbox preservation; use
  `git-history-refinement` for arbitrary history reconstruction.

## Environment & Dependencies

- **Git** ≥ 2.30 (for reliable `--force-with-lease`).
- **PowerShell** Windows 5.1+ or PowerShell Core 7+ (for sequence-editor
  scripts).
- **Personal remote** registered as `personal` via
  [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md).
- **Work doc** — recommended at
  `<workspace-root>/<ticket-id>-purification-workdoc.md` for round
  classification, per-round audit results, and the master safety-net
  audit verdict.

---

## Verification Checklist

- [ ] Phase 0: master safety net created
- [ ] Phase 1: classification table built, every commit classed TEAM / PERSONAL / MIXED / DROP
- [ ] Phase 1c: commits grouped into rounds, smallest-risk first
- [ ] Phase 2 (each round): three backup branches created
- [ ] Phase 3 (each round): sequence-editor reorders personal commits to team tip
- [ ] Phase 4 (final round): mixed commits split per file, byte-exact preservation verified
- [ ] Phase 5: team branch reset to team-only tip
- [ ] Phase 6a: sandbox restacked, six-axis audit passes
- [ ] Phase 6b/6c: personal commits inserted at original chronological slot on sandbox
- [ ] Phase 6d: post-slot audit confirms full preservation
- [ ] Phase 7a: dependent cascade run for every branch rooted on old team tip
- [ ] Phase 7b: three (or more) pushes authorized one at a time
- [ ] Phase 7c: per-round backups deleted after successful push
- [ ] Phase 8a/8b: master audit shows every backup commit covered (whole or per-file)
- [ ] Phase 8c: hand-back verdict table green
- [ ] Phase 8d: master backup deleted, zero `backup/*` branches remain
