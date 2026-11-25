---
name: review-instructions
description: Review a change to a key file, the text bots read as orders (AGENTS.md, skills, profiles, team templates), as the bot that will receive it.
---

# Review instructions

The files in `docs/key-files.md` are read by bots as orders. A wrong sentence is followed
by every bot at its next prompt, so review the text like code that runs everywhere.

1. **Read it as the receiver.** Take the bot that gets it, with its composed guide and its
   skills. Would a bot with only that text do the right thing? Is any sentence open to a
   second reading?
2. **Look for a contradiction.** Search the other key files for the same subject (a label,
   a rule, a name) and compare. Say which files you read.
3. **Check each claim against the code.** A page, a setting, a route, a name: open the code and
   see that it is there. A sentence that is not true is worse than a missing one.
4. **Say the blast radius.** Which bots, which workspaces, from when.
5. **Say how it reaches them.** `AGENTS.md` reaches bots when the board is rebuilt. A skill or a
   profile reaches them when the registry copy is updated, which a person does after the merge.
   Name the step, or say that it is missing.
6. **Smallest change.** A rule spelled in a new place is a copy that will drift. Link to the
   one that exists.

Verdict: on the exact commit, naming the key files touched and the ones read. The merge needs
the same two reviews as any pull request; the human is not a gate. If the change is only wording,
say so.
