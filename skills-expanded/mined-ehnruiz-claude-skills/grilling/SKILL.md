---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea until every branch of it is settled. Use when the user wants to stress-test their thinking, says "grill me", "poke holes in this", "interrogate this plan", or asks to be questioned before building something.
---

# Grilling

Interview the user relentlessly until you reach a shared understanding. Credit and license:
`LICENSE.md` in this folder.

Map the plan as a **design tree**: every decision branches into the decisions that hang off it.

## Rounds

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already
settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask
the whole frontier in one round: number each question and give your recommended answer. Word
each question so "yes" accepts your recommended answer, so agreeing never means answering "no".
Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and
unblock questions that depended on them. Recompute the frontier and ask the next round. A
question whose answer depends on another question still open in this round belongs to a _later_
round, not this one.

## Facts are yours, decisions are theirs

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the
environment (the code, the docs, a config, a tool's output), look it up: hand it to a background
subagent if you have one, otherwise read it yourself. Never ask the user for anything you could
look up. Don't block on a lookup: a running search is an unsettled prerequisite, so only the
questions downstream of it wait; ask the rest of the frontier now.

The _decisions_ are the user's: put each one to them and wait.

## Done

The session is done when the frontier is empty: every branch of the design tree visited,
nothing left silently assumed. Close with the settled decisions as a short list. Do not act on
them until the user confirms you have reached a shared understanding.
