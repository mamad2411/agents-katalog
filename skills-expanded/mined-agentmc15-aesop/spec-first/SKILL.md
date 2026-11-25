---
name: spec-first
description: Turn a feature request or task into a written spec before any code is written. Use whenever the user asks to build, add, or implement something non-trivial (3+ steps or an architectural decision), or says "let's design", "write the spec", or "plan this". Produces the spec the human approves and the agent executes against.
---
# spec-first

The human owns the spec and the taste; the agent fills in the blanks. A written spec up front
removes the ambiguity an agent would otherwise fill with a confident wrong guess (the classic:
correlating accounts by email instead of a persistent user ID).

## Steps
1. Restate the goal in one sentence as a **checkable success criterion**.
2. List the top-level decisions a human must own: identity/keys, data model, security boundaries,
   external dependencies, irreversible actions. Surface trade-offs; don't pick silently.
3. Draft the spec: scope, non-goals, interfaces/contracts, the verification plan (what proves it
   works), and open questions.
4. Get explicit human sign-off on the spec before writing code.
5. Keep the spec in the repo (`docs/specs/` or `tasks/`) so the implementing agent reads it, not
   re-derives it.

## Notes
- A strong spec is what lets an agent run autonomously (and what a `/goal` loop needs). A weak spec
  ("make it work") forces constant clarification.
- Don't over-spec trivial changes — match ceremony to stakes.
