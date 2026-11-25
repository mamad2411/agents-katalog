---
name: principle-write-it-down
description: "Apply whenever a decision is reached, a term is pinned, or a session ends. A decision that was not recorded did not happen."
user-invocable: false
---

# Write It Down

The output of planning is an artifact, not an understanding. Agreement that lives only in a transcript is agreement nobody can act on.

**Why:** The next agent - or you next week - has no transcript. Planning that ends in a shared feeling has moved the work rather than done it. Writing inline also catches disagreements while they are still cheap; a glossary written afterward records what you remember, not what was decided.

**Pattern:**

- **Capture terms as they resolve.** `CONTEXT.md` gets the entry the moment the term is pinned, not at the end.
- **A glossary is a glossary.** No implementation decisions in it. Those go to an ADR.
- **ADR only when all three hold:** hard to reverse, surprising without context, the result of a real trade-off. Miss one and skip it.
- **Every session ends in a spec, tickets, or both**, carrying a `settled:` block.
- **Record what you rejected** when the rejection is non-obvious, or it gets re-proposed in six months.

**Boundaries:**

- Not everything deserves a document. A reversible, obvious, unsurprising choice needs no ADR - you would only reverse it.

**The test:** If everyone in this session vanished, could someone pick up the artifact and build the right thing? If the answer depends on remembering the conversation, you have not written it down.
