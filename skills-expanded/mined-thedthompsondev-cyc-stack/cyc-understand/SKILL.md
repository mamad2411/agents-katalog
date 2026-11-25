---
name: cyc-understand
description: "Build an evidence-backed model of how the existing system behaves, or reproduce and locate a failure. Use for \"how does X work\", \"why does X happen\", bug reports, anything broken, throwing, or slow, and before designing a change to unfamiliar code."
---

# Understand the existing system

Produce a model of the real behavior that the next skill can rely on. Read-only unless an experiment is authorized. Follow the [handoff contract](../../docs/skill-contract.md) for labeling observed versus inferred claims.

**Something is broken?** Search the [error ledger](../cyc-error-ledger/SKILL.md) first, then use the [diagnose branch](references/diagnose.md). Its rule is "no red loop, no fix."

## The core loop

1. **Find relevant project evidence.** Once paths are known, use `node <cli> investigate --path <paths>` to retrieve matching [context](../cyc-context/SKILL.md) and recipes; reuse an existing Scout result while it applies. Run relevant investigation recipes when their prerequisites hold and effects are authorized; otherwise explain the specific unavailable check. Consult project instructions, terminology and test layout as needed. Use the project's vocabulary, explaining a user/code naming difference once. The [project tools guide](../../docs/project-tools.md) covers discovery and execution.
2. **Find the real entry point.** The route, handler, command, event, or component where the behavior starts. Search for the user-visible string or the route first; it is usually faster than guessing file names.
3. **Trace the path end to end.** Entry, validation, state change, persistence, and what reads the result. Write it as a chain with file:line for each hop:
   `click → Card.onFinish (Card.tsx:42) → store.update (store.ts:88) → saveAll (storage.ts:15)`
4. **Check the user's claims against the code.** If the user said "it saves to the server" and it writes localStorage, surface that contradiction immediately. It usually changes the plan.
5. **Observe when reading is ambiguous.** Run the code, print the stored value, or hit the endpoint. One observation beats three paragraphs of inference.
6. **Answer "why" honestly.** Look for commit messages, ADRs, or comments. Without them, label the reason as inference.

## Done when

- The path is written as a chain with a real location for every hop.
- Every claim the next step depends on is marked observed (you ran or saw it) or inferred (you read it).
- Contradictions between the user's description and the code are listed.
- For a bug: the diagnose branch's red loop exists and the cause is confirmed.

## Anti-patterns

| Name | The tell | Fix |
| --- | --- | --- |
| File tour | A list of files with one-line summaries | Write the chain of calls instead |
| Tests as truth | "The test says it works" | Tests show intent; run it to see behavior |
| Whole-repo read | Opening dozens of files before finding the entry point | Search for the visible string or route first |
| Fix before repro | Changing code for a bug that was never reproduced | Build the red loop first; reading code to find the repro conditions is fine |

## Handoff

For a change, pass the chain, observed facts, contradictions, and open questions to [Impact](../cyc-impact/SKILL.md). For an explanation or lesson, return the model to the parent. For a bug, hand the red loop and confirmed cause onward; do not fix unrelated things you noticed, but list them.
