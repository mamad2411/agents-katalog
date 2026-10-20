---
name: principle-close-or-block-the-dimension
description: "Apply at the end of any planning session. Every dimension ends either settled or as a named decision ticket - never merely discussed."
user-invocable: false
---

# Close or Block the Dimension

Each of the four dimensions - `problem`, `shape`, `approach`, `verification` - leaves the session in one of exactly two states: settled, or a decision ticket someone owns.

**Why:** A dimension that was discussed but not resolved reads downstream as open, so execution pays full rigor for it anyway - you did the thinking and got none of the savings. Worse, nobody knows it is outstanding, because a conversation is not a queue.

**Pattern:**

- **Two states only.** Settled or blocked. "Mostly agreed" is open. "We talked about it" is open.
- **A blocked dimension gets a ticket**, declaring `closes: <dimension>` and blocking the work that depends on it.
- **Match the ticket to the resolver.** Needs a structure worked out, `shape`. Needs an empirical answer, `approach` via `prototype`. Needs outside facts, `research`.
- **Closing the ticket updates the blocked work.** Whoever resolves it records which dimension was decided and with what.

**Boundaries:**

- Leaving a dimension open is legitimate and often correct. Leaving it open *silently* is the failure.

**The test:** Read back the `settled:` block. For every dimension not in it, can you name the ticket that will close it and who owns that ticket? If not, you left it merely discussed.
