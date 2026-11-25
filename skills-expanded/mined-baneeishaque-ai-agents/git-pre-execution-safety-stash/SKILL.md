---
name: git-pre-execution-safety-stash
description: Capture a verifiable working-tree safety snapshot via apply-not-pop stash before executing any multi-commit sequence, with end-of-session no-op verification and gated drop.
category: Git & Repository Management
---

# Git Pre-Execution Safety Stash Skill

> **Skill ID:** `git-pre-execution-safety-stash`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Before executing any multi-step Git commit sequence — atomic commit
construction batches, history refinement runs, rebase chains, hunk-staged
splits — capture a single high-fidelity snapshot of the full working tree
(tracked modifications, staged hunks, AND untracked files), immediately
re-apply it, and retain the stash entry until end-of-session verification
proves every planned change reached HEAD. The retained stash is the
cheapest, highest-fidelity rollback primitive available against accidental
`git checkout`, `git reset`, IDE crash, interrupted rebase, or stale-disk
recovery loss during long multi-commit sequences.

This skill is invoked by composer skills (atomic-commit construction,
history refinement, rebase standardization) and runs in three phases:
**Snapshot** (before execution), **Hold** (during execution — never
dropped), **Verify-and-Release** (after execution, only on clean no-op).

## Source Rules

| Rule File | Scope Incorporated |
|---|---|
| [`git-atomic-commit-construction-rules.md` §3.3](../../../ai-agent-rules/git-atomic-commit-construction-rules.md) | Pre-Execution Safety Stash mandate |
| [`git-operation-rules.md` §5](../../../ai-agent-rules/git-operation-rules.md) | Stash preservation — drop / pop / clear require explicit per-stash user authorization |

## Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ or Bash 4+ |
| State | Working tree may be dirty (the whole point); HEAD on a real branch (not detached) |

## When to Apply

Apply this skill when:

- About to execute a sequence of two or more commits authored under
  [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md).
- About to execute any batch under §3.2 Batch-by-Batch Authorization.
- About to run [`git-history-refinement`](../git-history-refinement/SKILL.md),
  [`git-rebase-standardization`](../git-rebase-standardization/SKILL.md), or
  [`git-commit-edit`](../git-commit-edit/SKILL.md) against a dirty working
  tree where hunk-by-hunk staging will run.
- About to run an interactive rebase across more than two pick lines.

Do NOT apply when:

- Executing a single-commit, single-file change with no hunk splitting.
- The working tree has zero modifications and zero untracked files —
  `git stash push` would no-op, but the apply-back verification step
  becomes meaningless.
- The destructive disposition of pre-existing stashes is itself the
  task — invoke [`git-stash-triage`](../git-stash-triage/SKILL.md)
  first; this skill creates a NEW snapshot, it does not classify
  legacy ones.

---

## Step-by-Step Procedure

### Phase 1 — Snapshot (before first commit of the sequence)

#### 1a — Inventory pre-existing stashes

```powershell
git -C <repo-path> --no-pager stash list
```

If the output is non-empty, each entry MUST be classified via
[`git-stash-triage`](../git-stash-triage/SKILL.md) BEFORE pushing
the safety stash. Pushing a safety stash on top of an unclassified
stash stack creates ambiguity at verification time about which
`stash@{N}` is "ours."

#### 1b — Author a descriptive snapshot message

The message MUST encode at minimum:

- Purpose token `safety:` (distinct from feature WIP, mixed work,
  triage-bucket markers).
- A short description of the upcoming sequence (e.g.,
  `pre-batch-2 snapshot of commits 7..11 family-unit introduction`).
- A change-count summary (e.g., `12 modified + 8 untracked`).
- An ISO date (e.g., `2026-05-17`).

Example:

```text
safety: pre-batch-1-remainder snapshot of 14 modified + 8 untracked entries before commits 5..N land (2026-05-17)
```

The `safety:` prefix is the canonical marker that lets the verification
phase (and any future triage) identify this stash entry unambiguously.

#### 1c — Push the snapshot with untracked files included

```powershell
git -C <repo-path> stash push -u -m "<message-from-1b>"
```

The `-u` flag is MANDATORY — untracked files are first-class working-tree
state per the §3.3 mandate, and a snapshot without them defeats the
rollback purpose for any sequence that introduces new files.

#### 1d — Immediately apply back

```powershell
git -C <repo-path> stash apply
```

**Apply, NOT pop.** Pop would drop the stash entry on success, defeating
the rollback contract. `apply` leaves the entry intact on the stash stack
while restoring every line to the working tree.

#### 1e — Verify post-apply parity

```powershell
git -C <repo-path> status --short | Measure-Object | Select-Object -ExpandProperty Count
```

The line count MUST equal the pre-stash status line count. Any mismatch
indicates the apply was partial (typically due to an IDE file-lock —
see Phase 1f).

```powershell
git -C <repo-path> stash list | Select-String '^stash@\{0\}: .* safety: '
```

The line MUST be present. If absent, the push failed silently — re-run
1c and 1d.

#### 1f — IDE File-Lock Recovery During Apply

`git stash apply` can fail mid-stream on Windows when the IDE (VS Code,
Eclipse, IntelliJ) holds open file handles on a directory the apply
needs to delete or restore:

```text
Deletion of directory '<path>' failed. Should I try again? (y/n)
...
warning: failed to remove <path>: Permission denied
```

The stash push itself succeeded (verify with 1e step 2); only the apply
is partial. Recovery options, in order of preference:

1. **Close the indexing tool window** for the affected workspace (or
   stop the JDT Language Server / Eclipse builder), then re-run
   `git stash apply`. The second apply typically succeeds.
2. **Move the offending directory out of the way** (`Move-Item`), re-run
   apply, then restore the moved directory by `git checkout -- <path>`
   if it is tracked or by `Move-Item` back if untracked.
3. **Apply via an isolated worktree** per
   [`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md)
   §4.6 pattern, then cherry-pick the apply into the main worktree.

In all cases the stash entry MUST remain on the stack — never `pop`
during recovery.

#### 1g — Stash-Apply Conflict Recovery via Selective File Extraction

When `git stash apply` fails because a live editor (VS Code, Copilot,
Eclipse, IntelliJ) rewrote files between the `push` and `apply` commands,
the standard recovery options in 1f (close editor → retry apply, move
offending directory) may not work — the editor instantly regenerates the
conflicting files. Do NOT retry `git stash apply`; each retry reproduces
the same conflicts. Instead, extract files **selectively** from the intact
stash entry as each commit in the planned sequence is executed.

**Prerequisite**: You MUST have an approved Arranged Commits Preview (from
[`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
§3 — the Verbose Display) that lists every planned commit and the files
it needs. Without this plan, selective extraction has no target.

**Procedure — repeat for each planned commit in sequence:**

1. **Identify needed files**. From the Arranged Commits Preview, list the
   exact file paths the current commit requires.

2. **Compare each file against the stash**. For every file the commit needs:
   - **If tracked** (exists in HEAD): `git diff stash@{0} -- <file>` shows
     whether the stash holds a different version. An empty output means the
     working tree already matches the stash; skip extraction.
   - **If untracked** (new file not yet in HEAD): `git ls-tree stash@{0}^3`
     lists untracked files captured by the `-u` flag. Check if `<path>`
     appears in that listing.

3. **Extract the desired stash version**:
   - **Tracked files**: `git checkout stash@{0} -- <file>`
   - **Untracked files**: `git show stash@{0}^3:<path> > <path>`
     (The `^3` suffix addresses the untracked-tree parent of a stash —
     `stash@{0}^3` is the tree object that `git stash push -u` captured.)

4. **Verify extraction**:

   ```bash
   git diff <file>
   # MUST show the stashed content now present in the working tree
   # (no diff means the working tree already matched stash)
   ```

5. **Stage and commit** per the approved plan using normal atomic-commit
   construction procedures (`git add <file>`, `git commit -m "..."`).

6. **Repeat** for the next planned commit.

**Example** — commit 1 needs `src/foo.ts` and `src/bar.ts`:

```bash
# Compare tracked files against stash
git diff stash@{0} -- src/foo.ts       # shows stash has changes
git diff stash@{0} -- src/bar.ts       # empty — working tree matches

# Extract foo.ts from stash
git checkout stash@{0} -- src/foo.ts

# Verify extraction
git diff src/foo.ts                    # no diff = correct

# Stage and commit per plan
git add src/foo.ts src/bar.ts
git commit -m "feat(foo): implement core logic"
```

**Safety guarantees**:

- The stash entry (`stash@{0}`) is NEVER modified by `git checkout
  stash@{0} -- <file>` or `git show stash@{0}^3:<path>` — these are
  read-only operations against the stash object. The stash remains
  intact for end-of-session Phase 3 verification.
- Files whose working-tree version was intentionally preferred over
  the stash version (e.g., because the live editor's changes are
  desired) are simply skipped in step 2 — no extraction, no conflict.
- After all planned commits land, proceed to **Phase 3**
  (Verify-and-Release) as normal. The stash is retained for the full
  verification cycle; it MUST NOT be dropped without user authorization
  per Phase 3d.

**When NOT to use this procedure**:

- The stash apply succeeded (even partially). Use Phase 1e/1f instead.
- You do not have an Arranged Commits Preview identifying per-commit
  files. Without a plan, you cannot know which files belong to which
  commit — abort and re-plan first.
- The stash itself is corrupted or missing (`git stash list` shows no
  `safety:` entry). A fresh Phase 1 capture is required.
- The stash is **not a safety stash** (no `safety:` prefix) — it is a
  stale or pre-existing stash. Delegate to
  [`git-stash-triage`](../git-stash-triage/SKILL.md) §4d (Selective File
  Restoration — Per-File Triage) instead, which covers the general
  per-file extraction protocol for any stash.

---

### Phase 2 — Hold (during the commit sequence)

#### 2a — Never drop the safety stash mid-sequence

The agent MUST NOT run `git stash drop`, `git stash pop`, or
`git stash clear` between Phase 1 and Phase 3. If the user requests
unrelated stash work mid-sequence, route them through
[`git-stash-triage`](../git-stash-triage/SKILL.md) and disambiguate
by `safety:` message prefix.

#### 2b — Re-verify presence at batch boundaries

For sequences running under §3.2 batch-by-batch authorization, before
emitting the next batch preview run:

```powershell
git -C <repo-path> stash list | Select-String '^stash@\{0\}: .* safety: '
```

A missing entry MUST halt the sequence — the snapshot has been lost
and a fresh Phase 1 capture is required before resuming.

---

### Phase 3 — Verify-and-Release (after the final commit of the sequence)

#### 3a — Capture the post-execution working-tree fingerprint

```powershell
$preApplyStatus = git -C <repo-path> status --short
```

If the working tree is clean (`$preApplyStatus` empty), every planned
change reached HEAD. If non-empty, classify the residue:

- **Expected**: Files deliberately left unstaged for a later batch (matches
  the Master Plan Table from §3.2). These remain after release.
- **Unexpected**: Files that should be in HEAD but aren't — investigate
  before release. Do NOT proceed to 3b until resolved.

#### 3b — Apply the safety stash on top of the current tree

```powershell
git -C <repo-path> stash apply
```

#### 3c — Verify the apply is a clean no-op

```powershell
$postApplyStatus = git -C <repo-path> status --short
# Compare line-by-line against $preApplyStatus
if (Compare-Object $preApplyStatus $postApplyStatus -SyncWindow 0) {
  Write-Host '[FAIL] Apply produced a delta — DO NOT drop the stash.'
} else {
  Write-Host '[OK] Apply was a no-op — every planned change is in HEAD.'
}
```

**Interpretation**:

- **Clean no-op** → Every line in the snapshot is also in HEAD (or in
  the expected residue). The stash is now redundant and safe to drop
  after user authorization (Phase 3d).
- **Apply produced a delta** → Some snapshot content is NOT in HEAD.
  Either a planned commit was skipped or partially applied, OR the
  residue analysis in 3a missed something. The stash MUST be retained
  for forensic recovery. Re-investigate before any drop.
- **Merge conflicts during 3b apply** → The working tree has diverged
  from the snapshot in a way that would discard snapshot content.
  Resolve manually using `git checkout -- <file>` from the stash, or
  abort with `git checkout .` and investigate. The stash MUST be retained.

#### 3c.1 — Optional: stronger per-file content audit

The `stash apply` no-op check in 3c proves the working tree didn't *change*
when the stash was re-applied — strong evidence that snapshot content is in
HEAD, but it is a *delta*-level check. For higher confidence (especially
when the stash captured untracked files via `-u`, where `apply` does NOT
restore tracked-blob equality information), run the
[`git-ref-content-audit`](../git-ref-content-audit/SKILL.md) per-file
blob-equality audit:

```bash
python3 .agents/skills/git-ref-content-audit/scripts/audit-ref-content.py \
    --repo <repo-path> \
    --stash 0 \
    --ref-b HEAD \
    --show-diffs
```

A `✅ FULLY SUPERSEDED` verdict upgrades 3c from "no delta on re-apply" to
"every stashed blob byte-equal at HEAD". A `⚠️ PARTIALLY SUPERSEDED`
verdict surfaces deliberate post-stash refinements that the `apply` no-op
would have masked silently — inspect each `DIFFERENT` file before deciding.
A `❌ NOT SUPERSEDED` verdict is a HARD STOP: do not proceed to 3d.

#### 3d — Gated drop with explicit user authorization

ONLY after 3c (and, if used, 3c.1) reports clean no-op / full supersession:

```text
The safety stash has been verified as a clean no-op against HEAD. Drop
stash@{0}? (yes / no / inspect-first)
```

- **yes** → `git stash drop stash@{0}`.
- **no** → Retain indefinitely. Recommend re-running 3b after any
  further commits to re-verify.
- **inspect-first** → Run `git stash show -u stash@{0}` and `git stash
  show -p stash@{0}` for full content review before deciding.

The drop MUST NOT be automated even when 3c is clean — per
[`git-operation-rules.md` §5](../../../ai-agent-rules/git-operation-rules.md),
every destructive stash operation requires explicit per-stash user
authorization.

---

## Composition by Higher-Level Skills

| Composer Skill | Role of this skill in the pipeline |
|---|---|
| [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) §3.3 | Mandatory invocation before the first commit of any sequence of ≥ 2 commits, including every batch under §3.2 Batch-by-Batch Authorization. |
| [`git-history-refinement`](../git-history-refinement/SKILL.md) | Captures the working tree before destructive history rewrites, providing a rollback path independent of the backup branch (which only covers committed history). |
| [`git-rebase-standardization`](../git-rebase-standardization/SKILL.md) | Captures the working tree before any rebase that runs against a dirty tree (the rebase will otherwise refuse or stash-implicitly). |
| [`git-commit-edit`](../git-commit-edit/SKILL.md) | Captures the working tree before interactive rebase with hunk-splitting. |

## Related Skills

| Skill | Relationship |
|---|---|
| [`git-stash-triage`](../git-stash-triage/SKILL.md) | **Prerequisite when stash list is non-empty at Phase 1a.** Classifies pre-existing stash entries so the `safety:` push lands at a known position on the stack. Also provides §4d (Selective File Restoration — Per-File Triage) for stale stashes where Phase 1g does not apply. |
| [`untracked-scratch-triage`](../untracked-scratch-triage/SKILL.md) | When Phase 3a residue includes unexpected untracked files (e.g., hunk-stage backup sidecars per §4.3), classifies them before deciding whether to drop the safety stash. |
| [`git-ref-content-audit`](../git-ref-content-audit/SKILL.md) | Optional Phase 3c.1 per-file blob-equality audit between the safety stash (including its `^3` untracked tree) and HEAD — upgrades the `apply` no-op check from delta-level to byte-level supersession proof. |
| [`git-worktree-state-fingerprint`](../git/basic/audit/git-worktree-state-fingerprint/SKILL.md) | Read-only byte-level worktree state capture/compare (no stash entry involved) — the complementary verification primitive when the proof requirement is "the working tree did not change" rather than "the working tree can be rolled back"; useful for bracketing any multi-commit sequence without touching the stash stack. |

## Pitfalls & Recovery

| Symptom | Recovery |
|---|---|
| `git stash push -u` returned `No local changes to save` | Sequence has nothing to snapshot — verify the §3.3 mandate even applies (≥ 2 commits AND non-empty working tree). Skip this skill if both conditions don't hold. |
| `git stash apply` fails with `CONFLICT` after a successful push | Working tree advanced between push and apply (rare — typically a parallel `git pull`). Resolve conflicts manually, then re-verify 1e. Never `git checkout .` here — it discards the conflict markers. |
| `git stash apply` fails because a live editor (VS Code, Copilot, Eclipse, IntelliJ) rewrote files and `git checkout .` / close-editor did not resolve the conflict | Do NOT retry apply. Switch to **Phase 1g** — Selective File Extraction from Stash — to extract per-commit files from `stash@{0}` individually, working through the approved commit plan one commit at a time. The stash remains intact for end-of-session verification. |
| Stale stash (not a `safety:` stash) with divergent apply that Phase 1g does not cover (no planned commit sequence) | Delegate to [`git-stash-triage`](../git-stash-triage/SKILL.md) §4d (Selective File Restoration — Per-File Triage) for general per-file extraction without a pre-planned commit sequence. |
| Stash list now shows multiple `safety:` entries | A prior sequence's verification was skipped. Inspect each via `git stash show -u stash@{N}` and verify-then-drop oldest-first using Phase 3 against each. |
| Phase 3c shows persistent delta on files matching `*.bak` / `*.full.bak` | Hunk-stage backup sidecars per §4.3 were not cleaned up — delete the sidecars, re-run 3b. |
| End-of-session verification skipped (agent terminated mid-sequence) | The safety stash remains valid for the recovery window. Resume with Phase 2b verification, then proceed with the remaining commits OR Phase 3 directly if the sequence completed externally. |
| Detached HEAD at Phase 1a | `git stash` works in detached HEAD but `stash apply` after a checkout will appear to "lose" the apply on the original commit. Checkout the intended branch first, then capture. |

## Source Conversations

| Date | Topic |
|---|---|
| 2026-05-17 | First codification — extracted from the batch-1-remainder execution discipline that surfaced a `.bak` sidecar leftover and an IDE file-lock during stash apply. |
