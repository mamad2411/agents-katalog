---
name: stacked-prs
description: |
  Use when dependent changes need separate, reviewable pull requests and a lower layer
  changes, merges, is retargeted, or is restacked while descendants remain open.
---

# Stacked pull requests

A stack is a chain of small, dependent PRs. Each PR has one logical change and targets the
branch immediately below it. Independent changes are parallel PRs, not a stack. Merge and
restack bottom-up; a child is not ready merely because its parent changed.

Author each layer's commit and PR text with `../change-writing/SKILL.md` (output-only); this skill
keeps sole ownership of base-branch topology, restack leases, and readback.

## Safety doctrine

- Save an old boundary for every layer before any operation: branch, local tip, PR number,
  base/head names, and exact remote OID. A changed target, base, head, or PR state invalidates
  the candidate; stop, re-query, re-gate, and re-review. Target/base/head/state drift invalidates
  the candidate. Every check occurs immediately before mutation.
- Never assume a hosting service changes a child target. After a parent merges, is abandoned,
  or is renamed, explicitly retarget each immediate child to the verified replacement base.
  Re-query `baseRefName`, `headRefName`, and `state` after each retarget before continuing.
- Before rewriting a stack, preserve every old parent boundary in an old-parent map. Build a
  new-parent map as each layer is rewritten, then cascade from the parent outward (nearest
  child first). For each child, use its saved old parent and current new parent exactly:

  ```sh
  git rebase --onto <new-parent> <saved-old-parent> <child>
  ```

  This replays only that child's commits; never replay ancestor commits or an ancestor range.
  Re-gate and re-review every rewritten or retargeted layer, obtaining fresh review.
- Before deleting any branch, re-query all open PRs and their base fields. Do not delete while
  any open PR uses that branch as a base. Missing, stale, unsupported, or HTTP 403 governance
  evidence means governance is UNKNOWN; UNKNOWN is not approval.
- Immediately before every rewrite or deletion, perform a final race check: re-read the saved
  remote OID (the saved remote OID), PR base/head/state, open-child usage, required checks, and governance. Any change
  invalidates the candidate and requires a fresh boundary and review. Only after that readback
  may a remote branch be deleted, and deletion must use the exact saved-OID lease:

  ```sh
  git push --force-with-lease=refs/heads/<branch>:<saved-remote-oid> origin :refs/heads/<branch>
  ```

  Never use ordinary unleased deletion, an unqualified lease, or `--force`. A lease failure or
  changed final readback is a stop, not a retry.

## Normal shape

```
main <- feat-a (PR 1) <- feat-b (PR 2) <- feat-c (PR 3)
```

Create each PR against the immediate parent. Keep the stack shallow (usually 2–4 layers),
keep a stack map in each PR, and merge only bottom-up. A child PR remains open while its
parent is reviewed; that is not permission to remove the parent branch.

## Rewrite discipline

For every rewritten branch, save its current remote OID before the final race check, preserve
the old parent boundary, and inspect the result before gating and review. Push only with the
exact saved-boundary lease:

```sh
git push --force-with-lease=refs/heads/<branch>:<saved-remote-oid> origin <branch>
```

A lease failure or changed readback is a stop: preserve evidence, re-query, and start a new
authorized candidate.
