---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

## Purpose
Interview the user relentlessly, as a design tree worked in rounds, until plan or decision is fully understood.

## When NOT to use
- The user wants a quick answer or implementation.
- Decisions are already settled and documented.

## Inputs
The plan, decision or idea to stress-test.

## Edge cases and failure handling
- User answers conflict with earlier answers -> surface the conflict and ask which holds.
- Question can be answered by reading the repo -> read it instead of asking.

## Validation
- No frontier questions remain; each decision has a stated answer; assumptions listed.

## Output requirements
Resolved decision tree and a list of open items.

## Related skills
grill-me, grill-with-docs, domain-modeling

## When to use
The user wants to stress-test a plan, decision or idea, or says "grill me".

## Core workflow
1. Build the design tree of decisions.
2. Compute the frontier of unblocked questions.
3. Ask the whole frontier in one numbered round with a recommended answer each.
4. Look up facts yourself (sub-agent) instead of asking.
5. Update the tree from the answers and repeat until the frontier is empty.

## Example
```text
"Grill my pricing plan": Q1 freemium vs trial (recommend trial) ... next round after answers.
```
