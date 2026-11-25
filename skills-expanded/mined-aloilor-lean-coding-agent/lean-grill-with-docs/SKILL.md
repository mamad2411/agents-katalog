---
name: lean-grill-with-docs
description: Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation in GLOSSARY.md and ADRs inline as decisions crystallize. Use when the user is creating or refining a plan or design and wants it grilled against their project's language and documented decisions.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. A question that depends on another question still open belongs to a later round. Ask the whole frontier in one round, numbering each question and giving your recommended answer, then wait for the user's answers. Recompute the frontier from the settled decisions and ask the next round.

Format each question like so, separating questions with `---`:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), use the `explorer` subagent if available; otherwise, dispatch a sub-agent on the smallest model suited to the task. If you can't dispatch one, look it up yourself. Don't ask the user for anything you could look up. Don't block on a running exploration: it's an unsettled prerequisite, so only the questions downstream of it wait for the result; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

# Domain Modeling

Actively build and sharpen the project's domain model as you design: challenge terms, invent edge-case scenarios, and write the glossary and decisions down the moment they crystallise.

For where `GLOSSARY.md` and ADRs live, and how to tell single- from multi-context repos, see [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md) and [ADR-FORMAT.md](./ADR-FORMAT.md). Create files lazily: only when you have something to write.

During the session:

- **Challenge against the glossary.** When a term conflicts with `GLOSSARY.md`, call it out immediately: "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"
- **Sharpen fuzzy language.** Propose a precise canonical term for vague or overloaded ones: "By 'account', do you mean the Customer or the User?"
- **Discuss concrete scenarios.** Stress-test domain relationships with invented edge cases that force precise boundaries between concepts.
- **Cross-reference with code.** When the user states how something works, check the code and surface contradictions: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"
- **Update `GLOSSARY.md` inline.** Record each term as soon as it's resolved, using [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md). No implementation details: it's a glossary, not a spec.

Offer an ADR only when the decision is all three:

1. **Hard to reverse**: changing your mind later is costly
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
