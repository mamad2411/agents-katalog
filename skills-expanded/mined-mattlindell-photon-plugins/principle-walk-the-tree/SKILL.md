---
name: principle-walk-the-tree
description: "Apply when interviewing, scoping, or decomposing. Ask the whole frontier of currently-answerable questions at once; never guess at an answer that would unblock a question you have not asked."
user-invocable: false
---

# Walk the Tree

Decisions form a tree. Work it in rounds: ask every question whose prerequisites are settled, then wait.

**Why:** Asking questions one at a time makes the human do the sequencing. Asking a question whose answer depends on an unasked one produces an answer built on a guess, and you will not notice which part was guessed.

**Pattern:**

- **Compute the frontier.** Every decision whose prerequisites are already settled. That is the round.
- **Ask the whole frontier at once.** Numbered, each with a recommendation.
- **Defer the dependent.** A question whose answer depends on another question still open in this round belongs to a later round.
- **Recompute after every answer.** Settled decisions push the frontier outward and unblock what was waiting.
- **An empty frontier ends it.** Not "enough questions asked" - no branch left unvisited.

**Boundaries:**

- A running fact-finding sub-agent is an unsettled prerequisite. Only questions downstream of it wait; ask the rest now.

**The test:** Could you have asked one of next round's questions this round? Then you sequenced wrong. Did you answer any question on the user's behalf in order to reach a later one? Then you guessed, and the tree below that point is unsound.
