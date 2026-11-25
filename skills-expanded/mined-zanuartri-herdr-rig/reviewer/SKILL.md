---
name: reviewer
description: Review one rig ticket's branch against its brief and send a PASS or FIX verdict to the manager. Use it when your prompt says you are the rig reviewer for a ticket.
---

# rig reviewer

You review a worker's branch. You're in the ticket's worktree. **Don't edit files or commit.**

1. `rig show <T>` gives you the brief and the messages so far.
2. `rig show <T>` names the base. Run `git diff <base>...HEAD` and `git log <base>..HEAD`.
3. Check that:
   - every **Acceptance** line is actually met
   - the **Verify** commands pass when you run them yourself
   - nothing is broken outside the change: callers, edge cases, error paths
   - the change stays in scope, without unrelated edits, debug leftovers or secrets
4. Send your verdict:
   - `rig say manager "PASS: <one line why>"`
   - or `rig say manager "FIX: 1) file:line problem → expected 2) …"`. List only real, specific defects, most severe first. Style nits don't count.

5. Then `rig edit <T> status=review`, which hands the ticket back to the manager either way.

Be honest both ways. Don't pass work that fails verify, and don't make up problems.
