---
name: write-adr
description: Writes an architecture decision record for a decision your team just made, with context, options weighed and consequences.
disable-model-invocation: true
---

Write an architecture decision record. The decision: $ARGUMENTS

1. Look for an existing ADR folder (docs/adr, docs/decisions, adr/). Copy its file naming, next number, template and status vocabulary. If none exists, propose `docs/adr/0001-<slug>.md`.
2. Gather evidence from the repository: the code and dependencies involved, relevant pull requests or commit messages (`git log --oneline -n 30 -- <path>`), and any older ADR this one changes.
3. Write the sections: Title, Status (proposed unless the user said accepted), Date, Context (the forces and constraints, in plain words), Decision (one active-voice paragraph starting "We will"), Options considered (each with real pros and cons), Consequences (good, bad and what we must now do).
4. Mark every claim you could not verify with "to be confirmed" instead of making up numbers, owners or dates.
5. If the decision replaces an earlier ADR, say so in both files.

Keep it to one page. Show the draft, list the open items, and ask before creating the file or editing the status of any older record.
