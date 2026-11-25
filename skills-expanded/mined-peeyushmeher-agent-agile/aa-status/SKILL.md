---
name: aa-status
description: Use when the user asks for status, progress, an overview, "where are we", a roadmap summary, or Key Result progress on an Agent-Agile project, for example "/aa-status", "how's this project going", "what's left to do".
license: MIT
metadata:
  system: agent-agile
---

# aa-status

Read-only — never write to any file, never dispatch a subagent.

If `.planning/STATE.md` does not exist, say so and point the user at the three front doors: a vague spark → `/aa-grill`, a clear idea → `/aa-new-project`, an existing plan or spec → `/aa-import`.

Otherwise, render four sections in order, sourced from the files named:

1. **Roadmap.** Read `.planning/ROADMAP.md` and reproduce its epic table as-is: number, epic name, demo sentence, initiative served, and status.
2. **State.** Read `.planning/STATE.md` and summarize its fields in plain language: which phase the project is in, what's in progress now, what's next, and any blocker.
3. **Key Result progress.** Read `.planning/PROJECT.md`'s Key Results list and restate each one. For any Key Result whose progress is evidenced elsewhere on disk — a `LEARNINGS.md` note, a verified epic whose demo sentence maps onto it — note that evidence next to it; otherwise mark it as not yet measured. Never invent a number that isn't backed by something on disk.
4. **Outstanding prerequisites.** Read `.planning/PREREQS.md` and list only the rows whose status is not `verified` (that is, `pending` or `done`) — a `done` row still belongs here, because "done" without "verified" means nobody has confirmed it actually works yet. If every row is `verified`, say so explicitly rather than showing an empty section.

Present all four sections together as one status report; don't ask the user which section they want first.
