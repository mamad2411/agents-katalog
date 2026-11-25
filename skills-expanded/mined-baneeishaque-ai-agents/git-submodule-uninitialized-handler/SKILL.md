---
name: git-submodule-uninitialized-handler
description: Recursive remediation skill that consumes the uninitialized-audit report and drives every pointer to a fully-initialized state — initializing reachable ones, recovering orphan gitlinks, and re-pointing dead upstreams via fork.
category: Git & Repository Management
---

# Git Submodule Uninitialized Handler Skill (v1)

This skill is the **remediation half** of the audit/handler pair. It consumes the report produced by
[`git-submodule-uninitialized-audit`](../git-submodule-uninitialized-audit/SKILL.md) and drives every uninitialized
pointer (top-level **and** nested) to one of three terminal states: **Initialized**, **Recovered-via-Fork**, or
**Removed-as-Unrecoverable**. The skill is strictly remedial — it does NOT re-enumerate or re-classify; that
responsibility belongs to the audit skill.

The end-state contract: after this skill runs, `git submodule status --recursive | grep '^-'` MUST return zero lines
and `git submodule foreach --recursive --quiet 'test -e .git || echo MISS'` MUST be empty.

***

## 1. Environment & Dependencies

Before execution, the agent **MUST** verify the industrial environment.

1. **Verify Git** (`>= 2.30`):

    ```bash
    git --version
    ```

2. **Verify GitHub CLI** (required for orphan recovery via fork):

    ```bash
    gh --version
    gh auth status
    ```

3. **Verify Audit Report Exists**: This skill MUST NOT execute without a fresh audit report from
   [`git-submodule-uninitialized-audit`](../git-submodule-uninitialized-audit/SKILL.md). If no report exists,
   the agent MUST run the audit skill first.

4. **Position at parent repo root**:

    ```bash
    cd "$(git rev-parse --show-toplevel)"
    ```

***

## 2. Pre-Flight Safety Checks

Before any mutation, capture an undo anchor and assert clean state.

1. **Capture pre-state hashes** (parent + every initialized submodule), so the user can `git reset --hard <sha>` if
   needed:

    ```bash
    PAGER=cat git rev-parse HEAD > /tmp/submodule-handler-parent-pre.sha
    PAGER=cat git submodule foreach --recursive --quiet 'echo "$displaypath $(git rev-parse HEAD)"' \
        > /tmp/submodule-handler-children-pre.txt
    ```

2. **Reject dirty working tree** (the handler MUST NOT bury user changes inside automated commits):

    ```bash
    if [ -n "$(git status --porcelain)" ]; then
        echo "FAIL: working tree dirty — commit or stash before running handler" >&2
        exit 1
    fi
    ```

3. **Reject existing index lock** (proves no other git process is mid-write):

    ```bash
    [ -e .git/index.lock ] && { echo "FAIL: stale .git/index.lock present" >&2; exit 1; }
    ```

***

## 3. Phase 1: Initialize Reachable Pointers

For every pointer the audit verdict-table marked **Uninit-Reachable**, perform a bounded recursive init.

1. **Bulk init for the parent** (initializes every top-level reachable pointer; nested pointers are picked up by
   `--recursive`):

    ```bash
    PAGER=cat git submodule update --init --recursive --jobs 4
    ```

    * `--init` — registers entries from `.gitmodules` into `.git/config` if absent, then clones.
    * `--recursive` — descends into each newly-cloned submodule and inits its own pointers.
    * `--jobs 4` — bounded parallelism. Higher values (`8`, `16`) commonly trigger GitHub rate-limit / connection
      reset on large supersets; `4` is the empirically-safe default for personal accounts.

2. **Per-pointer init** (when bulk init is undesirable — e.g., a single submodule needs a different `--depth`):

    ```bash
    PAGER=cat git submodule update --init --recursive --jobs 4 -- <path>
    ```

3. **Retry on `BUG: refs/files-backend.c` errors** — this is a known transient race when many submodules init in
   parallel; git auto-retries internally, and the user-visible result is success. Run the same command a second time
   to converge:

    ```bash
    PAGER=cat git submodule update --init --recursive --jobs 4
    ```

***

## 4. Phase 2: Recover Orphan Gitlinks

For every pointer the audit marked **Orphan-Gitlink**, delegate end-to-end to
[`git-submodule-orphan-gitlink-recovery`](../git-submodule-orphan-gitlink-recovery/SKILL.md). That skill itself
recursively delegates to:

- [`git-submodule-dead-upstream-audit`](../git-submodule-dead-upstream-audit/SKILL.md) for SHA-based discovery.
- [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md) when the parent submodule is
  read-only.

The handler MUST execute the orphan-recovery skill **once per containing submodule** (not once per orphan), because a
single fork + branch can carry registrations for multiple sibling orphans atomically.

After the orphan-recovery skill returns:

1. **Re-init the affected submodule** so the newly-recovered nested pointers materialize:

    ```bash
    PAGER=cat git submodule update --init --recursive --jobs 4 -- <orphan-containing-submodule-path>
    ```

***

## 5. Phase 3: Re-point Unreachable Pointers

For every pointer the audit marked **Uninit-Unreachable** (HTTP 4xx/5xx + dead-upstream audit returned ≥1 fork SHA):

1. **Apply [`git-submodule-fork-reconfigure`](../git-submodule-fork-reconfigure/SKILL.md)** §2–§4 to point the
   parent's `.gitmodules` entry at the discovered fork.
2. **Re-init**:

    ```bash
    PAGER=cat git submodule update --init --recursive --jobs 4 -- <path>
    ```

When the dead-upstream audit returned **zero** fork SHAs (truly unrecoverable), the handler MUST present the evidence
to the user and obtain explicit approval before invoking
[`git-submodule-removal`](../git-submodule-removal/SKILL.md). Auto-removal is **FORBIDDEN**.

***

## 6. Phase 4: Convergence Loop

The audit may be stale by the time Phase 1 completes (newly-cloned submodules can themselves contain unregistered
nested pointers that were not visible during the original audit). Run a tight convergence loop until the end-state
contract holds.

```bash
max_iters=3
i=0
while [ $i -lt $max_iters ]; do
    uninit=$(git submodule status --recursive | grep -c '^-' || true)
    if [ "$uninit" -eq 0 ]; then
        echo "Converged after $i additional iterations."
        break
    fi
    echo "Iteration $((i+1)): $uninit pointers still uninitialized — re-running init."
    PAGER=cat git submodule update --init --recursive --jobs 4
    i=$((i+1))
done
```

* `max_iters=3` — empirical bound. Three iterations cover the common case (parent → child → grandchild). If the loop
  fails to converge in 3 passes, the remaining pointers are categorically Orphan-Gitlink or Unreachable and MUST be
  routed back through Phase 2 / Phase 3.

***

## 7. Phase 5: End-State Verification

The handler MUST prove the contract before reporting success.

1. **Zero uninitialized**:

    ```bash
    PAGER=cat git submodule status --recursive | grep '^-' && echo "FAIL: uninit remain" || echo "OK: zero uninit"
    ```

2. **Zero empty submodule directories**:

    ```bash
    PAGER=cat git submodule foreach --recursive --quiet \
        'if [ ! -e .git ]; then echo "EMPTY: $displaypath"; fi'
    ```

    * Empty output = success.

3. **Pointer SHA == recorded SHA** for every pointer (no `+` prefixes):

    ```bash
    PAGER=cat git submodule status --recursive | grep '^+' && echo "FAIL: drift" || echo "OK: no drift"
    ```

4. **Generate post-state report** for diff against pre-state captured in §2.1:

    ```bash
    PAGER=cat git rev-parse HEAD > /tmp/submodule-handler-parent-post.sha
    PAGER=cat git submodule foreach --recursive --quiet 'echo "$displaypath $(git rev-parse HEAD)"' \
        > /tmp/submodule-handler-children-post.txt
    diff /tmp/submodule-handler-children-pre.txt /tmp/submodule-handler-children-post.txt || true
    ```

***

## 8. Operational Safety

- **No Force Push**: This skill NEVER force-pushes. Any push is `git push -u origin <branch>` to a fresh branch on a
  personal fork; pushes to upstream `origin` of read-only repos are FORBIDDEN.
- **No Auto-Removal**: Submodule removal requires explicit user approval per Phase 3.
- **No Bypass of Audit**: The handler MUST NOT enumerate pointers itself; doing so duplicates the audit skill's
  primitive and violates the SSOT contract. If the audit is missing or stale, re-run the audit skill first.
- **Bounded Parallelism**: `--jobs 4` is the upper bound. Higher values trigger transient `git: BUG:
  refs/files-backend.c:3188` and connection-reset failures, particularly when mixed with dead-URL clones.
- **Token Hygiene**: When invoking sub-skills that consume `$GH_TOKEN`, the handler MUST NOT log the token.
- **User Approval Gate**: Whenever Phase 2 or Phase 3 produces a fork URL, the handler MUST display the proposed
  parent `.gitmodules` diff and obtain `y/n` confirmation before committing. Silent re-pointing is FORBIDDEN.
- **Recursive Submodule Mandate** (per
  [`ai-rule-standardization-rules.md`](../../../ai-agent-rules/ai-rule-standardization-rules.md)): every documented
  init/update command in this skill uses `--recursive`; non-recursive variants are **FORBIDDEN**.

***

## 9. Composition Rationale

This skill is a **remediation composer** that orchestrates four base/composer skills:

```text
                                ┌─ git-submodule-uninitialized-audit       (consumed report)
                                │
git-submodule-                  ├─ git-submodule-orphan-gitlink-recovery   (Phase 2 — orphans)
uninitialized-handler  ─────────┤
                                ├─ git-submodule-fork-reconfigure          (Phase 3 — re-point)
                                │
                                └─ git-submodule-removal                   (Phase 3 — last resort, gated)
```

* **Audit consumption**: this skill MUST start from the audit report; re-enumeration is FORBIDDEN.
* **Orphan recovery delegation**: orphan-gitlink-recovery itself transitively composes dead-upstream-audit and
  fork-reconfigure — this skill never invokes those two directly when the cause is an orphan.
* **Direct fork-reconfigure**: invoked only for the Unreachable-but-recoverable case where there is no orphan
  involved (the parent's own `.gitmodules` URL is dead but the SHA exists in a fork).
* **Removal**: invoked only for truly-unrecoverable pointers, after explicit user approval.

Inlining any of the above primitives is **FORBIDDEN** by the Layered Composition Mandate.

***

## 10. Related Skills

- [Git Submodule Uninitialized Audit](../git-submodule-uninitialized-audit/SKILL.md) — produces the input this
  skill consumes.
- [Git Submodule Orphan Gitlink Recovery](../git-submodule-orphan-gitlink-recovery/SKILL.md) — Phase 2 delegate.
- [Git Submodule Fork Reconfigure](../git-submodule-fork-reconfigure/SKILL.md) — Phase 3 delegate.
- [Git Submodule Dead Upstream Audit](../git-submodule-dead-upstream-audit/SKILL.md) — invoked transitively via
  orphan-recovery.
- [Git Submodule Removal](../git-submodule-removal/SKILL.md) — last-resort delegate, gated by user approval.

***

## 11. Traceability

- Origin session: **AI Suite Submodule Audit** (May 2026) — formalizes the init / orphan-recover / fork-reconfigure
  pipeline used to bring the workspace from ~30 uninitialized pointers to zero, including nested
  `gudastudio_skills/{collaborating-with-codex,collaborating-with-gemini}` and the
  `ljt-520_openclaw-backup/Star-Office-UI` recovery.
- Standard authority: [Skill Factory](../skill-factory/SKILL.md) §2.0 (Layered Composition).
- Compatibility: macOS, Linux, Windows (Git Bash / Zsh).
