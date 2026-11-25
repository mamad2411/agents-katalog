---
name: modernize
description: Close the grid gaps that need judgment (split a big file, name with meaning, type strictly, write tests) one by one from `ion repo score --roadmap`: tests first, proof by `--rule ID`, one commit per gap. Use when the user asks to modernize a repo, raise its score or work the roadmap.
argument-hint: "[RULE-ID]"
---

Gap asked for: `$ARGUMENTS`; otherwise the first item of the roadmap. Talk to the user in their
language. Scripts close what they can first: if `ion repo score` lists gaps fixed by `ion repo fix`,
offer to run it before anything else (no token spent).

1. A branch in its worktree (`/repo:worktree`, `chore/modernize-<rule-id>` in lowercase), then
   `ion repo score --roadmap` there. Pick the item; read its rule (`ion repo grid <ID>`: why, sources,
   what passes). Open only the places the roadmap quotes, and what they call or import when the
   change needs it: the roadmap is there so you do not explore the repo.
   An item whose `ion repo fix` commit broke a check names its log: its first line gives the branch
   the commit waits on; cherry-pick it, make the check green again, and that is the gap closed.
2. **To confirm** (an approximate detector): look at each place once. A real gap stays in the
   list; a false positive is dismissed for good, with the user's yes:
   `ion repo waive <ID> --paths <file> --permanent --reason "false positive: <why, in a few words>"`.
   It never comes back, and counts as a false positive of the rule.
3. **A product decision** (behaviour a user sees, data kept or dropped, an API that changes, a
   name the team chose): stop and ask; do not guess.
4. **Safety net first**: when the code you are about to change has no test that runs it, write
   characterization tests that pin what it does today (old repos break when modernized blind),
   run them green, commit them on their own (`test: …`).
5. The change, as small as closes the gap. Then the repo's checks (`ion repo check`, or the commands
   its `CLAUDE.md` gives) and `ion repo score --rule <ID>`: it must pass and the checks stay green;
   otherwise fix or undo, never leave half of it. One commit per gap
   (`refactor: …` or `fix: …`, the rule ID in the body), with the ticket closed if `--write` made
   one.
6. Next item, or stop when the user says so or the session's budget is spent. At the end:
   `ion repo score` before and after, the gaps closed, the ones dismissed, what is left; then
   `/repo:merge`.
