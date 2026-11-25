---
name: decision-frameworks
description: "Make product decisions with structure and speed, even with imperfect information. Covers decision types, reversibility, and knowing how much analysis is enough. Use when decisions are stalling, when the team is stuck in analysis paralysis, or when decisions keep getting revisited."
---

# Decision Frameworks

Make better decisions faster by knowing what kind of decision you're making.

## How to use

- `/decision-frameworks` Apply decision framework constraints to this conversation.
- `/decision-frameworks <decision>` Apply the right framework to the described decision.

## Constraints

### Decision Typing
Classify every decision before making it:
- One-way door (irreversible): pricing model, platform migration, market positioning. Take more time.
- Two-way door (reversible): feature design, copy, UI layout. Decide fast, iterate based on data.
- MUST match analysis effort to decision type. Don't spend a week on a two-way door.
- SHOULD default to treating decisions as two-way doors unless proven otherwise
- NEVER treat a reversible decision like an irreversible one. Speed matters.

### Decision Quality
- MUST define the decision clearly: what exactly are we choosing between?
- MUST identify the criteria: what matters most in this decision?
- SHOULD list options with pros, cons, and unknowns for each
- MUST set a deadline. Decisions without deadlines never get made.
- SHOULD designate one decision-maker. Consensus is slow and often produces mediocre outcomes.

### Information Sufficiency
- MUST decide how much information is enough before gathering more
- For most product decisions, 70% confidence is sufficient to act
- SHOULD ask: "what additional information would change my decision?" If nothing, stop analyzing.
- MUST distinguish between information that reduces risk and information that delays action
- NEVER use "we need more data" as a way to avoid making a hard call

### Decision Communication
- MUST document: what was decided, why, what alternatives were considered, and who was involved
- SHOULD share decisions with affected teams promptly
- MUST create space for disagreement before the decision, not after
- Once decided: disagree and commit. NEVER undermine a decision you were part of making.
- MUST be willing to revisit decisions when new information fundamentally changes the context

### Anti-Patterns
- Analysis Paralysis: endlessly gathering data to avoid committing
- Decision by Committee: requiring consensus on everything, getting mediocrity
- The Redo: making the same decision three times because it was never properly committed to
- HiPPO Decisions: highest paid person's opinion always wins regardless of evidence
- The Non-Decision: not deciding and letting the default happen by inaction
