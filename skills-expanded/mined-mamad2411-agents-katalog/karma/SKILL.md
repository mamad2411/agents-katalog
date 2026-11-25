---
name: karma
description: Unpack SEAL.md at the start of a new chat -- reload the previous conversation's main topics, in-progress ideas, and learnings so it continues without re-derivation. Use when the user invokes /karma, especially early in a fresh conversation, or says something like "pick up where we left off."
---

# Karma — unpack a sealed conversation

The other half of `/seal`. Where `/seal` distills a conversation down to
three sections, `/karma` reloads them into a new chat as a short briefing,
not a raw dump — and checks whether anything in it has since gone stale
before treating it as current.

## Procedure

1. Read `SEAL.md` at the repo root. If it doesn't exist, say so plainly and
   ask whether the user wants to `/seal` the current conversation instead —
   don't fabricate a briefing from nothing.

2. Present it back as a short briefing:
   - **Main topics** — what we were doing.
   - **Ideas in process** — what's still open, phrased as decisions or work
     waiting on the user.
   - **Learnings** — what's already known, so it doesn't get re-litigated or
     re-discovered from scratch.

3. Ask explicitly which of the "ideas in process" the user wants to pick up
   now, rather than assuming the most recent one or doing all of them.

4. Treat `SEAL.md` as a snapshot, not gospel. If anything in it references a
   file, a status, or a piece of work that a quick check would confirm or
   contradict, check before relying on it — same rule as any other stored
   memory: verify before stating it as current fact.

## Where

Reads `SEAL.md` at the repo root (written by `/seal`).
