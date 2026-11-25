---
name: git
description: Router for user-invoked git skills — commit, push, sync, switch branch, land onto another branch.
disable-model-invocation: true
---

# Git skills

Type the skill name in chat (or attach it). This router only names them — invoke each skill yourself.

| Skill | Reach for it when |
| --- | --- |
| `git-commit` | Stage everything and create **one** Conventional Commits commit (no push) |
| `git-push-branch` | Push **existing** commits on the current branch only (no stage/commit) |
| `git-fetch-pull` | Sync: `fetch --all` then `pull` on the current branch |
| `git-checkout-branch` | Switch to a named branch; create only after explicit confirm |
| `git-merge-into-branch` | Land the branch you are on onto a named target, push target, switch back |

Args go in the same message (e.g. `git-checkout-branch feature/foo`, `git-merge-into-branch main`).
