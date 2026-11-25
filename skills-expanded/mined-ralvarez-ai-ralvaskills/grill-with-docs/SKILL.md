---
name: grill-with-docs
version: 1.1.3
description: Grilling session that stress-tests an existing plan against the project's domain model and updates CONTEXT.md and ADRs as decisions crystallise. Use when a plan exists and needs challenging.
---

# Grill With Docs

## What to do

Interview the user relentlessly about every aspect of their plan until you both reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Domain awareness

During codebase exploration, also look for existing documentation:

### File structure

Most repos have a single context (root `CONTEXT.md`, `docs/adr/`). If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts and the map points to where each lives; each context keeps its own `CONTEXT.md` and `docs/adr/`, with system-wide decisions in the root `docs/adr/`. Directory trees: [CONTEXT_FORMAT.md](./CONTEXT_FORMAT.md#directory-layout).

Create files lazily - only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y - which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' - do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible - which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up - capture them as they happen. Use the format in [CONTEXT_FORMAT.md](./CONTEXT_FORMAT.md).

`CONTEXT.md` is a glossary only, totally devoid of implementation details: no specs, scratch pad, or implementation decisions.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** - the cost of changing your mind later is meaningful
2. **Surprising without context** - a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** - there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR_FORMAT.md](./ADR_FORMAT.md).

---

_Adapted from [mattpocock/skills `grill-with-docs`](https://github.com/mattpocock/skills/tree/e74f0061bb67222181640effa98c675bdb2fdaa7/skills/engineering/grill-with-docs) by Matt Pocock (MIT). Changed for this workspace._
