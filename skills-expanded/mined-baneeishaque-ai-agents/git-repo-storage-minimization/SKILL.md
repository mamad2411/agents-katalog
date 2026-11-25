---
name: git-repo-storage-minimization
description: Industrial protocol for minimizing on-disk size of a Git
    repository and its initialized submodules via deinitialization,
    aggressive garbage collection, reflog expiry, and pruning — without
    rewriting commit history.
category: Git & Repository Management
---

# Git Repository Storage Minimization Skill

> **Skill ID:** `git-repo-storage-minimization`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Reduce the on-disk footprint of a Git repository (and its initialized
submodules) using **non-destructive** maintenance commands:

1. **Deinitialize unused submodules** — reclaim `.git/modules/<name>/`
   working clones for submodules the user does not need locally.
2. **Aggressive repack** — `git gc --aggressive` recompresses loose
   objects into a single optimized pack.
3. **Reflog expiry + prune** — `git reflog expire --expire=now --all`
   followed by `git gc --prune=now` drops the local undo journal so
   unreachable objects can be reclaimed.

Commit history, branches, tags, and remote-tracking refs are
**preserved bit-for-bit**. The only "loss" is the local reflog
(undo log for ref movements over the past ~90 days).

This skill is the SAFE tier. For destructive size reduction
(`filter-repo`, shallow clone replacement, BFG), use a dedicated
history-rewrite skill instead.

## Source Conversations

| Date | Topic |
|---|---|
| 2026-05-09 | Storage audit of `ai-suite-2`, deinit verification, two-pass `gc` on parent + `ai-agent-rules` submodule |

## Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Shell | Bash 4+ / Zsh / PowerShell 5.1+ |
| Tools | `du` (POSIX) or `Get-ChildItem` (PowerShell) |
| State | Clean working tree recommended (gc tolerates dirty trees but skip during active rebases) |
| Access | Local filesystem only — no remote operations |

## When to Apply

Apply this skill when:

- The user explicitly asks to "shrink", "minimize", "reduce size of",
  or "clean up disk usage" of a Git repository.
- `du -sh .git` shows a footprint disproportionate to repository content.
- The user wants to deinitialize unused submodules to reclaim
  `.git/modules/` storage.
- Following a destructive operation (e.g., large file removed, history
  rewritten via [`git-history-refinement`](../git-history-refinement/SKILL.md))
  where unreachable objects need pruning.

Do NOT apply when:

- The user wants destructive history rewriting — use a dedicated
  `git-filter-repo` skill instead.
- The user wants to convert to a shallow clone — destroys history
  permanently and requires a separate explicit protocol.
- An interactive rebase, merge, or cherry-pick is in progress —
  abort or complete the operation first.
- The repository is bare and used as a remote — different protocol
  applies (no working tree, no reflog by default).

---

## Step-by-Step Procedure

### Step 0 — Pre-Minimization Audit

Before any maintenance, baseline the current footprint and identify
recoverable storage.

#### 0a — Baseline `.git` Disk Usage

```bash
cd <repo-root>
du -sh .git
du -sh .git/* 2>/dev/null | sort -h
```

**Pedagogical breakdown:**

- `du -sh .git` — total `-s`ummary in `-h`uman-readable units.
- `du -sh .git/* | sort -h` — per-subdirectory breakdown sorted
  by size. Identifies the dominant consumers (typically `objects/`
  and `modules/`).

#### 0b — Inventory Initialized Submodules

```bash
git submodule status
ls .git/modules 2>/dev/null
du -sh .git/modules/* 2>/dev/null | sort -h
```

**Pedagogical breakdown:**

- `git submodule status` — prefix `+` = initialized & checked out,
  `-` = not initialized (zero disk cost), `U` = merge conflict.
- `.git/modules/<name>/` — per-submodule `.git` clone. Only
  initialized submodules occupy storage here.

#### 0c — Classify Submodules

Present the user with a table:

| Submodule | Status | `.git/modules/` size | Recommendation |
|---|---|---|---|
| `<name>` | initialized | `<size>` | Keep / deinit |

#### 0d — Present the Minimization Plan

The agent **MUST** present and obtain explicit user approval for:

````markdown
## Storage Minimization Plan

**Repository:** `<repo-root>`
**Current `.git` size:** `<X> MB`

### Phase 1 — Submodule deinitialization
- Keep: `<list>`
- Deinit: `<list>` (estimated reclaim: `<Y> MB`)

### Phase 2 — Aggressive repack on parent
- `git gc --aggressive --prune=now`
- Reclaims duplicate / loose objects.

### Phase 3 — Reflog expiry + final prune
- `git reflog expire --expire=now --all`
- `git gc --prune=now`
- ⚠️ **Drops local reflog** — recent ref movements (last ~90 days)
  cannot be undone via `git reflog` after this step.

### Phase 4 — Same passes on each kept submodule

### Estimated total reclaim: `<Z> MB`

Proceed? (yes / no)
````

**The agent MUST NOT execute any minimization step until the user
confirms.**

---

### Step 1 — Deinitialize Unused Submodules

For each submodule the user wants to deinitialize:

```bash
git submodule deinit -f -- <path>
rm -rf .git/modules/<path>
```

**Pedagogical breakdown:**

- `git submodule deinit -f -- <path>` — removes the submodule's
  working tree contents and clears the active flag in
  `.git/config`. The `-f` is required when the working tree has
  uncommitted changes; the `--` ends option parsing.
- `rm -rf .git/modules/<path>` — deletes the cached `.git`
  directory. `git submodule deinit` does NOT remove this on its
  own; it is the dominant storage win.

**Verification:**

```bash
git submodule status | grep "^-" | wc -l   # count uninitialized
du -sh .git/modules/* 2>/dev/null
```

The deinitialized entry should now show `-` prefix and be absent
from `.git/modules/`.

> [!NOTE]
> Deinit does NOT alter `.gitmodules` or the parent's recorded
> gitlink SHA. Reinitializing later is a single
> `git submodule update --init --recursive <path>`.

---

### Step 2 — Aggressive Garbage Collection (Parent)

```bash
git gc --aggressive --prune=now
```

**Pedagogical breakdown:**

- `git gc` — invokes the maintenance routine: repack, prune,
  reflog expire (with default windows).
- `--aggressive` — uses higher-quality pack heuristics (`-f`
  forced repack, larger window/depth). Slower but produces a
  smaller pack file.
- `--prune=now` — removes loose objects whose mtime is older than
  "now" (i.e., all unreachable loose objects). Default would only
  prune objects older than 2 weeks.

> [!IMPORTANT]
> `gc --aggressive` is CPU-intensive. On large repositories
> (≥ 1 GB), expect multi-minute runtimes. Do not run during
> active rebase / merge / cherry-pick.

---

### Step 3 — Reflog Expiry + Final Prune (Parent)

```bash
git reflog expire --expire=now --all
git gc --prune=now
```

**Pedagogical breakdown:**

- `git reflog expire --expire=now --all` — for `--all` refs, expire
  every reflog entry whose age is `<now`, i.e., the entire reflog.
  This severs the only reference to "lost" commits (e.g., commits
  abandoned by `--amend`, `reset --hard`, dropped rebases).
- `git gc --prune=now` — second pass, no `--aggressive` since
  pack was just rebuilt; the prune now reclaims objects that were
  reachable only via reflog.

> [!CAUTION]
> After this step, `git reflog` is empty. Recovery of
> recently-abandoned commits via `git reflog show` is no longer
> possible. Backup branches created via the
> [`git-commit-edit`](../git-commit-edit/SKILL.md) skill are
> still preserved (they are real refs, not reflog entries).

---

### Step 4 — Repeat on Each Kept Submodule

For every submodule still initialized:

```bash
git -C <submodule-path> reflog expire --expire=now --all
git -C <submodule-path> gc --aggressive --prune=now
```

**Pedagogical breakdown:**

- `git -C <path>` — runs the command as if `git` was invoked from
  inside `<path>`. Avoids `pushd`/`popd` and is the canonical
  way to operate on submodules from the parent root.
- Submodules have their own `.git/objects/` (located at
  `.git/modules/<name>/objects/`). The parent's `gc` does NOT
  touch submodule objects.

---

### Step 5 — Final Audit

```bash
du -sh .git
du -sh .git/modules/* 2>/dev/null | sort -h
```

Present a before / after comparison table:

| Component | Before | After | Reclaimed |
|---|---|---|---|
| `.git` total | `<X> MB` | `<Y> MB` | `<X-Y> MB` |
| `.git/modules/<name>` | `<A> MB` | `<B> MB` | `<A-B> MB` |

If the reclaim is negligible (< 5 %), inform the user that the
repository was already well-packed and further reduction requires
destructive operations (out of scope for this skill).

---

## Scope Coverage

| Category | Convention |
|---|---|
| Submodule deinit | `git submodule deinit -f -- <path>` + `rm -rf .git/modules/<path>` |
| Loose object repack | `git gc --aggressive --prune=now` |
| Reflog reclamation | `git reflog expire --expire=now --all` + `git gc --prune=now` |
| Submodule maintenance | `git -C <path> gc --aggressive --prune=now` |
| History preservation | All commits / branches / tags retained bit-for-bit |
| Reflog destruction | Local reflog wiped — backup branches recommended for high-risk operations |

---

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Executing any minimization step without explicit user approval**
  of the per-step plan presented in §0d.
- **Deinitializing submodules silently** — every deinit MUST be
  individually authorized in the plan.
- **Running `git gc` during an in-progress rebase / merge /
  cherry-pick** — verify with `git status` first; abort or
  complete the operation.
- **Suggesting destructive history rewriting** (`git filter-repo`,
  BFG, shallow conversion) within this skill — those require a
  separate explicit protocol.
- **Pruning before the user is informed that reflog history will
  be wiped** — the §0d plan MUST surface this consequence.
- **Skipping the before/after audit** — quantified reclaim is
  the only proof the operation succeeded.

---

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| `gc --aggressive` reclaims < 1 % | Repository is already optimally packed; further reduction requires destructive history rewriting (out of scope) |
| `git submodule deinit` leaves `.git/modules/<name>/` intact | Manually `rm -rf .git/modules/<name>/` after deinit — Git intentionally preserves the cached clone for fast re-init |
| `gc` fails with "fatal: gc is already running" | Stale `gc.pid` lock — verify no `git gc` process exists, then `rm .git/gc.pid` |
| `gc` aborted mid-run — repository corrupted? | `git fsck --full` to verify integrity; loose objects from interrupted repack are harmless and pruned on next `gc` |
| Reflog expiry destroys an undiscovered backup | Always create a real branch (`git branch backup/<name>`) for high-value states BEFORE running this skill — reflog is not a backup |
| Submodule `gc` skipped — parent looks unchanged | The parent's `.git/objects/` and the submodule's `.git/modules/<name>/objects/` are independent stores; both need separate maintenance |
| Network filesystem (NFS, SMB) — repack is slow / fails | Maintenance MUST be run on a local filesystem; copy the repo, gc, copy back |

---

## Related Skills

- [`git-commit-edit`](../git-commit-edit/SKILL.md) — creates backup
  branches that survive reflog expiry.
- [`git-submodule-removal`](../git-submodule-removal/SKILL.md) —
  permanent submodule removal (different from deinit).
- [`git-submodule-uninitialized-handler`](../git-submodule-uninitialized-handler/SKILL.md) —
  inverse operation; drives uninitialized submodules to a fully
  initialized state.
