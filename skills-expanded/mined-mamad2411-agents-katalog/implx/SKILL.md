---
name: implx
description: Use only when the user explicitly says implx or asks to invoke the SpecRail queue shortcut. Inventory and drain the authorized issue and PR queue from current GitHub state.
---

# Implx

Implx is explicit. Never start it from a generic request to implement or review
one item.

## Startup

1. Read repository instructions and current Issues, PRs, reviews, CI, branches,
   and worktrees.
2. Search for duplicate and already-owned work.
3. Inventory the full queue, then select a bounded tranche.
4. Record item, owner, original branch/PR, done-when, verification, blocker, and
   next action.

## Order

1. Finish existing non-draft PRs.
2. Resume Issues with an existing remote branch.
3. Start unowned actionable Issues.
4. Re-audit the queue after every tranche.

For each item, use repository-native tests and current remote state. Preserve
disjoint ownership if the user requested parallel agents. Push, comment,
resolve threads, close, and merge only within the caller's explicit
authorization. Never force-push.

`implx auto` permits unattended continuation only for the named run. It does
not broaden repository, security, publication, or external-action authority.
