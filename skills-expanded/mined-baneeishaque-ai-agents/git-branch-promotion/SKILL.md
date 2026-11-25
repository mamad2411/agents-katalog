---
name: git-branch-promotion
description: Composer — promote a refined parallel branch (e.g.,
    a reworded `master-2`) onto the canonical branch (e.g.,
    `master`) without losing any commits unique to the canonical
    side, via cherry-pick equivalence audit, unique-commit
    cherry-pick, tree-parity verification, and authorized force-push.
category: Git & Repository Management
---

# Git Branch Promotion Skill (v1)

> **Skill ID:** `git-branch-promotion`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

When a parallel branch (commonly produced by a bulk reword,
history refinement, or feature-branch atomic-commit workflow) is
ready to replace the canonical branch on `origin`, this skill:

1. Audits cherry-pick equivalence between the two branches and
   identifies commits **truly unique** to each side (modulo any
   reword/rebase that preserves the patch).
2. Backs up both branches (local **and** remote) before any
   destructive operation.
3. Cherry-picks the canonical-only commits onto the refined branch
   in **chronological order** so the refined branch becomes a
   strict superset (modulo reword).
4. Verifies tree parity (`git diff --stat == EMPTY`) and commit-count
   parity before promotion.
5. Promotes via `git reset --hard` + `git push --force-with-lease`
   under explicit user authorization.
6. Offers — but does NOT execute without authorization — cleanup of
   the refined-branch alias and the promotion backup.

## Composition Rationale

This is a **post-processing composer** that runs AFTER any history
rewriter (reword, refinement, feature branch) has produced a parallel
branch and BEFORE that branch displaces the canonical branch on the
remote.

```text
┌─────────────────────────────────────────┐
│ History Rewriter                        │
│  - git-commit-message-bulk-reword       │
│  - git-commit-message-reword            │
│  - git-history-refinement               │
│  - git-feature-branch-atomic-commit     │
│  - git-commit-edit                      │
└──────────────────┬──────────────────────┘
                   │ produces parallel/refined branch
                   ▼
┌─────────────────────────────────────────┐
│ git-branch-promotion (THIS SKILL)       │
│  audit ▸ cherry-pick uniques ▸ parity   │
│  ▸ promote ▸ cleanup                    │
└─────────────────────────────────────────┘
```

| Concern | Owner |
| --- | --- |
| Identifying unique commits between two branches via patch-id (cherry-pick equivalence) | **this skill** (`§2`); for deep unit-by-unit categorization use [`git-divergence-audit`](../git-divergence-audit/SKILL.md) |
| Single-commit reword mechanics | [`git-commit-edit`](../git-commit-edit/SKILL.md) |
| Range reword mechanics | [`git-commit-message-bulk-reword`](../git-commit-message-bulk-reword/SKILL.md) |
| Promotion (`reset --hard` + `--force-with-lease`) and backup/cleanup gates | **this skill** |

The composer **MUST NOT** reimplement reword or refinement logic. It
takes an already-refined branch as input and handles only the
audit → cherry-pick → parity → promotion → cleanup pipeline.

## Source Rules

| Rule File | Scope Incorporated |
| --- | --- |
| [`ai-rule-standardization-rules.md`](../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First Architecture, Layered Composition Mandate, Fidelity Mandate, Inter-Document SSOT |
| [`git-commit-edit/SKILL.md` Step 7b / Step 8](../git-commit-edit/SKILL.md) | Push-authorization gate; cleanup-authorization gate (re-applied to the promotion phase here) |
| [`git-divergence-audit/SKILL.md` §3](../git-divergence-audit/SKILL.md#3-asset-auditing-unit-by-unit) | When a deeper categorization (Technical / Documentation / Noise) of canonical-only commits is needed before deciding to cherry-pick |

> **Inverse use-case**: When the parallel branch's commits do NOT belong on a
> single destination but must be **fanned out** across canonical + opt-in +
> personal sandbox (e.g., the parallel branch mixes functional code, optional
> diagnostics, and personal docs), use
> [`git-parallel-branch-decommission`](../git-parallel-branch-decommission/SKILL.md)
> instead of this skill.

## Source Conversations

| Date | Topic |
| --- | --- |
| 2026-05-09 | Promotion of `master-2` (27-commit bulk reword) onto `master` in `ai-agent-rules`; cherry-picked 6 canonical-only commits, verified tree parity, force-pushed under explicit authorization |

***

## Phase Map (Executive Overview)

The skill executes in **three phases**, each gated by explicit user
authorization. The numbered sections below are the operational SSOT;
this map is the mental model.

| Phase | Name | Sections | Authorization Gate | Reversible? |
| --- | --- | --- | --- | --- |
| **Phase 1** | **Audit** — identify truly-unique commits on each side via patch-id equivalence | §1 Environment, §2 Cherry-Pick Equivalence Audit (incl. optional §2.3 deep categorization) | Read-only; no gate required | N/A (read-only) |
| **Phase 2** | **Reconcile** — back up both sides, cherry-pick canonical-only commits onto refined, prove tree parity | §3 Cherry-Pick (incl. §3.1 backup), §4 Tree-Parity Verification | User must approve the §2.2 decision and the cherry-pick list | Yes (delete refined branch + restore from `backup/pre-promote-<canonical>`) |
| **Phase 3** | **Promote** — fast-forward canonical to the refined tip locally and on `origin`, then offer cleanup | §5 Promotion (`reset --hard` + `--force-with-lease`), §6 Cleanup, §7 Submodule pointer (incl. §7.2 historical pointer repair) | **STOP gate** before §5.1 AND before §5.2 AND before §6 | Only via `backup/pre-promote-<canonical>` until cleanup runs |

**Per-phase exit criteria:**

* End of Phase 1: a `(canonical-only count, refined-only count)` pair
  plus an explicit user decision per §2.2.
* End of Phase 2: `git diff --stat <canonical> <refined>` empty AND
  commit-count parity AND `--cherry-pick --left-only` count = 0.
* End of Phase 3: `origin/<canonical>` == local `<canonical>` ==
  pre-promotion `<refined>` tip; backup branch retained until next
  session unless user authorizes its deletion.

***

## 1. Environment & Dependencies *(Phase 1)*

The agent MUST verify:

1. **Git** ≥ 2.28 (for `--force-with-lease` semantics):

    ```bash
    git --version
    ```

2. **Working tree is clean** in the parent repo (no uncommitted changes):

    ```bash
    git status --porcelain
    ```

    If non-empty, STOP and ask the user to commit, stash, or discard.

3. **Both branches exist locally and on origin**:

    ```bash
    git rev-parse --verify <canonical>           # e.g., master
    git rev-parse --verify <refined>             # e.g., master-2
    git ls-remote --heads origin <canonical> <refined>
    ```

4. **`git fetch origin --prune` is fresh** (within the current session):

    ```bash
    git fetch origin --prune
    ```

5. **Auth-failure pre-flight** (because Phase 4 of this skill is a force-push):

    If `git fetch` or any later `git push --force-with-lease` returns `HTTP 401` / `HTTP 403` /
    `Permission to ... denied to <other-user>`, the agent MUST STOP and defer to
    [Git / GitHub Auth Fallback](../git-github-auth-fallback/SKILL.md) §2 (classification) before attempting
    Phase 4. A force-push that fails halfway through credential negotiation can leave the user uncertain about
    branch state on the remote — auth MUST be resolved up front.

6. **No direct-shell tool**: When `run_in_terminal` is unavailable, route every command in this skill through
   [Terminal Fallback via VS Code Tasks](../terminal-fallback-via-vscode-tasks/SKILL.md) §3.

***

## 2. Cherry-Pick Equivalence Audit *(Phase 1)*

The goal is to find commits **truly unique** to each side after
accounting for reword/rebase (which changes SHA but preserves
patch-id).

### 2.1 Count truly-unique commits

```bash
# Truly unique to canonical (not patch-equivalent on refined):
git log --cherry-pick --left-only --no-merges --oneline \
  <canonical>...<refined>

# Truly unique to refined (not patch-equivalent on canonical):
git log --cherry-pick --right-only --no-merges --oneline \
  <canonical>...<refined>
```

> **Flag breakdown:**
>
> * `--cherry-pick` ≡ apply patch-id equivalence; commits with the same
>   patch on the other side are filtered out even when SHAs differ
>   (post-reword/rebase).
> * `--left-only` / `--right-only` restricts to the corresponding side of
>   the symmetric difference.
> * `--no-merges` excludes merge commits (their patch-id is degenerate).
> * `<A>...<B>` is the symmetric difference (commits reachable from
>   exactly one of `A`, `B`).

### 2.2 Decide

| Canonical-only count | Refined-only count | Action |
| --- | --- | --- |
| 0 | ≥ 0 | Skip §3; jump to §4 (promotion is a clean fast-forward semantically) |
| ≥ 1 | ≥ 0 | Proceed to §3 (cherry-pick canonical-only commits onto refined) |

### 2.3 (Optional) Deep categorization

If the canonical-only commits are non-trivial (mix of technical,
documentation, noise), run [`git-divergence-audit`](../git-divergence-audit/SKILL.md)
§3 to produce a Commit Action Mapping (CAM) table before deciding
which to cherry-pick vs. drop.

***

## 3. Cherry-Pick Canonical-Only Commits Onto Refined *(Phase 2)*

### 3.1 Backup BOTH branches (local + remote)

> **Critical:** This is the only safety net before §4 force-push.

```bash
git branch backup/pre-promote-<canonical> <refined>
git push origin backup/pre-promote-<canonical>
```

> **Naming convention:** `backup/pre-promote-<canonical-branch-name>`
> — the backup snapshots the **tip of the refined branch** at the
> moment cherry-picks begin, so the post-promotion canonical can be
> rolled back to it if §5 verification fails.

### 3.2 Switch to refined branch

```bash
git checkout <refined>
```

### 3.3 Cherry-pick in chronological order

List the canonical-only SHAs **oldest first**:

```bash
git log --cherry-pick --left-only --no-merges \
  --reverse --format=%H <canonical>...<refined>
```

Apply each cherry-pick **one at a time** (no batch), inspecting
each result:

```bash
git cherry-pick <sha>
git log -1 --stat   # verify it landed correctly
```

> **On conflict:** STOP, present the conflict to the user, await
> resolution. Do NOT auto-resolve. After `git add` + `git cherry-pick
> --continue`, re-verify with `git log -1 --stat`.

***

## 4. Tree-Parity Verification (Pre-Promotion Gate) *(Phase 2 exit)*

Before any destructive promotion, all three checks MUST pass.

```bash
# 1. Diff: MUST be empty
git diff --stat <canonical> <refined>

# 2. Commit count: MUST be equal
echo "canonical: $(git rev-list --count <canonical>)"
echo "refined:   $(git rev-list --count <refined>)"

# 3. Cherry-pick equivalence: canonical-only count MUST be 0
git log --cherry-pick --left-only --no-merges --oneline \
  <canonical>...<refined> | wc -l
```

| Check | Expected |
| --- | --- |
| `git diff --stat` | EMPTY (zero output lines) |
| `git rev-list --count` (both) | EQUAL |
| `--cherry-pick --left-only` count | `0` |

If **any** check fails, STOP. Return to §2 to investigate. Common
causes:

| Symptom | Likely Cause |
| --- | --- |
| Diff non-empty | A canonical-only commit was missed in §3, or a cherry-pick conflict was resolved incorrectly |
| Counts differ but diff is empty | Empty commits or merge commits in one side; re-run §2.1 with merge-handling |
| `--left-only` count > 0 | Cherry-pick was skipped or a new canonical commit landed during §3 (re-fetch and re-audit) |

***

## 5. Promotion (Authorization Gate) *(Phase 3)*

> **STOP. The agent MUST NOT execute §5.1 or §5.2 without explicit
> user authorization.** Present the proposed commands and the
> verification results from §4 to the user and wait.

### 5.1 Promote locally

```bash
git checkout <canonical>
git reset --hard <refined>
```

### 5.2 Push to origin

```bash
git push --force-with-lease origin <canonical>
```

> **Why `--force-with-lease`:** rejects the push if `origin/<canonical>`
> has advanced since the last fetch — protecting against overwriting
> a teammate's commit landed during §2-§4. **NEVER use `--force`.**

### 5.3 Post-push verification

```bash
git fetch origin --prune
git rev-parse <canonical>
git rev-parse origin/<canonical>      # MUST equal local <canonical>
git log -3 --oneline <canonical>      # spot-check tip
```

***

## 6. Cleanup (Authorization Gate) *(Phase 3 follow-up)*

> **STOP. The agent MUST NOT execute §6 without explicit user
> authorization.** Cleanup is destructive of the rollback path.

### 6.1 Order of safety

| Artifact | When safe to delete |
| --- | --- |
| Refined branch alias (`<refined>`, e.g., `master-2`) | Immediately after §5.3 verification — its tip equals `<canonical>` |
| `backup/pre-promote-<canonical>` | Only after the user confirms the published `<canonical>` looks correct (typically next session) |
| Any pre-rewrite backups (`backup/pre-bulk-reword-*`, etc.) | Owned by the upstream rewriter skill; consult its cleanup gate |

### 6.2 Commands

```bash
# Refined branch (local + remote)
git branch -D <refined>
git push origin --delete <refined>

# Promotion backup (local + remote) — only after user re-confirms
git branch -D backup/pre-promote-<canonical>
git push origin --delete backup/pre-promote-<canonical>

# Sync remote-tracking refs
git fetch origin --prune
git branch -a   # final sanity check
```

***

## 7. Parent Repository Pointer (Submodule Case) *(Phase 3 follow-up)*

If the promoted branch lives in a **submodule**, the parent repo is
affected in **two distinct ways** that MUST be addressed in order:

### 7.1 Current Pointer Bump (always required)

The parent repo's working-tree gitlink still references the **old
canonical tip**. After §5:

1. Switch to the parent repo working tree.
2. `cd <submodule-path> && git checkout <canonical> && git pull --ff-only`
3. Return to the parent: `cd .. && git status` — the submodule
   pointer change is now staged.
4. Commit the pointer bump per the parent repo's commit-message rules
   (typically a `chore(submodule): bump <name> to <new-tip>` — confirm
   via the parent's [`git-commit-message-reword` §0a](../git-commit-message-reword/SKILL.md#0a--locate-the-commit-message-rules)).

The pointer commit MUST be presented to the user for authorization
before push, per the upstream commit-edit / commit-message-reword
push gate.

### 7.2 Historical Pointer Repair (required when canonical-side history was rewritten)

If the canonical-side history of the submodule was **rewritten** (not
merely advanced) — which is exactly the case for any promotion driven
by [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md),
[`git-commit-message-bulk-reword`](../git-commit-message-bulk-reword/SKILL.md),
[`git-history-refinement`](../git-history-refinement/SKILL.md),
[`git-commit-edit`](../git-commit-edit/SKILL.md) (with content edits),
or [`git-feature-branch-atomic-commit`](../git-feature-branch-atomic-commit/SKILL.md) —
then **EVERY parent-repository commit** whose tree referenced the old
(now-orphaned) submodule SHAs is invalidated. The current-pointer bump
in §7.1 only addresses the latest pointer; historical pointers remain
broken and any clone of the parent will fail submodule initialization
at those commits.

**The parent's history MUST be repaired** via
[`git-submodule-pointer-repair` §5 (Mass Pointer Reconciliation)](../git-submodule-pointer-repair/SKILL.md#5-mass-pointer-reconciliation-full-history-rewrite-recovery)
using the **reword-tolerant match key** documented in that skill's
§5.2.0 (subject EXCLUDED — because the rewrite changes subjects).

**Pre-rewrite SHA preservation requirement.** Pointer-repair needs the
old (orphaned) submodule SHAs to remain resolvable from at least one
of:

* a **pre-rewrite local clone** of the submodule (strongest source);
* a **retained backup branch** in the rewritten submodule clone (per
  Step 0e of [`git-commit-edit`](../git-commit-edit/SKILL.md));
* an **origin fetch by SHA** while the remote still has the dangling
  commit (typically until the next remote `gc`).

The agent MUST verify at least one of these is available BEFORE
authorizing §6 cleanup of the rewritten submodule's backup branches.
Cleaning the backup before the parent's pointer-repair is complete is
FORBIDDEN — it severs the only remaining `old_sha → new_sha` mapping
source.

***

## 8. Prohibited Behaviors

* **Skipping §3.1 backup**.
* **Using `git push --force`** instead of `--force-with-lease`.
* **Executing §5 or §6 without explicit user authorization.**
* **Deleting `backup/pre-promote-<canonical>` in the same session as
  the push** — keep at least one rollback point until the user
  re-confirms the result on origin.
* **Batch cherry-picking** in §3.3 (e.g., `git cherry-pick A B C D` in
  one command). Each pick MUST be inspected individually.
* **Auto-resolving cherry-pick conflicts.**
* **Re-running §2 audit on a stale fetch.** The `--cherry-pick` filter
  is only meaningful against current refs; re-fetch before each new
  audit pass.
* **Promoting a refined branch whose tree is NOT a superset (modulo
  reword) of canonical** — i.e., §4 verification MUST pass.

***

## 9. Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| `--cherry-pick --left-only` returns commits that "should" have a match | Patch-id mismatch caused by reword that also touched body OR a rebase that re-ordered hunks — inspect with `git show <sha>` and decide manually whether to cherry-pick or drop |
| Cherry-pick produces empty commit | Means the change was already on refined under a different SHA. Use `git cherry-pick --skip` (or `--keep-redundant-commits` if you intentionally want the marker) — confirm with the user |
| `--force-with-lease` rejected with `stale info` | A teammate pushed to `<canonical>` between §1.4 fetch and §5.2 push. Re-run from §1, re-audit §2 (the new commits become canonical-only), re-cherry-pick if appropriate |
| Tree parity FAILS after cherry-picks | One of: missed cherry-pick, conflict resolved incorrectly, or a noise commit on canonical was kept when it should have been dropped — re-run §2.1 to enumerate |
| Submodule parent still points to old tip after §5 | Expected; see §7 |
| Refined branch deleted before §5.3 verification | RECOVER: `git branch <refined> backup/pre-promote-<canonical>` (the backup IS the refined-branch tip) |
| Backup branch already exists | Pick a numeric suffix (`backup/pre-promote-<canonical>-2`) — never overwrite an existing backup |

***

## 10. Related Skills

* [`git-divergence-audit`](../git-divergence-audit/SKILL.md) — deeper
  unit-by-unit (Technical / Documentation / Noise) categorization of
  canonical-only commits when §2.3 is invoked.
* [`git-commit-edit`](../git-commit-edit/SKILL.md) — base of the
  commit-rewrite stack; defines the push-authorization gate this
  skill mirrors in §5.
* [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md) —
  upstream rewriter that commonly produces the refined branch
  consumed here.
* [`git-commit-message-bulk-reword`](../git-commit-message-bulk-reword/SKILL.md) —
  range rewriter; canonical upstream that produced the
  `master-2` branch in the originating session.
* [`git-history-refinement`](../git-history-refinement/SKILL.md) —
  upstream rewriter (split / reorder); also produces a refined branch
  that this skill can promote.
* [`git-feature-branch-atomic-commit`](../git-feature-branch-atomic-commit/SKILL.md) —
  upstream rewriter (per-commit branches); consult before promoting
  to ensure each branch's PR has merged or is intentionally being
  fast-forwarded.
* [`git-dependent-branch-restack-cascade`](../git-dependent-branch-restack-cascade/SKILL.md) —
  downstream cascade. Once this skill advances the canonical tip, any
  branch (diagnostics, opt-in instrumentation, personal sandbox,
  feature stack) still rooted on the pre-promotion canonical tip must
  be restacked via the cascade composer.
* [`git-absorbed-branch-decommission`](../git-absorbed-branch-decommission/SKILL.md) —
  downstream cleanup. After this skill promotes `<refined>` onto
  `<canonical>`, the original `<refined>` branch is fully absorbed by
  `<canonical>` (by SHA in the local clone, and typically by patch-id
  if a CI/integration team has its own cherry-pick path). Use the
  absorbed-decommission skill to delete `<refined>` safely with a
  verified audit trail.

***

## 11. Composition by Higher-Level Skills

None at present. This skill is a leaf composer in the
rewrite → promote pipeline.
