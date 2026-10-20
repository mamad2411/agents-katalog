---
name: principle-block-on-the-human
description: "Apply when an open question could be answered by the person in front of you. In an interactive planning session the human is the cheapest resolver of ambiguity - ask, and wait."
user-invocable: false
---

# Block on the Human

Planning is interactive work. The person in front of you is the cheapest and fastest way to resolve an ambiguity, and using them is the point of the session, not a failure of it.

**Why:** This is the deliberate inverse of `ph-build`'s **never block on the human**, and both are correct in their own harness. An unattended agent that stops to ask is a stall with nobody to answer. A planning session that guesses instead of asking has thrown away the one resource that made it a session.

**Pattern:**

- **Ask, then wait.** Put the decision to them and stop. Do not proceed on an assumption and offer to revise later.
- **Recommend, never merely present.** Every question carries your recommended answer. A menu without a recommendation makes the human do your thinking.
- **Facts are yours, decisions are theirs.** Anything you could look up - the filesystem, the code, the tracker - you look up. Never ask a human for a fact.
- **Disagreement is signal.** When they reject your recommendation, the reason matters more than the answer. Ask for it.

**Boundaries:**

- Reversible *research* actions proceed freely - reading, searching, dispatching a sub-agent to find something out.
- Once the frontier is empty and the user has confirmed, execution hands off to `ph-build`, where the opposite rule governs.

**The test:** Did you ask the human anything they alone could answer? If a whole session passed without a real question, you were not planning - you were narrating.
