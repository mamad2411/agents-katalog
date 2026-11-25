---
name: closeout-worktree
description: Read-only dirty-worktree classification and exact-work preservation during RP-00 containment.
license: MIT
compatibility: Octon Gate-0 containment.
metadata:
  author: Octon Framework
  created: "2026-05-21"
  updated: "2026-07-14"
skill_sets: [collaborator, guardian, specialist]
capabilities: [external-dependent, safety-bounded, self-validating]
allowed-tools: Read Glob Grep Bash(git status *) Bash(git diff *) Bash(git rev-parse *) Bash(git branch *) Bash(git ls-files *) Bash(bash .octon/framework/assurance/runtime/_ops/scripts/classify-change-closeout-residue.sh *) Bash(bash .octon/framework/assurance/runtime/_ops/scripts/validate-closeout-worktree-wrapper.sh *) Write(/.octon/state/evidence/validation/analysis/*) Write(/.octon/state/evidence/runs/skills/*)
---

# Closeout Worktree — RP-00 Preservation Wrapper

During SI-00 this wrapper inventories, partitions, and reports a dirty
worktree without delegating an effect. The default is always `preserved`;
`cleaned` is never a default.

1. Bind the current worktree and exact ref baseline.
2. Inventory and classify every staged, unstaged, untracked, ignored,
   generated, evidence, control, input, and foreign path read-only.
3. Partition coherent candidates and record exact include/exclude paths,
   ownership, validation needs, and later owner.
4. Preserve every candidate, ref, branch, worktree, rollback handle, retained
   evidence item, and unrelated change.
5. Emit a `closeout-worktree-report-v1` with
   `direct_material_actions_performed: false`,
   `repo_hygiene_cleanup_actions_performed: false`, `cleaned_claim: false`, and
   `repo_hygiene_cleanup_ref: none`, plus
   `worktree_terminal_state: nonterminal` or a preservation-only disposition.

An omitted target defaults to `preserved`, never `cleaned`. Direct-main,
hosted branch-no-PR, landing, sync, landed/synced, and any effectful/default
publication request returns `RP00_CONTAINMENT_PUBLICATION_DISABLED` before
delegation. Cleanup, deletion, or `cleaned` requests return
`RP00_CONTAINMENT_CLEANUP_DISABLED` before delegation.

Do not invoke `closeout-change`, `closeout-pr`, `repo-hygiene-cleanup`, a Git or
GitHub mutation helper, a publisher, or an archive route. Do not stage, commit,
push, land, merge, fetch for mutation, checkout, reset, restore, delete, prune,
clean, remove worktrees, or mutate refs. Classification and compatibility
receipts never authorize current effects. Name RP-06/RP-08 as later owners.

If a pre-existing delegated repo-hygiene receipt is observed, record its exact
`repo_hygiene_cleanup_ref` without treating it as wrapper cleanup authority.
The wrapper validator checks delegated repo-hygiene cleanup evidence while
still requiring `repo_hygiene_cleanup_actions_performed: false`.
