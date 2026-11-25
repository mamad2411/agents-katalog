---
name: git-merge-into-branch
description: Merges the branch you started on into a named target, pushes the target, then switches back.
disable-model-invocation: true
---

# Git merge into target branch

**Land** means: `target` receives a merge of the branch you started on (`source`), then you return to `source`.

`target` = branch name from this message (trimmed). If missing or ambiguous, ask once and stop.

## Steps

1. `source =` `git branch --show-current`. If `source` equals `target`, report and stop.
2. `git status --short`. Uncommitted changes → stop; do not stash/discard unless told in this message.
3. `git fetch --all` when network is allowed (else use existing refs and say so).
4. Resolve `target`:
   - Local exists → use it
   - Else `origin/target` exists → `git switch -c target --track origin/target` (or `git switch target` if Git creates the tracking branch)
   - Else → report missing; stop (do not invent branches)
5. `git switch target` then `git merge source` (repo defaults for ff/merge).
6. Conflicts → list files, stay on `target`, stop for manual resolve/abort.
7. After a clean merge: push `target` (`git push`, or `git push -u origin <target>` if no upstream). Push failure or no remote → stay on `target`, report; switch back only after push succeeds or the user says to skip push and switch back.
8. After push succeeds: `git switch source`.
9. **Done when:** `target` contains the merge, push succeeded (or skip authorized), and HEAD is back on `source` — or you stopped at a hard stop above.

## Guardrails

- Do not push `source` or other branches unless this message asks.
- No rebase, `--force`, or `reset --hard` unless explicitly requested.
