---
name: cmd-ship
description: Command — Finish a development branch — verify tests, present integration options (merge/PR/keep/discard), execute.
---

# /ship

Invokes `Skill(finishing-a-development-branch)`:

1. Verifies all tests pass
2. Detects environment (worktree, normal repo, detached HEAD)
3. Presents 3–4 integration options
4. Executes the chosen option (merge / PR / keep / discard)
5. Cleans up worktree if owned

Halts on test failures. Requires typed confirmation for discard.

After integrating, the production deploy is a separate step — `Skill(deploy-checklist)` covers pre-deploy verification and rollback triggers.
