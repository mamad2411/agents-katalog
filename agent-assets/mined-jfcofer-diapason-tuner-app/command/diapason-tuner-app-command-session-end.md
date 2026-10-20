---
description: Close the session so the next agent loses nothing
---

Close out this working session. Follow `AGENTS.md` §2 exactly.

1. Run `just verify`. If it is red, do not hide it — it goes in STATE.md as a blocker, with the
   exact failing command.
2. Update the active task file: tick the acceptance criteria that are genuinely met (not the ones
   that are nearly met), and fill in "Implementation notes" and "Verification performed" with what
   actually happened, including anything you tried and abandoned.
3. Rewrite `docs/agents/STATE.md` completely. It is a snapshot, not a log. Keep it under 120 lines.
   It must answer: where are we, what is active, what is next, what is blocked, what is unresolved.
4. Append a journal entry at `docs/agents/journal/YYYY-MM-DD-<slug>.md` using the template in that
   directory. The "Tried and abandoned" section is the one that pays for itself later — write it
   even when it is embarrassing.
5. If any decision this session closed off an alternative, write an ADR in `docs/adr/` and add it to
   the index. If a decided ADR turned out wrong, supersede it; never edit it.
6. If a reference doc is now inaccurate because of what you built, fix the doc in this session.
   A doc that lies is worse than no doc.
7. Show me the diff summary and the proposed commit messages. Do not push.
